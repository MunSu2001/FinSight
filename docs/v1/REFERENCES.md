# V1 사전 레퍼런스 — OpenDART

V1의 데이터 계약과 초기 OpenDART 조회 범위를 정할 때 확인한 공식 자료다. API 구현 전에는 이 문서를 다시 확인하고, 요청·응답 필드와 제한 사항이 바뀌었는지 점검한다.

| 자료 | V1에서 확인할 내용 | 활용 목적 |
|---|---|---|
| [고유번호 API 개발가이드](https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS001&apiId=2019018) | `corp_code`, `corp_name`, `stock_code`, `modify_date`가 ZIP 안 XML에 포함됨 | 기업명에서 OpenDART 고유번호를 찾는 기준 확인 |
| [단일회사 전체 재무제표 API 개발가이드](https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS003&apiId=2019020) | `fnlttSinglAcntAll`의 요청 URL과 필수 인증·기업 식별 인자 | 사업보고서 기준 재무계정 raw 응답 확인 |
| [정기보고서 재무정보 API 목록](https://opendart.fss.or.kr/guide/main.do?apiGrpCd=DS003) | 재무정보는 정기보고서의 XBRL 재무제표 기반이며, 대상 회사 범위가 명시됨 | 재무 수치의 데이터 원천과 제한 기록 |
| [공시검색 API 개발가이드](https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS001&apiId=2019001) | 기업·기간·공시 유형·정렬 조건으로 공시 목록을 검색하고 `rcept_no`를 받음 | 기간 조건 공시 목록과 원문 식별자 확인 |

## V1에 적용하는 기준

- 기본 보고서는 사업보고서(`reprt_code=11011`)다.
- 연결 재무제표를 우선 사용하고, 없을 때만 별도 재무제표로 대체한 뒤 기준을 결과에 표시한다.
- 기본 공시 근거는 사업보고서 원문 링크다. 기간 내 공시 목록은 사용자가 요청한 경우에만 최종 제출본(`last_reprt_at=Y`)으로 추가하며, V1은 목록의 중요도를 자동 판정하지 않는다.
- API 키는 `.env`의 `OPENDART_API_KEY`에서만 읽는다. 문서·출력·Git에는 기록하지 않는다.

## V1 후속 단계의 초기 기술 레퍼런스

아래 자료는 이미 학습한 개념을 V1 검증에 적용할 때 다시 확인할 공식 문서다. 지금은 API 호출 기준선만 구현했으므로, 이 문서를 근거로 새로운 패키지나 workflow를 추가하지 않는다.

| 단계 | 자료 | 확인할 핵심 |
|---|---|---|
| Router·Tool | [LangChain Models](https://docs.langchain.com/oss/python/langchain/models), [Tools](https://docs.langchain.com/oss/python/langchain/tools) | Tool은 입력 스키마와 실행 함수의 쌍이며, 모델의 요청과 실제 실행을 분리해야 함 |
| 구조화 질문 해석 | [LangChain Structured Output](https://docs.langchain.com/oss/python/langchain/structured-output) | 스키마 기반 필드 검증과 structured output 전략 |
| 단일 workflow | [LangGraph Graph API](https://docs.langchain.com/oss/python/langgraph/graph-api) | State·Node·Edge의 역할, 조건부 edge의 라우팅 규칙 |
| 로컬 Qwen 연결 | [ChatOllama integration](https://docs.langchain.com/oss/python/integrations/chat/ollama) | `langchain-ollama` 패키지, 모델 호출·tool calling 지원 확인 방법 |

## 아직 수집하지 않는 자료

- LlamaIndex의 parsing, chunking, embedding, vector store, retrieval 평가 문서는 공시 원문 RAG의 데이터 범위와 비교 후보가 정해지는 시점에 최신 공식 문서로 수집한다.
- Recall@K, MRR, nDCG의 계산 기준과 평가셋 작성 참고자료는 실제 retrieval 평가 단계 직전에 수집한다. 현재 공시 목록 조회에는 retrieval 지표를 적용하지 않는다.
