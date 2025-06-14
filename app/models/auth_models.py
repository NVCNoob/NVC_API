from pydantic import BaseModel


class EmailRequest(BaseModel):
  email: str
  jwt: str

class EmailVerificationRequest(BaseModel):
  secret: str
  jwt: str

class ForgotPsswordRequest(BaseModel):
  email: str
  