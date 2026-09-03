# V1 평가 계획

## 1. 평가 목적

V1 평가는 LLM 답변의 자연스러움만 보지 않는다. FinSight가 질문에 맞는 조사 경로를 선택하고, OpenDART 수치·계산·사업보고서 근거를 정확히 연결하는지를 측정해 최종 workflow를 선택하는 것이 목적이다.

평가 결과는 Prompt, Router·Tool 설계, 기간 Resolver, RAG 방식, Validator, workflow와 모델 후보의 선택 근거로 사용한다.

## 2. 평가 원칙

- 실제 비교는 동일한 평가셋·데이터 기준일·모델 설정에서 A vs B로 수행한다.
- Router, RAG, Validator, workflow를 한 실험에서 동시에 바꾸지 않는다.
- 핵심 품질 지표에서 명확히 우세한 후보만 채택한다.
- 지표별 우열이 갈리면 결과를 보류하고 실패 사례·사용 시나리오·비용을 추가 검토한다.
- 비용·지연시간·자원 사용량은 품질이 동등하거나 비열등한 후보의 선택 근거로만 사용한다.
- 실제 후보 비교 전에는 임의의 합격선이나 최종 후보를 정하지 않는다.

## 3. 평가 질문과 정답 계약

### 질문 범주

1. 단일 기업·단일 사업연도 재무 조회
2. 단일 기업 다년도 재무 추세와 계산
3. 다기업 다년도 비교와 공통 사업연도 선택
4. 기업·기간 조건 공시 목록 조회
5. 사업보고서 원문 근거 검색
6. 재무 수치와 사업보고서 근거를 함께 요구하는 복합 질문
7. 모호한 기업명, 금융업, 데이터 부재, 지원하지 않는 투자 추천 등 경계 질문

### 사례별 정답 정보

- 질문 원문
- 정답 기업명·`corp_code`·상장 상태·비금융 판정·요청 데이터 가용성
- 정답 사업연도·결산일·다기업 공통 연도
- 기대 Tool 집합과 인자
- 정답 원천 수치·재무제표 기준·계산 결과
- 정답 공시 목록 조건 또는 사업보고서 근거 문단·접수번호
- 허용 답변 범위, 제한 문구, 금지 주장
- 데이터 조회 기준일과 원문 링크

### 개발/holdout 분리

- 개발 세트는 후보 비교에 사용한다.
- holdout은 선택한 최종 후보를 한 번 확인하고 이후 회귀 기준으로 사용한다.
- 같은 사업보고서, 같은 접수번호 또는 거의 같은 질문이 개발과 holdout에 겹치지 않도록 분리한다.
- 사례 수·기업·업종 분포·반복 횟수는 실제 정답 근거를 수집한 뒤 사용자와 합의한다.

## 4. 평가 대상과 지표

| 대상 | 설계 또는 비교 대상 | 핵심 지표 |
|---|---|---|
| 기업 식별·대상 판정 | 기업명 해석, `corp_code`, 복수 후보 확인, 상장 상태·비금융·데이터 가용성 판정 | Entity Accuracy, Candidate Recall@K, Unsafe Selection Rate, Abstention Accuracy |
| 기간 Resolver | 명시 연도, 최근 N년, 다기업 공통 사업연도 정책 | Period Exact Match, Common-Year Validity, Limitation Accuracy |
| 재무 데이터 계약 | 계정 매핑, CFS 우선/OFS 대체, 단위·결측 처리 | Field Accuracy, Statement-Basis Accuracy, Missing-data Handling Accuracy |
| 계산 | 공식·단위·위험 계산 처리 | Calculation Accuracy, Unsafe-calculation Rate |
| Router·Tool | Prompt, structured schema, Tool 설명, 분기 방식 | Route Exact Match, Tool Precision/Recall/F1, Argument Exact Match, Over-call Rate, Invalid-plan Rate |
| 공시 목록 | 기간·최종 제출본·원문 식별자 정책 | Date-filter Accuracy, 목록 Precision/Recall, 링크·접수번호 Accuracy |
| 사업보고서 RAG | 파싱, chunking, embedding, retrieval, reranker | Passage Recall@K, MRR, nDCG@K, Citation Retrieval Recall, 검색 지연시간 |
| 근거·답변 검증 | 규칙 기반·모델 기반 Validator 후보 | Numeric Faithfulness, Citation Correctness, Claim Support Precision, Unsupported Claim Rate, Limitation Accuracy |
| end-to-end workflow | 조건부 실행, Validator 유무, 기준선 workflow | Task Completion Rate, Evidence-complete Task Rate, E2E Error/Partial-result Rate, 핵심 품질 지표 |
| 운영 성능 | 품질 비열등 후보의 모델·workflow | p50/p95 Latency, Tool-call Count, Error Rate, VRAM/RAM Peak, cold/warm 시간 |

