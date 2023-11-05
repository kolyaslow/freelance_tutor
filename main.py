from fastapi import FastAPI

import uvicorn

from api_v1 import router as api_v1_router

app = FastAPI()
app.include_router(router=api_v1_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
