from pydantic import BaseModel

class GetUserResDTO(BaseModel):
    walk_distance: float # 사용자가 산책한 총 거리 (km 단위)
    walk_time: int # 사용자가 산책한 총 시간 (분 단위)