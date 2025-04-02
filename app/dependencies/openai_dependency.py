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
        풍경 {view}, 산책 강도 {difficulty}를 고려하여 
        풍경은 0을 기준으로 클수록 자연환경, 작을수록 도시에 가깝다는 것을 의미해.
        산책 강도는 0을 기준으로 클수록 힘들고 운동이 되는 강도, 작을수록 평탄하고 편안한 강도를 의미해.
        현재 위도 {latitude}와 경도 {longitude}에서 
        산책 시간 {walk_time}분 만큼 걸리는 산책 목적지를 3개 선정해줘.

        선정한 3곳을 아래 형태로 json만 반환해줘.
            {{
                [
                    {{
                        "latitude": float,
                        "longitude": float,
                        "name": string,
                        "address": string,
                        "distance": double,
                        "walks": int,
                        "time": int,
                        "imgUrl": string
                    }},
                    {{
                        "latitude": float,
                        "longitude": float,
                        "name": string,
                        "address": string,
                        "distance": double,
                        "walks": int,
                        "time": int,
                        "imgUrl": string
                    }},
                    {{
                        "latitude": float,
                        "longitude": float,
                        "name": string,
                        "address": string,
                        "distance": double,
                        "walks": int,
                        "time": int,
                        "imgUrl": string
                    }}
                ]
            }}

    """
    prompt = PromptTemplate.from_template(template)
    chain = prompt | llm | StrOutputParser()
    return chain

