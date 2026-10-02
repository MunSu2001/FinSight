# 기술 레퍼런스

확인일: 2026-10-01

여기에는 실제로 사용하는 데이터 API와 프레임워크의 **공식 문서**를 기록한다. 패키지 버전이나 기능 지원은 변할 수 있으므로, 새 테스트·구현 직전에 해당 공식 문서를 다시 확인한다.

| 자료 | 확인한 사실 | FinSight에서의 활용 |
|---|---|---|
| [OpenDART 고유번호 API](https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS001&apiId=2019018) | DART 공시대상 회사의 `corp_code`, 회사명, 종목코드, 최근 변경일을 파일로 제공한다. | 사용자 기업명을 OpenDART 기업 후보와 `corp_code`로 검증한다. |
| [OpenDART 공시검색 API](https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS001&apiId=2019001) | 회사·접수일 기간·공시 유형 등으로 조회한다. `last_reprt_at=N`은 정정보고서를 포함한 제출본 전체, `Y`는 최종보고서만 검색한다. 응답에는 `total_count`, `total_page`, `rcept_no`, `rcept_dt`가 있고 페이지당 최대 100건이다. | V1 공시 목록의 날짜·최종본·전체 페이지·원문 식별자 계약을 확인한다. |
| [OpenDART 공시서류원본파일 API](https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS001&apiId=2019003) | `rcept_no`로 공시 원문을 ZIP 바이너리로 내려받는다. 정상 ZIP이 아닌 응답에는 오류 코드가 올 수 있다. | 사업보고서 RAG에 넣을 실제 원문과 문서 식별자를 확인한다. |
| [OpenDART 단일회사 전체 재무제표 API](https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS003&apiId=2019020) | 정기보고서 기반 단일 회사 재무제표 조회 API를 제공한다. | V1 재무 원천값과 CFS/OFS 데이터 계약을 검증한다. |
| [LangChain Models — Structured output](https://docs.langchain.com/oss/python/langchain/models) | `with_structured_output()`으로 Pydantic 등 스키마에 맞는 구조화 출력을 요청할 수 있고, 원문·파싱 결과를 함께 보존할 수 있다. | LLM이 자유 답변 대신 기업명 검색어·Router 인자를 제한된 형식으로 반환하게 한다. |
| [LangChain Messages](https://docs.langchain.com/oss/python/langchain/messages) | `system` 메시지는 모델의 역할·행동 지침을, `human` 메시지는 사용자 입력을 전달한다. 메시지는 모델 간 공통 형식으로 사용된다. | 같은 Qwen 모델에서 시스템 프롬프트 정책만 바꾸는 검색어 제안 A/B 평가의 입력 경계를 고정한다. |
| [LangChain ChatOllama integration](https://docs.langchain.com/oss/python/integrations/chat/ollama) | `ChatOllama`는 로컬 Ollama 모델의 구조화 출력과 tool calling 연동을 제공한다. | 초기 로컬 Qwen 평가에서 동일한 호출 인터페이스를 사용한다. |
| [LlamaIndex Node Parser](https://developers.llamaindex.ai/python/framework/module_guides/loading/node_parsers/) | 원문 Document를 텍스트 Node로 나누며, Node는 원문 메타데이터를 상속할 수 있다. | 원문 추출 확인 후 chunking 후보를 비교할 때 사용한다. |
| [LlamaIndex Retrieval Evaluation](https://developers.llamaindex.ai/python/framework/understanding/evaluating/evaluating/) | Retrieval 평가는 질문과 정답 Node ID가 있어야 MRR·hit rate 등을 계산할 수 있다. | 사업보고서 근거 문단의 독립 정답을 만든 뒤 검색 방식을 평가한다. |
| [RapidFuzz process 문서](https://rapidfuzz.github.io/RapidFuzz/Usage/process.html) | 문자열 후보 집합에서 유사도 상위 결과를 반환하며 scorer·후보 수·cutoff를 설정할 수 있다. | LLM 없이도 가능한 기업명 오타 후보 생성 기준선으로 사용한다. |

## 사용 원칙

- OpenDART가 제공하는 실제 기업 목록과 `corp_code`가 사실 검증의 기준이다.
- 공시 목록의 `bgn_de`·`end_de`는 **접수일** 기준이다. 재무제표의 사업연도와 같은 뜻으로 쓰지 않는다. 뷰어 링크 `https://dart.fss.or.kr/dsaf001/main.do?rcpNo=<접수번호>`는 공식 가이드의 형식이지만, 링크 형식 검사만으로 실제 페이지 열림을 검증했다고 주장하지 않는다.
- LangChain·ChatOllama는 모델 호출과 출력 형식을 연결하는 도구이며, LLM이 OpenDART의 사실을 대체하지 않는다.
- 패키지 설치·모델 변경·새 API 연결은 각 공식 문서와 현재 환경의 호환성을 다시 확인한 뒤 진행한다.

V1에서 이미 사용한 상세 API 제한과 결정은 [V1 REFERENCES](../../v1/REFERENCES.md)를 함께 본다.
