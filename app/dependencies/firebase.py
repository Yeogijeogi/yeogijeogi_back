from fastapi import HTTPException
from firebase_admin import storage, auth
import jwt

def check_token(token):
    return auth.verify_id_token(token)
    # return jwt.decode(token, "secret", algorithms=["HS256"])

class FirebaseAuth:
    def verify_token(self, token):
        try:
            c = check_token(token)
            return c["user_id"]
        except: raise HTTPException(status_code=401, detail="token validation failed")

    def develop_create_token(self, uid):
        return jwt.encode({"user_id": uid}, 'secret', algorithm="HS256")

def get_auth() -> FirebaseAuth:
    return FirebaseAuth()

# TODO : 만약에 Blob이 존재하지 않는다면..?
class FirebaseStorage:
    @classmethod
    def remove_image_by_walk_id(self, walk_id:str, user_id:str):
        prefix = "images"
        postfix = ".png"
        bucket = storage.bucket()
        blob = bucket.get_blob(f"{prefix}/{user_id}/{walk_id}{postfix}")
        if blob:
            # only when blob exists
            blob.delete()