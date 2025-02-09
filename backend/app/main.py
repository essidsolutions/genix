from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, cloud_cost, oauth  # ✅ Import OAuth

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(cloud_cost.router)
app.include_router(oauth.router)  # ✅ Ensure OAuth is included

@app.get("/")
def read_root():
    return {"message": "Welcome to Cloud Cost Optimizer"}
