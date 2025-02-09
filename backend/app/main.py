from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, cloud_cost  # ✅ Import cloud_cost route

app = FastAPI()

# Enable CORS to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include the cloud cost and authentication routers
app.include_router(auth.router)
app.include_router(cloud_cost.router)  # ✅ Add this line

@app.get("/")
def read_root():
    return {"message": "Welcome to Cloud Cost Optimizer"}
