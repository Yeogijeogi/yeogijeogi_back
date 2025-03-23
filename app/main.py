from fastapi import FastAPI
from routers import root

app = FastAPI()

app.include_router(root.router)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
