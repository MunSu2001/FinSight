from src.dart.client import summarize_financial_rows


def test_summarize_financial_rows_selects_three_main_accounts():
    rows = [
        {
            "sj_div": "IS",
            "account_id": "ifrs-full_Revenue",
            "account_nm": "매출액",
            "thstrm_amount": "1000",
        },
        {
            "sj_div": "IS",
            "account_id": "dart_OperatingIncomeLoss",
            "account_nm": "영업이익",
            "thstrm_amount": "120",
        },
        {
            "sj_div": "IS",
            "account_id": "ifrs-full_ProfitLoss",
            "account_nm": "당기순이익",
            "thstrm_amount": "90",
        },
    ]

    summary = summarize_financial_rows("테스트기업", 2025, rows)

    assert summary == {
        "기업명": "테스트기업",
        "사업연도": 2025,
        "매출액": "1000",
        "영업이익": "120",
        "당기순이익": "90",
    }
