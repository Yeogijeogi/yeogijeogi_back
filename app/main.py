from fastapi import FastAPI
from app.routers import root, walk
from app.routers import user
from app.routers import temp
from app.db.mongodb import db_lifespan

app = FastAPI(lifespan=db_lifespan)

app.include_router(root.router)
app.include_router(walk.router)

app.include_router(user.router)
app.include_router(temp.router)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
