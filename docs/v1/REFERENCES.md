# V1 사전 레퍼런스 — OpenDART

V1의 데이터 계약과 초기 OpenDART 조회 범위를 정할 때 확인한 공식 자료다. API 구현 전에는 이 문서를 다시 확인하고, 요청·응답 필드와 제한 사항이 바뀌었는지 점검한다.

| 자료 | V1에서 확인할 내용 | 활용 목적 |
|---|---|---|
| [고유번호 API 개발가이드](https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS001&apiId=2019018) | `corp_code`, `corp_name`, `stock_code`, `modify_date`가 ZIP 안 XML에 포함됨 | 기업명에서 OpenDART 고유번호를 찾는 기준 확인 |
| [기업개황 API 개발가이드](https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS001&apiId=2019002) | `stock_code`, `corp_cls`, `induty_code`, 결산월을 제공 | 상장 상태·업종·결산월 확인 기준 |
| [단일회사 전체 재무제표 API 개발가이드](https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS003&apiId=2019020) | `fnlttSinglAcntAll`의 요청 URL과 필수 인증·기업 식별 인자 | 사업보고서 기준 재무계정 raw 응답 확인 |
| [정기보고서 재무정보 API 목록](https://opendart.fss.or.kr/guide/main.do?apiGrpCd=DS003) | 재무정보는 정기보고서의 XBRL 재무제표 기반이며, 대상 회사 범위가 명시됨 | 재무 수치의 데이터 원천과 제한 기록 |
| [공시검색 API 개발가이드](https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS001&apiId=2019001) | 기업·기간·공시 유형·정렬 조건으로 공시 목록을 검색하고 `rcept_no`를 받음 | 기간 조건 공시 목록과 원문 식별자 확인 |
| [통계청 한국표준산업분류](https://kostat.go.kr/boardDownload.es?bid=108&list_no=422598&seq=3) | 금융 및 보험업은 대분류 K(64~66) | OpenDART 업종코드와 금융·비금융 판정 기준을 검증할 때 참고 |
| [RapidFuzz `process` 공식 문서](https://rapidfuzz.github.io/RapidFuzz/Usage/process.html) | `extract`는 문자열 후보 목록에서 유사도 순 상위 결과를 반환하며, scorer·후보 수·점수 cutoff를 설정할 수 있음 | 기업명 오타·부분 표현의 후보 생성 방식과 Candidate Recall@K 비교 |

## V1에 적용하는 기준

- 기본 보고서는 사업보고서(`reprt_code=11011`)다.
- 연결 재무제표를 우선 사용하고, 없을 때만 별도 재무제표로 대체한 뒤 기준을 결과에 표시한다.
- 기본 공시 근거는 사업보고서 원문 링크다. 기간 내 공시 목록은 사용자가 요청한 경우에만 최종 제출본(`last_reprt_at=Y`)으로 추가하며, V1은 목록의 중요도를 자동 판정하지 않는다.
- API 키는 `.env`의 `OPENDART_API_KEY`에서만 읽는다. 문서·출력·Git에는 기록하지 않는다.
- V1은 상장·비상장 OpenDART 공시기업을 식별·조회 대상으로 하며, 금융·보험업은 제외한다. OpenDART `induty_code`와 한국표준산업분류의 실제 매핑·예외 처리는 데이터 계약 단계에서 검증하기 전까지 확정하지 않는다.

## V1 후속 단계의 초기 기술 레퍼런스

아래 자료는 이미 학습한 개념을 V1 검증에 적용할 때 다시 확인할 공식 문서다. 지금은 API 호출 기준선만 구현했으므로, 이 문서를 근거로 새로운 패키지나 workflow를 추가하지 않는다.

| 단계 | 자료 | 확인할 핵심 |
|---|---|---|
| Router·Tool | [LangChain Models](https://docs.langchain.com/oss/python/langchain/models), [Tools](https://docs.langchain.com/oss/python/langchain/tools) | Tool은 입력 스키마와 실행 함수의 쌍이며, 모델의 요청과 실제 실행을 분리해야 함 |
| 구조화 질문 해석 | [LangChain Structured Output](https://docs.langchain.com/oss/python/langchain/structured-output) | 스키마 기반 필드 검증과 structured output 전략 |
| 단일 workflow | [LangGraph Graph API](https://docs.langchain.com/oss/python/langgraph/graph-api) | State·Node·Edge의 역할, 조건부 edge의 라우팅 규칙 |
| 로컬 Qwen 연결 | [ChatOllama integration](https://docs.langchain.com/oss/python/integrations/chat/ollama) | `langchain-ollama` 패키지, 모델 호출·tool calling 지원 확인 방법 |

## V1 기업 식별 LLM 검색어 제안 평가 레퍼런스

2026-09-14에 다시 확인한 공식 자료다. 다음 평가에서는 LLM이 `corp_code`를 고르거나 OpenDART를 직접 호출하지 않고, 구조화된 **검색어 후보**만 반환하게 한다.

| 자료 | 이번 평가에서 확인한 내용 | 활용 목적 |
|---|---|---|
| [LangChain Models — Structured output](https://docs.langchain.com/oss/python/langchain/models) | `with_structured_output()`은 Pydantic 스키마로 출력 형식을 제한하며, `include_raw=True`로 원문·파싱 결과·오류를 함께 받을 수 있음 | 검색어 후보 수·문자열 길이·허용 필드를 검사하고, 형식 실패를 별도 지표로 기록 |
| [LangChain ChatOllama integration](https://docs.langchain.com/oss/python/integrations/chat/ollama) | `ChatOllama`는 구조화 출력과 tool calling을 지원하며 `temperature=0`으로 생성 조건을 고정할 수 있음 | 로컬 `qwen3.6:27b`를 같은 실행 조건으로 호출하고 응답 메타데이터에서 지연시간을 기록 |

이번 단계의 안전 경계는 다음과 같다.

```text
사용자 원문 기업 표현 + LLM 제안 검색어
→ OpenDART 기업 목록에서 각각 후보 탐색
→ corp_code 기준 후보 병합
→ 코드가 RESOLVED / NEEDS_CONFIRMATION / NOT_FOUND 처리
```

LLM 제안은 후보 생성의 입력일 뿐, 단독으로 기업 또는 `corp_code`를 자동 확정하는 근거가 아니다. 정확한 정식 법인명에서 OpenDART 고유 exact 결과가 하나이면 LLM 호출 없이 그대로 처리한다.

## 아직 수집하지 않는 자료

- LlamaIndex의 parsing, chunking, embedding, vector store, retrieval 평가 문서는 공시 원문 RAG의 데이터 범위와 비교 후보가 정해지는 시점에 최신 공식 문서로 수집한다.
- Recall@K, MRR, nDCG의 계산 기준과 평가셋 작성 참고자료는 실제 retrieval 평가 단계 직전에 수집한다. 현재 공시 목록 조회에는 retrieval 지표를 적용하지 않는다.
