from fastapi import FastAPI
from routers import root
from db.mongodb import db_lifespan

app = FastAPI(lifespan=db_lifespan)

app.include_router(root.router)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
