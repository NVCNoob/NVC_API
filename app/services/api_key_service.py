from sqlmodel import Session, select
from app.core.database import get_db
from app.schemas.api_key import APIKey
from fastapi import Depends, HTTPException, Header


def verify_api_key(
    x_api_key: str = Header(...),
    db: Session = Depends(get_db)
) -> APIKey:
    statement = select(APIKey).where(APIKey.key == x_api_key, APIKey.is_active == True)
    key = db.exec(statement).first()

    if not key:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")

    return key



def admin_only(x_admin_token: str = Header(...)):
    if x_admin_token != "aiaidj231j43^%#3GGFSt%$32$%Grgrtce^^%4#4@21Y_r)%$(hgbjhbdeed$)5930djksdhb@Y^631728/.vkjvdfdvneui":
        raise HTTPException(status_code=403, detail="Admin access only")


