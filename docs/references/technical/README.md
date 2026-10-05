# 기술 레퍼런스

확인일: 2026-10-03

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

## V1-26 청킹 비교 레퍼런스 (2026-10-03 확인)

| 자료 | 확인한 사실 | FinSight에서의 활용 |
|---|---|---|
| [LlamaIndex Node Parser Usage Pattern](https://developers.llamaindex.ai/python/framework/module_guides/loading/node_parsers/) | `SentenceSplitter`는 `Document`를 Node 청크로 나누며 `chunk_size`와 `chunk_overlap`을 지정할 수 있다. | 같은 크기·겹침 설정에서 제목 경계 선분할 여부만 비교한다. |
| [LlamaIndex Retrieval Evaluation](https://developers.llamaindex.ai/python/framework/understanding/evaluating/evaluating/) | 검색 평가에는 질문과 정답 Node ID가 필요하며, MRR·hit rate 등의 평가 예제를 제공한다. | V1-26은 청킹마다 Node ID가 달라지므로 원문에서 확인한 인용문을 공통 정답으로 두고 Hit@K·MRR@K를 직접 계산한다. |
| [scikit-learn HashingVectorizer](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.HashingVectorizer.html) | 이 변환기는 학습이 필요 없는(stateless) 문자 n-gram 벡터와 L2 정규화를 제공한다. | V1-26에서 청킹 외 검색 조건을 고정할 어휘 검색 기준선으로 사용한다. 의미 기반 임베딩 검색 성능을 대신하지 않는다. |

V1-26의 정답 인용문은 OpenDART 공시서류원본파일 API로 실제 두 사업보고서 XML에서 확인했다. 문장별 고유성은 같은 B 추출 텍스트에서 각각 1회 출현하는지 점검한다. 이는 작은 개발셋의 근거이며 독립 holdout은 아니다.

## V1-27 사업보고서 검색 비교 레퍼런스 (2026-10-05 확인)

| 자료 | 확인한 사실 | FinSight에서의 활용 |
|---|---|---|
| [multilingual-E5-small 모델 카드](https://huggingface.co/intfloat/multilingual-e5-small) | 다국어 임베딩 모델이며 검색에는 질문에 `query: `, 문서에 `passage: ` 접두어를 붙인다. 입력은 최대 512 token까지 처리한다. 모델 라이선스는 MIT이고 safetensors 가중치는 약 471 MB다. | 26번과 동일한 B 청크에서 의미 기반 dense 검색 기준선을 만든다. CPU에서 사용하고 잘린 청크 수를 기록한다. 이 모델의 성능이 모든 임베딩 모델을 대표하지는 않는다. |
| [LlamaIndex 순위 결합 예제](https://developers.llamaindex.ai/python/examples/low_level/fusion_retriever/) | 벡터 검색과 어휘 검색 결과를 Reciprocal Rank Fusion(RRF)으로 결합할 수 있다. | 점수 척도가 다른 어휘·dense 검색의 상위 순위를 결합하는 첫 하이브리드 기준선으로 사용한다. |
| [scikit-learn HashingVectorizer](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.HashingVectorizer.html) | 문자 n-gram을 상태 없는 희소 벡터로 변환할 수 있다. BM25나 학습된 의미 임베딩은 아니다. | 26번의 어휘 검색기를 그대로 유지해 벡터·하이브리드와 비교한다. |

V1-27의 실제형 질문 6개는 26번에서 확인한 같은 근거 6개를 다른 사용자 표현으로 재질문한 것이다. 평가에 도움은 되지만 새로운 문서·독립 근거가 추가된 holdout으로 간주하지 않는다.

### V1-27 후속 어휘 검색 비교 레퍼런스 (2026-10-05 확인)

| 자료 | 확인한 사실 | FinSight에서의 활용 |
|---|---|---|
| [SQLite FTS5 공식 문서](https://www.sqlite.org/fts5.html#the_bm25_function) | FTS5는 내장 `bm25()` 순위 함수를 제공한다. 반환 점수는 낮을수록 관련성이 높고, `rank`로 정렬할 수 있다. | 새 패키지 없이 같은 사업보고서 청크에서 한국어 BM25 어휘 검색 기준선을 만든다. |
| [Kiwi 형태소 분석 API](https://bab2min.github.io/kiwipiepy/) | `Kiwi.tokenize()`가 한국어를 형태소와 품사로 나눈다. | 조사·어미를 제외한 핵심 형태소를 FTS5 입력 토큰으로 사용한다. 선택한 품사 집합 자체도 검색 품질에 영향을 줄 수 있으므로 현재 비교의 조건으로 기록한다. |

문자 n-gram과 형태소 BM25는 토큰 단위와 점수식이 함께 다르다. 후속 비교는 두 **어휘 검색 구성 전체**의 우열만 해석하며 BM25 점수식의 독립 효과로 해석하지 않는다. FTS5 실험용 테이블은 XML의 재무·사업 필드를 구조화한 DB가 아니다.

## V1-29 Weighted RRF 비교 (2026-10-05 확인)

| 자료 | 확인한 사실 | FinSight에서의 활용 |
|---|---|---|
| [LangChain EnsembleRetriever 공식 구현](https://github.com/langchain-ai/langchain/blob/master/libs/langchain/langchain_classic/retrievers/ensemble.py) | 검색기별 `weights`와 순위 완화 상수 `c`를 사용해 Weighted RRF로 순위를 결합한다. | E5·BM25 가중치만 변경하는 notebook 함수의 수식 근거. 현재 실험에서 이 클래스를 호출하는 것은 아니다. |
| [Elastic RRF 공식 문서](https://www.elastic.co/docs/reference/elasticsearch/rest-apis/reciprocal-rank-fusion) | `rank_constant`는 순위별 기여 차이를, `rank_window_size`는 결합할 후보 범위를 조절한다. 이 페이지의 구현은 검색기에 동일 가중치를 준다. | 결합 가중치와 후보 수·순위 상수를 구분하고 이번에는 후보 20·상수 60을 고정한다. |

추가 개발 질문은 [NAVER 공식 IR](https://www.navercorp.com/investment/irReports)의 2024 사업보고서, [LG생활건강 공식 사업보고서](https://www.lghnh.com/ir/business_report.jsp)의 2024 보고서, [HDC 공식 공고](https://www.hdc-holdings.com/ko/ir/disclosure/notice/view?fromNotice=true&inIdx=6)의 2024 보고서를 읽고 검색 실행 전에 작성했다. 공식 IR PDF는 정답 수집 근거이며, 검색 입력은 기존 OpenDART XML로 유지한다. 실제 XML·청크에도 인용문이 존재하는지 실행 시 확인해야 한다.

29번은 5기업·5개 2024 보고서·25개 **개발 질문**이다. 기업별 2개 연도나 독립 holdout을 확보한 것으로 표현하지 않는다. 비율 후보는 E5:BM25 = 10:0 / 7:3 / 5:5 / 3:7 / 0:10이며, 정답은 제한된 인용문 기반이므로 전체 관련 근거에 대한 완전한 relevance 판정이 아니다.

## V1-30 Parent-child 청킹 비교 (2026-10-05 확인)

| 자료 | 확인한 사실 | FinSight에서의 활용 |
|---|---|---|
| [LlamaIndex HierarchicalNodeParser 공식 API](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/hierarchical/) | 계층별 parser로 재귀 분할하며 부모·자식 Node 관계를 만든다. `node_parser_ids`와 `node_parser_map`으로 계층별 SentenceSplitter를 지정할 수 있다. | 설치된 `llama-index-core 0.14.25`의 구현도 확인했다. 모든 계층에 E5 tokenizer를 명시해 부모 1,200·자식 400·overlap 48 후보를 만든다. 큰 부모는 E5에 넣지 않는다. |
| [LlamaIndex Auto Merging 공식 예제](https://developers.llamaindex.ai/python/framework/integrations/retrievers/auto_merging_retriever/) | leaf Node를 검색 인덱스에 넣고 부모 문맥은 별도로 보존한다. 예제의 AutoMergingRetriever는 검색된 자식 집합을 임계값에 따라 부모로 병합한다. | 작은 자식 검색과 큰 문맥 반환을 구분하는 구조의 근거다. 30번은 해당 임계값 병합 클래스를 사용하지 않고 상위 자식 5개의 부모를 직접 가져와 중복 제거한다. |

사용자가 승인한 E5:BM25 = 5:5를 **후속 비교 기준선**으로 고정한다. 최종 운영 검색기까지 확정했다는 뜻은 아니다. A/B는 같은 제목 섹션에서 시작하며, 부모→자식 순서의 재분할과 부모 확장을 함께 비교하므로 확장만의 독립 효과라고 표현하지 않는다. 반환 문맥의 크기가 달라 제한 없는 결과와 공통 2,400 E5-token 예산 결과를 나눈다. 정답은 동일 인용문 ID 기준이고, 기존 개발 질문 25개와 기존 근거를 묶은 복합 질문 5개를 분리한다. 해당 크기·예산은 이번 실험 가정이며 공식 문서가 권고한 최적값은 아니다.

### 원문 제목 계층 후보 C 추가 (2026-10-06 확인)

- [NVIDIA의 청킹 비교 실험](https://developer.nvidia.com/blog/finding-the-best-chunking-strategy-for-accurate-ai-responses/)은 token/page/section 구성을 비교했고, 금융 문서끼리도 데이터셋·질문 특성에 따라 최적 크기·방식이 달라졌다고 보고했다. FinSight의 B가 C보다 좋다는 직접 근거는 아니며, 문서 구조 기반 방식이 항상 우세하다고 가정하지 않고 기존 토큰 후보를 유지하는 근거로만 사용한다. PDF·추출 모델·검색 및 생성 구성도 달라 해당 수치를 우리 XML retrieval 점수로 옮기지 않는다.
- [OpenDART 공시서류 원본파일 API 공식 가이드](https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS001&apiId=2019003)는 접수번호별 원본 XML 파일을 제공한다. 가이드 자체가 모든 XML의 제목 스키마를 보장한다고 해석하지 않는다.
- 같은 API로 삼성전자 `20250311001085`, 리노공업 `20250318000229`, LG생활건강 `20250317000790`의 XML을 읽기 전용 조회하고 기존 보정·`lxml-xml` 파서로 구조를 확인했다. 파싱된 트리에서 삼성전자는 SECTION-1 3개/SECTION-2 12개, 리노공업은 14/36/SECTION-3 2개, LG생활건강은 14/37/SECTION-3 2개가 관찰됐다. TITLE은 SECTION 안에 중첩돼 있었고 제목의 ATOCID도 확인했다. 이 개수는 현재 파서의 관찰 결과이지 원본 전체의 무손실성 검증이나 모든 보고서에 대한 스키마 규약이 아니다.
- C는 SECTION 중첩을 제목 수준의 근거로 사용하고 SUBTITLE은 해당 SECTION의 TITLE 하위로 처리한다. XML 제목 이벤트와 기존 B 텍스트의 제목 경계 수·본문 보존을 검사하며, 제목 계층이 없거나 불일치하면 중단한다. 텍스트 번호 패턴으로 없는 계층을 만들어내지 않는다.
- 자연 제목 구간은 E5 입력 한도 안이면 그대로 검색한다. 한도를 넘는 본문만 400-token 안전 조각으로 나누되 부모는 원래 상위 제목 구간으로 유지한다. 하위 제목이 있는 내부 노드의 직접 본문은 그 내부 노드 전체 문맥으로 연결한다. 하위 제목이 없는 자연 leaf는 실제 상위 제목 전체로 연결하며 최상위 독립 제목은 자기 문맥으로 연결한다. 예를 들어 `연회비→국내/해외`에서 국내 구간을 검색하면 국내만이 아니라 연회비 전체를 반환한다. 따라서 **원문 계층 + 임베딩 길이 안전 분할** 후보이며 모든 조각이 제목 하나와 일대일이라는 뜻은 아니다.
- 원래 제목 부모가 공통 예산보다 크면 현재 통째 반환 정책으로 담지 못한다. 무제한 근거 Recall, 예산 Recall, 첫 부모 예산 초과 비율을 함께 해석하고 예산 부적합을 제목 검색 실패와 구분한다. 세 후보 모두 같은 추출 본문·질문·정답·5:5 검색기를 사용하고 부모를 임베딩하지 않는다.
