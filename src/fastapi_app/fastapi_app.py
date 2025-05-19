from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from src.fastapi_app.endpoints.asteroids import router
import uvicorn

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(router, prefix='/asteroids', tags=['asteroids'])

if __name__ == '__main__':
    uvicorn.run('fastapi_app:app', host='0.0.0.0', port=8001)
