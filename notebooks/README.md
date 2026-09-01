# Notebooks

이 폴더는 OpenDART 기반 기업 분석 Agent를 단계적으로 학습·실험하는 노트북을 둡니다. 각 노트북은 다음 단계의 기능을 미리 연결하지 않고, 하나의 개념 또는 흐름을 확인하는 범위로 구성합니다.

## 구성

| 파일 | 설명 |
|---|---|
| `01_dart_api.ipynb` | OpenDART API를 직접 호출해 기업명에서 `corp_code`를 찾고, 사업연도별 재무제표 raw JSON과 주요 재무항목을 확인한다. |
| `02_langchain_basics.ipynb` | 로컬 Qwen 모델을 LangChain으로 호출하고, Prompt와 Structured Output의 기본 흐름 및 선택적 OpenAI API 비교를 확인한다. |
| `03_langchain_tool_calling.ipynb` | LLM의 Tool 호출 요청, Python의 실제 Tool 실행, Tool 결과를 받은 최종 답변의 분리된 흐름을 확인한다. |
| `04_opendart_tool_calling.ipynb` | OpenDART 재무 조회 함수를 단일 LangChain Tool로 연결해 실제 기업 재무정보를 조회하는 흐름을 확인한다. |
| `05_langgraph_state_node_edge.ipynb` | 가짜 재무 데이터를 사용해 LangGraph의 State, Node, Edge와 State 갱신 흐름을 확인한다. |
| `06_langgraph_conditional_edge.ipynb` | 가짜 재무 데이터와 사람이 지정한 분석 유형을 사용해 LangGraph Conditional Edge의 경로 선택을 확인한다. |

## 참고

- 학습용 코드는 위에서부터 셀 순서대로 실행한다.
- 노트북의 실행 결과와 학습 메모는 실험 기록이다. 최종 통합 pipeline은 평가와 구조 선택이 끝난 뒤 별도로 구현한다.
