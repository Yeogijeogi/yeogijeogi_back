from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, Tool, AgentType
from langchain_community.tools.tavily_search.tool import TavilySearchResults
from langchain.memory import ConversationBufferMemory

from app.core.config import settings

openai_api_key = settings.openai_api_key
tavily_api_key = settings.tavily_api_key


def get_openai_client():
    # Create a search tool with more specific parameters
    search_tool = TavilySearchResults(
        tavily_api_key=tavily_api_key,
        k=5,  # Limit results to prevent excessive searching
        max_results=5
    )

    tools = [
        Tool.from_function(
            func=search_tool.run,
            name="Search",
            description="출발지 주변 목적지 및 산책 코스 정보를 검색할 수 있는 실시간 웹 검색 도구. 한 번만 사용해야 합니다."
        )
    ]

    # Use a more capable model to prevent repeated searches
    llm = ChatOpenAI(
        temperature=0,
        openai_api_key=openai_api_key,
        model_name="gpt-4o-mini"
    )

    # Using structured agent format with clearer instructions
    template = """
    당신은 산책 코스를 추천하는 전문가입니다.

    산책 목적지를 찾을 때 다음 중요 사항을 따르세요:
    1. 검색은 딱 한 번만 수행하세요. 반복 검색은 금지됩니다.
    2. 같은 검색어를 두 번 사용하지 마세요.
    3. 검색 후에는 즉시 결과를 분석하고 최종 응답을 생성하세요.
    4. 반드시 정확히 3개의 목적지를 추천해야 합니다. 2개나 4개가 아닌 정확히 3개여야 합니다.
    5. 가장 중요한 것은 제시된 산책 시간({walk_time}분)을 엄격히 지켜야 한다는 것입니다.

    주어진 입력값:
    - 풍경 지수 {view}: 0을 기준으로, 클수록 자연환경에 가깝고 작을수록 도시 환경에 가깝습니다.
    - 산책 강도 {difficulty}: 0을 기준으로, 클수록 운동량이 높고 힘든 코스, 작을수록 평탄하고 편안한 코스입니다.
    - 산책 출발지 {start_location}: 산책 출발지 주변을 우선으로 목적지를 조회합니다.
    - 산책 시간 {walk_time}: 분(minutes) 단위로 주어지고 산책 출발지로부터 해당 시간(분) 내외로 걸어서 도달할 있는 목적지를 추천합니다.

    작업 단계:
    1. "{start_location} 주변 산책 명소" 또는 "{start_location} 주변 {walk_time}분 산책 코스"와 같은 검색어를 한 번만 사용하세요.
    2. 검색 결과에서 '무조건 3개'의 목적지를 선택하고 즉시 JSON 형식으로 답변하세요.
    3. 검색을 반복하지 마세요.
    4. 충분한 결과가 없더라도 반드시 3개의 목적지를 반환해야 합니다.

    결과물 형식:
    아래 형식의 JSON만 출력하세요. 추가 설명이나 사고 과정은 포함하지 마세요.
    {{"destinations": [
      {{"name": "장소명1", "address": "주소1"}}, 
      {{"name": "장소명2", "address": "주소2"}}, 
      {{"name": "장소명3", "address": "주소3"}}
    ]}}

    중요: 반드시 정확히 3개의 목적지를 포함해야 하며, 그 이상도 그 이하도 안 됩니다.
    """

    prompt = PromptTemplate.from_template(template)

    # Use ZERO_SHOT_REACT_DESCRIPTION agent for more predictable behavior
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        max_iterations=3,  # Limit the number of steps to prevent infinite loops
        early_stopping_method="generate"  # Force stop if hitting iteration limit
    )

    def run_chain(view, difficulty, start_location, walk_time):
        filled_prompt = prompt.format(
            view=view,
            difficulty=difficulty,
            start_location=start_location,
            walk_time=walk_time
        )

        # Create a focused search query directly in the prompt
        search_query = f"{start_location} 주변 {walk_time}분 산책 코스 추천"

        try:
            # First perform a single search to get results
            search_results = search_tool.run(search_query)

            # Format the prompt with search results included
            final_prompt = f"""
            {filled_prompt}

            다음은 검색 결과입니다. 이 결과를 바탕으로 정확히 3곳의 목적지를 선택하세요:
            {search_results}

            반드시 3개의 목적지를 포함하는 JSON을 반환해야 합니다. 2개나 4개가 아닌 정확히 3개의 목적지를 포함해야 합니다.
            결과가 충분하지 않더라도 반드시 3개의 목적지를 찾아서 반환하세요. 필요하다면 기존 결과를 바탕으로 적절한 목적지를 추론하여 포함하세요.

            모든 목적지는 다음 JSON 형식을 정확히 따라야 합니다:
            {{"destinations": [
              {{"name": "장소명1", "address": "주소1"}}, 
              {{"name": "장소명2", "address": "주소2"}}, 
              {{"name": "장소명3", "address": "주소3"}}
            ]}}
            """

            # Use the agent for the final processing only
            response = llm.invoke(final_prompt)

            # 결과 검증: JSON에 정확히 3개의 목적지가 포함되어 있는지 확인
            try:
                import json
                import re

                # 응답에서 JSON 부분만 추출하기 위한 시도
                content = response.content

                # 결과가 JSON 형식인지 확인하고, 아니라면 JSON으로 변환 시도
                result_dict = json.loads(content)
                # except:
                #     # JSON이 아닌 경우, JSON 형식을 찾아보기
                #     json_match = re.search(r'\{.*"destinations".*\}', content, re.DOTALL)
                #     if json_match:
                #         try:
                #             result_dict = json.loads(json_match.group(0))
                #         except:
                #             # 여전히 파싱 실패하면 직접 형식 만들기
                #             result_dict = {"destinations": []}
                #     else:
                #         # JSON 형식이 없으면 직접 파싱해보기
                #         result_dict = {"destinations": []}
                #
                # # 목적지가 없거나 3개가 아닌 경우 처리
                # if "destinations" not in result_dict or len(result_dict["destinations"]) != 3:
                #     # 결과가 부족하면 강제로 3개로 맞추기
                #     destinations = result_dict.get("destinations", [])
                #
                #     # 기존 목적지가 있으면 유지
                #     while len(destinations) < 3:
                #         placeholder_num = len(destinations) + 1
                #         destinations.append({
                #             "name": f"추천 장소 {placeholder_num}",
                #             "address": f"{start_location} 인근 {walk_time}분 거리 내 위치"
                #         })
                #
                #     # 3개를 초과하면 3개로 줄이기
                #     if len(destinations) > 3:
                #         destinations = destinations[:3]
                #
                #     result_dict["destinations"] = destinations
                #
                #     # 최종 결과를 JSON 문자열로 변환
                #     final_result = json.dumps(result_dict, ensure_ascii=False)
                #     return {"content": final_result}

                return result_dict
            except Exception as e:
                # 오류 발생 시 3개의 기본 목적지를 반환
                fallback = {
                    "destinations": [
                        {"name": f"{start_location} 인근 공원", "address": f"{start_location} 인근"},
                        {"name": f"{start_location} 근처 산책로", "address": f"{start_location} 인근"},
                        {"name": f"{start_location} 주변 명소", "address": f"{start_location} 인근"}
                    ]
                }
                return {"content": json.dumps(fallback, ensure_ascii=False)}
        except Exception as e:
            return {"error": str(e)}

    return run_chain