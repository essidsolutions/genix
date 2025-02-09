import boto3
import requests
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.user import User
from app.models.oauth import OAuthCredentials
from pydantic import BaseModel
from cryptography.fernet import Fernet
import os

router = APIRouter(prefix="/oauth", tags=["OAuth"])

# Generate an encryption key for storing credentials securely (do this once and save the key securely)
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", Fernet.generate_key().decode())
cipher_suite = Fernet(ENCRYPTION_KEY.encode())

class OAuthRequest(BaseModel):
    provider: str
    client_id: str
    client_secret: str
    auth_token: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/connect")
def connect_cloud(oauth_request: OAuthRequest, db: Session = Depends(get_db)):
    encrypted_client_id = cipher_suite.encrypt(oauth_request.client_id.encode()).decode()
    encrypted_client_secret = cipher_suite.encrypt(oauth_request.client_secret.encode()).decode()

    # Store credentials in the database
    credentials = OAuthCredentials(
        provider=oauth_request.provider,
        client_id=encrypted_client_id,
        client_secret=encrypted_client_secret
    )
    db.add(credentials)
    db.commit()

    if oauth_request.provider == "AWS":
        try:
            sts_client = boto3.client("sts")
            response = sts_client.assume_role_with_web_identity(
                RoleArn="arn:aws:iam::YOUR_ACCOUNT_ID:role/OAuthAccessRole",
                RoleSessionName="OAuthSession",
                WebIdentityToken=oauth_request.auth_token
            )
            credentials = response["Credentials"]
            return {"message": "Connected to AWS successfully!", "access_key": credentials["AccessKeyId"]}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    elif oauth_request.provider == "Azure":
        try:
            token_response = requests.post(
                "https://login.microsoftonline.com/YOUR_TENANT_ID/oauth2/v2.0/token",
                data={
                    "client_id": oauth_request.client_id,
                    "client_secret": oauth_request.client_secret,
                    "grant_type": "authorization_code",
                    "code": oauth_request.auth_token,
                    "redirect_uri": "http://localhost:3000/callback"
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
            token_data = token_response.json()
            return {"message": "Connected to Azure successfully!", "access_token": token_data["access_token"]}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    elif oauth_request.provider == "GCP":
        try:
            token_response = requests.post(
                "https://oauth2.googleapis.com/token",
                data={
                    "client_id": oauth_request.client_id,
                    "client_secret": oauth_request.client_secret,
                    "grant_type": "authorization_code",
                    "code": oauth_request.auth_token,
                    "redirect_uri": "http://localhost:3000/callback"
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
            token_data = token_response.json()
            return {"message": "Connected to GCP successfully!", "access_token": token_data["access_token"]}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    return {"message": "Invalid provider specified."}
