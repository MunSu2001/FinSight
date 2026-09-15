# V1 Experiment Reports

이 폴더에는 V1의 실제 비교 실험이 끝난 뒤 결과 보고서를 저장한다. 아직 실행하지 않은 실험의 예상 결과나 결론은 기록하지 않는다.

## 보고서 작성 단위

비교 대상 하나당 `NN_topic.html` 파일을 만든다. 예시는 다음과 같다.

- `13_llm_entity_search_expansion.html`
- `14_llm_entity_search_prompt_comparison.html`
- `20_filing_rag_retrieval.html`

`NN`은 해당 결과를 만든 notebook의 번호와 같아야 한다. 따라서 `notebooks/v1/13_llm_entity_search_expansion.ipynb`의 실제 결과는 `13_llm_entity_search_expansion.html`에 기록한다.

## 현재 V1 보고서 순서

| Notebook | 보고서 | 평가 대상 |
|---|---|---|
| 05 | `05_entity_resolution_baseline.html` | 기업 식별 기준선 |
| 06 | `06_entity_resolution_index_benchmark.html` | 전수 탐색과 인덱스 탐색 |
| 07 | `07_entity_resolution_fuzzy_candidates.html` | fuzzy 후보 생성 |
| 08 | `08_entity_resolution_confirmation_policy.html` | 자동 확정과 사용자 확인 정책 |
| 09 | `09_entity_not_found_policy.html` | 초기 NOT_FOUND 정책 |
| 10 | `10_entity_candidate_composition.html` | 후보 구성 A/B/C |
| 11 | `11_entity_confirmation_with_union_candidates.html` | 통합 후보 기반 확인 정책 |
| 12 | `12_not_found_cutoff_with_interpretation_policy.html` | cutoff grid |
| 13 | `13_llm_entity_search_expansion.html` | LangChain LLM 검색어 확장 |
| 15 | `15_llm_entity_reasoning_disabled.html` | Thinking 비활성화 + Schema grounding LLM 검색어 확장 |
| 16 | `16_llm_entity_prompt_detail_comparison.html` | 상세 Prompt LLM 검색어 확장 A/B 비교 |

## 각 보고서의 필수 내용

1. **목적과 가설**: 무엇을 선택하거나 확인하려는 실험인지
2. **비교 후보**: Prompt, Tool 설명, workflow, retrieval 방식, 모델 등 비교한 조건
3. **실행 조건**: 평가셋 구분, 데이터 기준일, 코드 커밋, 모델·양자화·temperature, 하드웨어
4. **평가 지표**: 선택한 지표와 해당 지표가 필요한 이유
5. **결과**: 원시 결과 위치와 집계 표
6. **해석**: 지표 차이가 무엇을 의미하는지, 실패 사례는 무엇인지
7. **채택·미채택 결정**: 비교한 모든 후보의 채택 또는 미채택 여부, 각각의 이유와 감수한 trade-off. 최종 확정이 이르면 `조건부 채택` 또는 `보류`와 남은 검증을 명시
8. **비용·성능**: 측정 가능한 경우 p50/p95 latency, 오류율, 모델 파일 크기, VRAM/RAM peak, cold/warm 실행 시간, API 비용 또는 토큰 사용량
9. **한계와 다음 실험**: 평가셋의 한계, 재현 조건, 남은 검증 항목

## 비용·인프라 기록 원칙

- 로컬 모델은 모델명·양자화, 모델 파일 크기, 하드웨어, VRAM/RAM peak, cold/warm 지연시간을 기록한다.
- API 모델은 모델명, 입력·출력 토큰, 호출 수, 실행 시점의 가격 기준과 추정 비용을 기록한다.
- 품질 기준을 통과하지 못한 후보는 비용이 낮아도 최종 후보로 채택하지 않는다.
- 모든 실험에서 자원을 측정할 필요는 없다. 모델·workflow·retrieval 후보처럼 성능 또는 비용 선택에 영향을 주는 비교에만 기록한다.
