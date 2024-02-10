from fastapi import FastAPI
from uuid import uuid4 as uuid
import models
from database import engine
from fastapi.middleware.cors import CORSMiddleware
from endpoints.users import router as user_router
from endpoints.admin import router as admin_router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

origins = [
    'http://localhost:8000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

models.Base.metadata.create_all(bind=engine)


@app.get('/api')
async def read_root():
    return {'id': uuid(), "response": "GSJ Engineering s.r.o.", 'data': 'GSJ Notes'}


app.include_router(user_router)
app.include_router(admin_router)
