from app.db.dao.MongoUserDAO import MongoUserDAO
from app.schemas.walk_schema import request_schema, response_schema
from app.db.dao.MongoWalkSummaryDAO import MongoWalkSummaryDAO
from app.db.dao.MongoWalkDAO import MongoWalkDataBase
from app.db.dao.MongoWalkPointsDAO import MongoWalkPointsDataBase
from app.core.config import get_settings
from fastapi import HTTPException
from app.services.mongo_filters import check_walk_exists, check_walk_summary_exists
import re

from math import radians, sin, cos, sqrt, atan2
import json
import requests
import datetime

tmap_address_list = ['city_do', 'gu_gun', 'eup_myun', 'ri', 'legalDong', 'adminDong','buildingName', 'buildingDong']


class WalkService:
    def __init__(self, auth, token, chain) -> None:
        self.chain = chain
        self.token = token
        self.auth = auth

    # 채팅 함수
    async def recommend(self, latitude: float, longitude: float, walk_time: int, view: int, difficulty: int):

        #TODO : interface에 의존하게 수정해야함 일단 hotfix
        uuid = self.auth.verify_token(self.token)
        mongo_user_dao = MongoUserDAO(uuid)
        if not await mongo_user_dao.check_user_exists():
            raise HTTPException(status_code=401, detail="invalid-token")


        tmap_app_key = get_settings().tmap_app_key
        start_response = requests.get(
            url=f"https://apis.openapi.sk.com/tmap/geo/reversegeocoding?version={1}&lat={latitude}&lon={longitude}&appKey={tmap_app_key}",
        )
        if start_response.status_code == 204 or start_response.status_code == 400:
            raise HTTPException(status_code=400, detail="invalid-location")

        start_response = start_response.json()

        # print(start_response)
        start_location = start_response["addressInfo"]["fullAddress"] if start_response["addressInfo"]["buildingName"] == "" else start_response["addressInfo"]["fullAddress"] + " " + start_response["addressInfo"]["buildingName"]
        start_response = requests.get(
            url=f"https://apis.openapi.sk.com/tmap/geo/reversegeocoding?version={1}&lat={latitude}&lon={longitude}&appKey={tmap_app_key}",
        )
        print(start_response)
        recom_response = self.chain(
            start_location= start_location,
            walk_time=walk_time,
            view=view,
            difficulty=difficulty)
        # json_response = json.loads(recom_response.replace("\\", ""))
        json_response = recom_response
        response_list = []
        for dest, i in zip(json_response['destinations'], [0, 1, 2]):
            dest_response = requests.get(
                url=f"https://apis.openapi.sk.com/tmap/geo/fullAddrGeo?version=1&fullAddr={dest['name']}&appKey={tmap_app_key}",
            ).json()
            #print("dest_response", dest_response)
            if "error" in dest_response:
                continue
                #raise HTTPException(status_code=501, detail=dest_response['error'])
            else:
                dest_x = dest_response['coordinateInfo']['coordinate'][0]["lon"] if dest_response['coordinateInfo']['coordinate'][0]["lon"] != "" else dest_response['coordinateInfo']['coordinate'][0]["newLon"]
                dest_y = dest_response["coordinateInfo"]['coordinate'][0]['lat'] if dest_response['coordinateInfo']['coordinate'][0]["lat"] != "" else dest_response['coordinateInfo']['coordinate'][0]["newLat"]

                if abs(float(dest_x) - longitude) >= 0.3 or abs(float(dest_y) - latitude) >= 0.3:
                    continue

                route_response = requests.post(f"https://apis.openapi.sk.com/tmap/routes/pedestrian?version=1",
                                               headers={'appKey': tmap_app_key},
                                               data={
                                                   "startX": longitude,
                                                   "startY": latitude,
                                                   "endX": dest_x,
                                                   "endY": dest_y,
                                                   "startName": start_location,
                                                   "endName": dest['address'] + " " + dest['name'],
                                               }
                                         )

                try:
                    # 제어문자 제거 후 파싱
                    cleaned_text = re.sub(r'[\x00-\x1F\x7F]', '', route_response.text)
                    route_response = json.loads(cleaned_text)
                except json.JSONDecodeError as e:
                    continue
                    #print("JSON 파싱 실패:", e)
                    #HTTPException(status_code=500)
                # print(route_response.content)
                #print("route_response", route_response)
                if "error" in route_response:
                    continue
                    #raise HTTPException(status_code=501, detail=route_response['error'])
                else:
                    route_list = []
                    dist = route_response["features"][0]["properties"]["totalDistance"]
                    time = route_response["features"][0]["properties"]["totalTime"]
                    for j in range(len(route_response["features"])):
                        cur_route = route_response["features"][j]
                        if cur_route["geometry"]["type"] == "Point":
                            route_list.append({
                                "latitude": cur_route["geometry"]["coordinates"][1],
                                "longitude": cur_route["geometry"]["coordinates"][0]}
                            )
                        else:
                            for route in cur_route["geometry"]["coordinates"]:
                                route_list.append({"latitude": route[1], "longitude": route[0]})

                    #목적지 address에서 시*도 수준의 이름 제거
                    def delete_sido_name(address: str):
                        sido_name_list = ['서울특별시', '경기도', '인천광역시', '강원특별자치도', '충청남도', '충청북도', '세종특별자치시', '대전광역시', '광주광역시',
                                     '전라남도', '전북특별자치도', '경상북도', '경상남도', '부산광역시', '울산광역시', '대구광역시', '제주특별자치도']
                        for sido in sido_name_list:
                            if sido in address:
                                return address[len(sido) + 1: ]

                    dest_info = {
                        "location": route_list[-1],
                        "start_name": start_location,
                        "name":dest['name'],
                        "address": delete_sido_name(dest['address']),
                        "distance":dist,
                        "walks":dist//0.78,
                        "time":time//60,
                        "routes": route_list
                    }
                    response_list.append(dest_info)
        return response_list
    
    #산책 시작 서비스
    async def walk_start(self, request = request_schema.PostStartWalkReqDTO):
        uuid = self.auth.verify_token(self.token)

        user_has_walk = await MongoWalkDataBase().check_user_has_walked(uuid = uuid)
        print(user_has_walk)
        if user_has_walk:
            latest_walk_id = await MongoWalkDataBase().get_latest_walk(uuid = uuid)
            is_no_stored_walk_existed = await MongoWalkSummaryDAO().check_walk_exists(walk_id = latest_walk_id)

            if is_no_stored_walk_existed:
                save_latest_walk_request = request_schema.PatchSaveWalkReqDTO(
                    walk_id = str(latest_walk_id),
                    mood = 0,
                    difficulty = 0,
                    memo = ""
                )

                await MongoWalkSummaryDAO().create_walk_summary(latest_walk_id, 0, 0)
                await MongoWalkSummaryDAO().patch_walk(save_latest_walk_request)

        walk_input = {
            "user_id": uuid,
            "start_name": request.start_name,
            "end_name": request.end_name,
            "end_address": request.end_address,
        }
        walk_id = await MongoWalkDataBase().post_start_walk(uuid = uuid, request=walk_input)
        walk_point_input = {
            "walk_id": walk_id,
            "location": request.start_location,
        }
        await MongoWalkPointsDataBase().create_walk_point(request=walk_point_input)

        return str(walk_id)

    async def walk_location(self, request = request_schema.PostLocationReqDTO):
        uuid = self.auth.verify_token(self.token)
        response = await MongoWalkPointsDataBase().post_walk_point(request=request)
        return response

    @check_walk_exists
    async def post_walk_end(self, walk_id:str, time:int, distance:float):
        await MongoWalkSummaryDAO().create_walk_summary(walk_id, time, distance)
        return True

    async def patch_end(self, request = request_schema.PatchSaveWalkReqDTO):
        await MongoWalkSummaryDAO().patch_walk(request)
        return True

    @check_walk_exists
    async def get_walk_summary(self, walk_id) -> response_schema.GetWalkEndDTO:
        points = await MongoWalkPointsDataBase().get_all_points(walk_id)
        walk_info = await MongoWalkDataBase().get_walk(walk_id)

        len_data = len(points)
        time_diff = datetime.datetime.now() - walk_info.created_at
        time_diff = int(time_diff.total_seconds() // 60)
        dist = 0

        def haversine(lat1, lon1, lat2, lon2):
            R = 6371000  # Earth radius in meters
            dlat = radians(lat2 - lat1)
            dlon = radians(lon2 - lon1)
            a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            return R * c

        for i in range(len_data - 1):
            lon1, lat1 = points[i]["location"]
            lon2, lat2 = points[i + 1]["location"]
            dist += haversine(lat1, lon1, lat2, lon2)

        start_name, end_name = walk_info.start_name, walk_info.end_name
        return response_schema.GetWalkEndDTO(
            start_name=start_name,
            end_name=end_name,
            distance=dist,
            time=time_diff,
        )
