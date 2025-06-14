import os

import requests
from appwrite.client import Client
from appwrite.services.account import Account
from typing import Optional
from app.models.auth_models import EmailRequest, EmailVerificationRequest
from fastapi import HTTPException
from appwrite.exception import AppwriteException


class AppwriteAuthService:
    def __init__(self, project_id: str, api_key: str, hostname: str):
        """
        Handles Appwrite-based authentication from the backend.
        """
        self.client = Client()
        self.client.set_endpoint(hostname).set_project(project_id).set_key(api_key)
        self.project_id = project_id
        self.api_key = api_key
        self.hostname = hostname

    def _get_account_with_jwt(self, jwt: str) -> Account:
        """
        Creates a new Account instance with a user's JWT.
        """
        client = Client()
        client.set_endpoint(self.hostname).set_project(self.project_id).set_jwt(jwt)
        return Account(client)

    def signup_user(self, email: str, password: str) -> dict:
        """
        Registers a new user.
        """
        account = Account(self.client)
        try:
            return account.create(
                user_id="unique()",
                email=email,
                password=password
            )
        except Exception as e:
            raise Exception(f"Signup failed: {e}")

    def login_user(self, email: str, password: str) -> str:
        """
        Logs in a user and returns a JWT token.
        """
        account = Account(self.client)
        try:
            # Create a session first
            account.create_email_password_session(email=email, password=password)
            # Now generate JWT
            jwt = account.create_jwt()
            return jwt['jwt']
        except Exception as e:
            raise Exception(f"Login failed: {e}")

    def send_verification_email(self, email_request: EmailRequest):
        account = self._get_account_with_jwt(email_request.jwt)

        try:
            verification_redirect = os.getenv("VERIFICATION_REDIRECT")
            if verification_redirect is None:
                raise ValueError("VERIFICATION_REDIRECT environment variable not set")
            
            account.create_verification(
                url=verification_redirect
            )
            
            return {"message": "Verification email sent."}
        except AppwriteException as e:
            raise HTTPException(status_code=400, detail=str(e))

    def forgot_password(self, email: str):
        account = Account(self.client)

        try:
            recovery_redirect = os.getenv("RECOVERY_REDIRECT")
            if recovery_redirect is None:
                raise ValueError("RECOVERY_REDIRECT environment variable not set")
            account.create_recovery(
                email=email, url=recovery_redirect
            )
            return {"message": "Password reset email sent."}
    
        except AppwriteException as e:
            raise HTTPException(status_code=400, detail=str(e))

    def verify_email(self, verification_request: EmailVerificationRequest):
        account = self._get_account_with_jwt(verification_request.jwt)
        user_id: str = account.get()["$id"]
        
        try:
            _ = account.update_verification(user_id=user_id, secret=verification_request.secret)
            return {"message": "Email verified successfully."}
        except AppwriteException as e:
            raise HTTPException(status_code=400, detail=str(e))

    def get_user_from_jwt(self, jwt: str) -> Optional[dict]:
        """
        Gets user info from a JWT.
        """
        try:
            account = self._get_account_with_jwt(jwt)
            return account.get()
        except Exception as e:
            print(f"Invalid JWT or session: {e}")
            return None

    def logout_user(self, jwt: str):
        """
        Deletes the current session associated with the JWT.
        """
        try:
            account = self._get_account_with_jwt(jwt)
            account.delete_session("current")
            return {"message": "Logged out"}
        except Exception as e:
            raise Exception(f"Logout failed: {e}")

    def delete_user_account(self, jwt: str) -> dict:
        """
        Deletes the authenticated user's account by calling Appwrite REST API directly.
        """
        headers = {
            "Authorization": f"Bearer {jwt}",
            "Content-Type": "application/json",
        }
        url = f"{self.hostname}/account"
        response = requests.delete(url, headers=headers)

        if response.status_code == 204:
            return {"message": "Account deleted successfully"}
        else:
            raise Exception(f"Account deletion failed: {response.status_code} - {response.text}")


PROJECT_ID = os.getenv("PROJECT_ID")
API_KEY = os.getenv("API_KEY")
HOSTNAME = "https://cloud.appwrite.io/v1"

def get_auth_service() -> AppwriteAuthService:
    return AppwriteAuthService(
        project_id=PROJECT_ID,
        api_key=API_KEY,
        hostname=HOSTNAME
    )



