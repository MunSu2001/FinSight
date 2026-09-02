"""OpenDART에서 기업의 주요 재무정보를 조회하는 최소 함수 모음."""

import io
import json
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
import zipfile


CORP_CODE_URL = "https://opendart.fss.or.kr/api/corpCode.xml"
FINANCIALS_URL = "https://opendart.fss.or.kr/api/fnlttSinglAcntAll.json"
DISCLOSURE_LIST_URL = "https://opendart.fss.or.kr/api/list.json"

TARGET_ACCOUNTS = {
    "매출액": {
        "ids": {"ifrs-full_Revenue", "ifrs-full_RevenueFromContractsWithCustomers"},
        "names": {"매출액", "수익(매출액)"},
    },
    "영업이익": {
        "ids": {"dart_OperatingIncomeLoss"},
        "names": {"영업이익", "영업이익(손실)"},
    },
    "당기순이익": {
        "ids": {"ifrs-full_ProfitLoss"},
        "names": {"당기순이익", "당기순이익(손실)"},
    },
}


def _get_bytes(url: str, params: dict[str, str], timeout: int = 30) -> bytes:
    """OpenDART GET 요청의 응답 바이트를 반환한다."""
    request_url = f"{url}?{urllib.parse.urlencode(params)}"

    try:
        with urllib.request.urlopen(request_url, timeout=timeout) as response:
            return response.read()
    except urllib.error.HTTPError as error:
        raise RuntimeError(f"OpenDART HTTP 오류: {error.code}") from None
    except urllib.error.URLError as error:
        raise RuntimeError(f"OpenDART 네트워크 연결 오류: {error.reason}") from None


def find_corp_info(corp_name: str, api_key: str) -> dict[str, str]:
    """정식 기업명과 정확히 일치하는 기업의 정보와 corp_code를 찾는다."""
    corp_zip_bytes = _get_bytes(CORP_CODE_URL, {"crtfc_key": api_key})
    corp_zip_stream = io.BytesIO(corp_zip_bytes)

    if not zipfile.is_zipfile(corp_zip_stream):
        error_text = corp_zip_bytes.decode("utf-8", errors="replace")
        raise RuntimeError(f"기업 고유번호 응답이 ZIP이 아닙니다:\n{error_text}")

    with zipfile.ZipFile(corp_zip_stream) as archive:
        xml_bytes = archive.read(archive.namelist()[0])

    root = ET.fromstring(xml_bytes)
    matches = [
        {child.tag: child.text or "" for child in item}
        for item in root.findall("list")
        if item.findtext("corp_name") == corp_name
    ]

    if len(matches) != 1:
        raise LookupError(
            f"{corp_name!r}과 정확히 일치하는 기업이 1개가 아닙니다: {len(matches)}개"
        )

    return matches[0]


def fetch_financial_rows(
    corp_code: str,
    business_year: int,
    api_key: str,
    report_code: str = "11011",
    fs_div: str = "CFS",
) -> list[dict[str, str]]:
    """단일회사의 전체 재무제표 raw JSON에서 계정 행 목록을 반환한다."""
    response_bytes = _get_bytes(
        FINANCIALS_URL,
        {
            "crtfc_key": api_key,
            "corp_code": corp_code,
            "bsns_year": str(business_year),
            "reprt_code": report_code,
            "fs_div": fs_div,
        },
    )
    response = json.loads(response_bytes.decode("utf-8"))

    if response.get("status") != "000":
        raise RuntimeError(
            f"OpenDART 재무제표 오류 [{response.get('status')}]: {response.get('message')}"
        )

    return response.get("list", [])


def fetch_disclosure_rows(
    corp_code: str,
    start_date: str,
    end_date: str,
    api_key: str,
    final_reports_only: bool = True,
) -> list[dict[str, str]]:
    """기간 내 공시 목록의 모든 페이지를 조회한다."""
    params = {
        "crtfc_key": api_key,
        "corp_code": corp_code,
        "bgn_de": start_date,
        "end_de": end_date,
        "last_reprt_at": "Y" if final_reports_only else "N",
        "sort": "date",
        "sort_mth": "desc",
        "page_count": "100",
    }
    rows: list[dict[str, str]] = []
    page_no = 1

    while True:
        response_bytes = _get_bytes(
            DISCLOSURE_LIST_URL,
            {**params, "page_no": str(page_no)},
        )
        response = json.loads(response_bytes.decode("utf-8"))

        if response.get("status") != "000":
            raise RuntimeError(
                f"OpenDART 공시 목록 오류 [{response.get('status')}]: "
                f"{response.get('message')}"
            )

        rows.extend(response.get("list", []))
        total_page = int(response.get("total_page", 1))
        if page_no >= total_page:
            total_count = int(response.get("total_count", 0))
            if len(rows) != total_count:
                raise RuntimeError(
                    f"OpenDART 공시 목록 수가 일치하지 않습니다: "
                    f"{len(rows)} / {total_count}"
                )
            return rows

        page_no += 1


def build_filing_url(rcept_no: str) -> str:
    """OpenDART 접수번호로 DART 공시 원문 URL을 만든다."""
    return f"https://dart.fss.or.kr/dsaf001/main.do?rcpNo={rcept_no}"


def _find_account(rows: list[dict[str, str]], target: dict[str, set[str]]) -> dict[str, str] | None:
    income_rows = [row for row in rows if row.get("sj_div") in {"IS", "CIS"}]

    by_id = next(
        (row for row in income_rows if row.get("account_id") in target["ids"]),
        None,
    )
    if by_id:
        return by_id

    return next(
        (row for row in income_rows if row.get("account_nm") in target["names"]),
        None,
    )


def summarize_financial_rows(
    corp_name: str,
    business_year: int,
    rows: list[dict[str, str]],
) -> dict[str, str | int | None]:
    """재무제표 행에서 매출액, 영업이익, 당기순이익만 추린다."""
    selected_accounts = {
        label: _find_account(rows, target)
        for label, target in TARGET_ACCOUNTS.items()
    }

    return {
        "기업명": corp_name,
        "사업연도": business_year,
        **{
            label: row.get("thstrm_amount") if row else None
            for label, row in selected_accounts.items()
        },
    }


def get_financial_summary(
    corp_name: str,
    business_year: int,
    api_key: str,
    report_code: str = "11011",
    fs_div: str = "CFS",
) -> dict[str, str | int | None]:
    """기업명과 사업연도로 주요 재무정보를 조회한다."""
    corp_info = find_corp_info(corp_name, api_key)
    rows = fetch_financial_rows(
        corp_info["corp_code"],
        business_year,
        api_key,
        report_code=report_code,
        fs_div=fs_div,
    )
    return summarize_financial_rows(corp_info["corp_name"], business_year, rows)
