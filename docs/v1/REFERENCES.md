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

## V1 OpenAI API 모델 비교 레퍼런스

2026-09-15에 확인한 공식 자료다. 이 비교는 기존 `.env`의 `OPENAI_MODEL`을 사용해 로컬 Qwen과 API 모델의 기업명 검색어 확장 품질을 비교한다. API 키 값은 notebook 출력·문서·Git에 기록하지 않는다.

| 자료 | 확인한 내용 | 활용 목적 |
|---|---|---|
| [LangChain ChatOpenAI integration](https://docs.langchain.com/oss/python/integrations/chat/openai) | `langchain-openai`의 `ChatOpenAI`는 `OPENAI_API_KEY`를 읽고, 구조화 출력과 token usage 메타데이터를 지원한다. | 16번 상세 Prompt B를 유지한 API 모델 호출과 입력·출력 token 기록 |
| [OpenAI Models](https://developers.openai.com/api/docs/models/gpt-5.6-luna) | 현재 설정 모델 `gpt-5.6-luna`는 비용 민감형 모델이며, 문서상 일반 입력 $0.20/MTok·캐시 입력 $0.02/MTok·출력 $1.20/MTok으로 안내된다. | 실행 시점의 token usage로 사전 연결 확인과 평가 호출 비용을 구분해 추정. 가격은 변경될 수 있어 결과 보고서에 기준일·출처를 함께 기록 |
| [OpenAI API 데이터 정책](https://developers.openai.com/api/docs/guides/your-data) | API 전송 데이터는 기본적으로 모델 학습에 사용되지 않지만, abuse-monitoring 로그는 기본적으로 최대 30일 보관될 수 있다. | 외부 모델 호출 시 데이터 보존 조건을 명시하고, API 키·민감 입력을 출력·Git에서 제외 |

### 이번 비교의 고정 조건

- `.env`의 `OPENAI_API_KEY`, `OPENAI_MODEL`을 사용한다. 키 값은 출력하지 않는다.
- 16번에서 조건부 채택한 상세 Prompt B와 같은 26개 개발 사례·OpenDART 재검증·Pydantic 출력 계약을 사용한다.
- API 모델도 `corp_code`를 선택하지 않고 검색어 가설만 반환한다.
- 모델 품질 외에 API 구조화 출력 방식이 달라질 수 있으므로, 결과는 순수 모델 크기만이 아니라 **모델·제공처 조합**의 비교로 해석한다.
- 실행 결과에는 Candidate Recall, 안전 보류, 구조화 출력, token usage, 추정 비용, p50/p95를 기록한다.

## V1 LangChain Tool Calling Prompt 평가 레퍼런스

2026-09-21에 확인한 공식 자료다. V1-21은 Tool 실행 결과가 아니라 `bind_tools()` 이후 모델이 반환하는 Tool 호출 요청과 인자를 A/B Prompt 조건에서 비교한다.

| 자료 | 확인한 내용 | 활용 목적 |
|---|---|---|
| [LangChain Tools](https://docs.langchain.com/oss/python/langchain/tools) | Tool은 호출 가능한 함수와 입력 스키마를 모델에 제공하는 인터페이스다. | 재무·계산·공시·사업보고서 검색의 함수명, 설명, 인자를 고정해 Prompt만 비교 |
| [LangChain Models — Tool calling](https://docs.langchain.com/oss/python/langchain/models) | `bind_tools()`로 Tool 스키마를 모델에 연결하면 모델 응답의 `tool_calls`에서 호출 이름과 인자를 읽을 수 있다. | 실제 함수를 실행하지 않고 Tool 선택·인자 생성 품질을 측정 |
| [LangChain Structured output](https://docs.langchain.com/oss/python/langchain/structured-output) | 스키마 기반 제약은 후속 코드가 읽을 출력 계약을 만들며, provider별 전략이 다를 수 있다. | 이번 단계의 Tool 호출과 이후 Router 구조화 출력 평가의 차이와 경계를 기록 |

이번 비교에서는 **동일 모델, 동일 Tool 정의, 동일 개발 질문**에서 System Prompt만 바꾼다. 이 결과는 Prompt 조건의 Tool 호출 계획 품질이며, 실제 OpenDART 실행·계산·RAG 검색·최종 답변 품질을 의미하지 않는다.

## 아직 수집하지 않는 자료

- LlamaIndex의 parsing, chunking, embedding, vector store, retrieval 평가 문서는 공시 원문 RAG의 데이터 범위와 비교 후보가 정해지는 시점에 최신 공식 문서로 수집한다.
- Recall@K, MRR, nDCG의 계산 기준과 평가셋 작성 참고자료는 실제 retrieval 평가 단계 직전에 수집한다. 현재 공시 목록 조회에는 retrieval 지표를 적용하지 않는다.
