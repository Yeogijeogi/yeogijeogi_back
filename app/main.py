from fastapi import FastAPI
from app.routers import root, walk_root
from app.db.mongodb import db_lifespan

app = FastAPI(lifespan=db_lifespan)

app.include_router(root.router)
app.include_router(walk_root.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
