# 도메인 레퍼런스

확인일: 2026-10-01

이 문서는 투자 추천 기준이 아니라, FinSight가 사용하는 공시·재무 데이터의 의미와 해석 경계를 확인하기 위한 1차 출처 목록이다.

| 자료 | 확인한 사실 | FinSight에서의 활용 |
|---|---|---|
| [OpenDART 서비스 소개](https://opendart.fss.or.kr/) | OpenDART는 DART 공시정보를 API, XBRL, Excel, TXT 등의 형태로 활용할 수 있게 개방하며 사업보고서·재무정보 조회 기능을 제공한다. | 재무 수치·사업보고서·공시 목록의 공식 원천 범위를 설명한다. |
| [OpenDART 공시정보 개발가이드](https://opendart.fss.or.kr/guide/main.do?apiGrpCd=DS001) | 공시검색, 기업개황, 공시서류 원본파일, 고유번호 등 공시정보 API를 제공한다. | 기업 식별, 기간 공시 목록, 원문 근거의 데이터 출처를 구분한다. |
| [IFRS 10 — Consolidated Financial Statements](https://www.ifrs.org/issued-standards/list-of-standards/ifrs-10-consolidated-financial-statements/) | 연결재무제표는 모회사와 자회사의 자산·부채·자본·수익·비용·현금흐름을 하나의 경제 실체처럼 표시한다. | CFS가 무엇을 의미하는지와 연결 기준 수치가 단일 법인 수치와 다를 수 있는 이유를 설명한다. |
| [IAS 27 — Separate Financial Statements](https://www.ifrs.org/content/dam/ifrs/publications/pdf-standards/english/2021/issued/part-a/ias-27-separate-financial-statements.pdf) | 별도재무제표는 투자기업이 종속기업·관계기업·공동기업 투자에 대한 회계처리를 따로 표시하는 재무제표다. | OFS가 연결 기준의 단순 세부 행이 아니라 별도 기준 재무제표임을 설명한다. |
| [CFA Institute — Financial Ratio List](https://www.cfainstitute.org/sites/default/files/-/media/documents/support/programs/cfa/cfa_program_level_ii_financial_ratio_list.pdf) | 영업이익률·순이익률은 매출을 분모로, ROA·ROE는 평균 자산·평균 자본을 분모로, 유동비율은 유동부채를 분모로 계산한다. 같은 이름의 재무비율도 정의가 달라질 수 있음을 명시한다. | V1 계산식의 공통 부분을 확인하고 분모·기간 기준을 기록한다. |
| [KRX KIND 공시의 부채비율 정의 사례](https://kind.krx.co.kr/external/2025/08/06/000531/20250806000057/91954.htm) | 해당 공시는 부채비율을 재무제표상 부채총계 ÷ 자본총계로 정의한다. | FinSight의 `부채비율`이 총부채가 아닌 **부채총계**를 분자로 쓰는 프로젝트 정의임을 분명히 한다. |

## FinSight에 적용하는 해석 경계

- “연결이 항상 더 좋다”는 외부 회계 기준의 결론이 아니다. V1의 **CFS 우선, 부재 시 OFS 전체 대체**는 기업집단 기준 비교를 일관되게 하려는 프로젝트 정책이며, [V1 요구사항](../../v1/REQUIREMENTS.md)에 기록돼 있다.
- CFS와 OFS는 동일한 분석 표에 일부 항목만 섞지 않는다. 비교 기준이 달라져 사용자가 수치를 잘못 해석할 수 있기 때문이다. 이 역시 FinSight의 데이터 계약 정책이다.
- V1의 매출 성장률·영업이익률·순이익률·ROA·ROE·부채비율·유동비율 계산식은 [용어집](../../DOMAIN_GLOSSARY.md)에 기록한다. ROA·ROE의 평균은 전기말과 당기말 잔액의 단순 평균을 후보 기준으로 둔다. 영업현금흐름률(영업활동현금흐름 ÷ 매출액)은 FinSight가 명시한 프로젝트 정의 지표이며 CFA 목록의 표준 지표라고 주장하지 않는다.
- CFA 목록의 영문 `debt-to-equity ratio`는 이자부 단기·장기차입금인 `total debt`를 분자로 정의한다. FinSight의 한국어 `부채비율`은 **부채총계 ÷ 자본총계**이므로 두 지표를 같은 이름으로 바꿔 쓰거나 서로 직접 비교하지 않는다.
- 공식·단위·결측 처리의 실제 OpenDART 적용은 23번 재무 Tool 평가에서 확인한다. 근거 없는 투자 해석이나 매수·매도 판단은 이 문서의 범위가 아니다.

용어의 간단한 설명은 [DOMAIN_GLOSSARY.md](../../DOMAIN_GLOSSARY.md)를 본다.
