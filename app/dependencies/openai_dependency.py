from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

from app.core.config import settings

openai_api_key = settings.openai_api_key

def get_openai_client():
    llm = ChatOpenAI(
        temperature = 0,
        openai_api_key=openai_api_key,
        model_name = "gpt-4o-mini"
    )
    template =  """
        당신은 산책 코스를 추천하는 전문가입니다.

        주어진 입력값을 기반으로, 산책 목적지 3곳을 선정해 주세요:

        - 입력값:
            - 풍경 {view}: 0을 기준으로, 클수록 자연환경에 가깝고 작을수록 도시 환경에 가깝습니다.
            - 산책 강도 {difficulty}: 0을 기준으로, 클수록 운동량이 높고 힘든 코스, 작을수록 평탄하고 편안한 코스입니다.
            - 산책 출발지 {start_location}: 산책 출발지 주변을 우선으로 목적지를 조회합니다.
            - 산책 시간 {walk_time}: 산책 출발지로부터 해당 시간(분) 내외로 도달할 있는 목적지를 추천합니다.
        
        - 작업 흐름:
            1. 출발지 주소를 기반으로 목적지를 조회합니다.
            2. 산책 출발지 좌표 주위의 목적지를 검색하고, 입력된 view와 difficulty에 맞춰 필터링합니다.
            3. walk_time에 맞는 거리(평균 걷기 속도 4~5km/h 고려)로 목적지를 선택합니다.
        
        - 결과물 형식(JSON):
            아래와 같은 형태로, 3개의 목적지를 배열로 반환해 주세요. 추가 설명 없이 JSON만 출력합니다 ```json도 빼주세요.

            {{"destinations": [{{"name": string,"address": string}},{{"name": string,"address": string}},{{"name": string,"address": string}}]}}
        
            - 주의사항:
            - 꼭 위의 JSON 포맷을 지켜 주세요.
            - 꼭 지도에 있는 목적지만 추천해주세요. 구글 지도에 나와있는 지명으로 나타내주세요.
        """
    prompt = PromptTemplate.from_template(template)
    chain = prompt | llm | StrOutputParser()
    return chain

