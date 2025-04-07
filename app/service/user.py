# from app.dependencies.firebase import get_auth

def create_user(authorization_token:str):
    auth = get_auth()
    auth.verify_id_token(authorization_token)