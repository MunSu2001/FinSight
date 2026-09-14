# 도메인 레퍼런스

확인일: 2026-09-14

이 문서는 투자 추천 기준이 아니라, FinSight가 사용하는 공시·재무 데이터의 의미와 해석 경계를 확인하기 위한 1차 출처 목록이다.

| 자료 | 확인한 사실 | FinSight에서의 활용 |
|---|---|---|
| [OpenDART 서비스 소개](https://opendart.fss.or.kr/) | OpenDART는 DART 공시정보를 API, XBRL, Excel, TXT 등의 형태로 활용할 수 있게 개방하며 사업보고서·재무정보 조회 기능을 제공한다. | 재무 수치·사업보고서·공시 목록의 공식 원천 범위를 설명한다. |
| [OpenDART 공시정보 개발가이드](https://opendart.fss.or.kr/guide/main.do?apiGrpCd=DS001) | 공시검색, 기업개황, 공시서류 원본파일, 고유번호 등 공시정보 API를 제공한다. | 기업 식별, 기간 공시 목록, 원문 근거의 데이터 출처를 구분한다. |
| [IFRS 10 — Consolidated Financial Statements](https://www.ifrs.org/issued-standards/list-of-standards/ifrs-10-consolidated-financial-statements/) | 연결재무제표는 모회사와 자회사의 자산·부채·자본·수익·비용·현금흐름을 하나의 경제 실체처럼 표시한다. | CFS가 무엇을 의미하는지와 연결 기준 수치가 단일 법인 수치와 다를 수 있는 이유를 설명한다. |
| [IAS 27 — Separate Financial Statements](https://www.ifrs.org/content/dam/ifrs/publications/pdf-standards/english/2021/issued/part-a/ias-27-separate-financial-statements.pdf) | 별도재무제표는 투자기업이 종속기업·관계기업·공동기업 투자에 대한 회계처리를 따로 표시하는 재무제표다. | OFS가 연결 기준의 단순 세부 행이 아니라 별도 기준 재무제표임을 설명한다. |

## FinSight에 적용하는 해석 경계

- “연결이 항상 더 좋다”는 외부 회계 기준의 결론이 아니다. V1의 **CFS 우선, 부재 시 OFS 전체 대체**는 기업집단 기준 비교를 일관되게 하려는 프로젝트 정책이며, [V1 요구사항](../../v1/REQUIREMENTS.md)에 기록돼 있다.
- CFS와 OFS는 동일한 분석 표에 일부 항목만 섞지 않는다. 비교 기준이 달라져 사용자가 수치를 잘못 해석할 수 있기 때문이다. 이 역시 FinSight의 데이터 계약 정책이다.
- 재무지표의 공식·단위·결측 처리처럼 추가 검증이 필요한 도메인 규칙은 실제 평가 직전에 공식 자료를 추가 수집한다. 근거 없는 투자 해석이나 매수·매도 판단은 이 문서의 범위가 아니다.

용어의 간단한 설명은 [DOMAIN_GLOSSARY.md](../../DOMAIN_GLOSSARY.md)를 본다.
