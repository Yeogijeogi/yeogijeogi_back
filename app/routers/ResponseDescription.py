class ResponseDescription:
    @classmethod
    def get_401(cls): return { "description": "Invalid Token"}
    @classmethod
    def get_500(cls): return { "description": "Internal Server Error"}
    @classmethod
    def get_200(cls): return {"description" : "Successful Response"}
    @classmethod
    def get_404(cls): return {"description" : "Resource Not Found"}