공시 목록은 기간 조건으로 반환되는 데이터이므로 RAG 지표를 적용하지 않는다. Recall@K, MRR, nDCG@K는 순위가 있는 사업보고서 passage retrieval에만 적용한다.

## 5. 후보 비교 설계

### 5.1 데이터 계약과 계산

이 단계는 후보 선택보다 정답 기반을 검증하는 단계다. 상장·비상장 비금융 기업과 여러 업종·연도에서 계정 매핑, CFS/OFS 대체, 단위, 결측과 계산 예외를 확인한다. 비상장 기업의 요청 재무·사업보고서 데이터 부재는 별도 정답 상태로 기록한다. 이 기반이 불안정하면 이후 Router·RAG·workflow 점수는 해석하지 않는다.

### 5.2 Router·Tool·기간 해석

Prompt·구조화 스키마·Tool 설명·분기 방식 후보를 비교한다. 실제 가용 사업연도 선택은 LLM이 아니라 기간 Resolver가 담당하며, Router는 `최근 N년` 같은 제약을 구조화하는 역할만 맡는다.

### 5.3 사업보고서 RAG

문서 파싱과 chunking을 먼저 비교하고, 선택된 문서 단위에서 retrieval과 reranker 후보를 비교한다. 조합 폭발을 피하기 위해 모든 후보를 한 번에 교차하지 않는다.

### 5.4 Validator와 workflow ablation

앞 단계에서 선택된 Tool·RAG 후보를 고정한 뒤 workflow 구조만 비교한다.

최소 기준선 후보는 아래와 같다.

1. 필요한 Tool만 조건부 실행, Validator 없음
2. 필요한 Tool만 조건부 실행, Validator 있음
3. 모든 Tool을 항상 실행

3번은 최종안 후보가 아니라, 조건부 Routing이 품질·비용에 실제로 기여하는지 확인하는 기준선이다. 자동 재검색·재계획·병렬 실행은 이 비교 결과와 필요성이 확인되기 전에는 추가하지 않는다.

## 6. 평가 순서

```text
평가 질문·정답·근거 데이터 계약 확정
→ 데이터 계약·재무·계산 기준선 확인
→ Router·Tool·기간 Resolver 후보 비교
→ 공시 목록 정책 확인 및 사업보고서 RAG 후보 비교
→ Validator 후보 비교
→ workflow ablation
→ holdout end-to-end 평가
→ 최종 통합 구현 승인 여부 결정
```

새 Tool, RAG 경로 또는 workflow 분기를 추가하면 해당 기능 평가뿐 아니라 기존 holdout end-to-end 회귀 평가를 다시 수행한다.

## 7. 실행 기록과 보고서

실제 비교 실험에는 데이터 기준일, 원문 접수번호, 코드 커밋, Prompt 버전, 모델·양자화·temperature, context 길이, 하드웨어를 기록한다.

- 확률적 모델은 반복 실행하여 median과 p95를 기록한다.
- 로컬 모델은 cold/warm 지연시간, 모델 파일 크기, VRAM/RAM peak를 기록한다.
- 모델 로드·인덱스 생성 시간과 질의 처리 시간은 분리한다.
- 실제 비교 결과는 `docs/v1/reports/`에만 기록한다.

평가셋, 실행 manifest, 원시 결과의 세부 폴더 구조는 실제 실험을 시작하기 전에 목적·후보·지표와 함께 사용자에게 별도로 제안하고 합의한 뒤 만든다.
