from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import bcrypt
import jwt
from fastapi import Header
import datetime 

SECRET_KEY="JWT_SECRET_KEY"
ALGORITHM="HS256"

app = FastAPI()

user_db = {}

def get_password_hash(password: str):

    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(pwd_bytes, salt)

    return hashed_password.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str):
    password_byte_enc = plain_password.encode('utf-8')
    hashed_password_byte_enc = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_byte_enc, hashed_password_byte_enc)

def create_access_token(username: str):
    payload = {
        "sub": username,
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=30)
    }

    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

class User(BaseModel):
    username: str
    password: str = Field(..., max_length=72)

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.post("/register")
def register(user_data: User):
    if user_data.username in user_db:
        raise HTTPException(status_code=400, detail="User already registered")
        
    hashed_password = get_password_hash(user_data.password)
    user_db[user_data.username] = hashed_password
    return {"status": "success", "message": "User registered successfully"}

@app.post("/login")
def login(user_data: User):
    if user_data.username not in user_db:
        raise HTTPException(status_code=400, detail="User not registered")
    
    if not verify_password(user_data.password, user_db[user_data.username]):
        raise HTTPException(status_code=400, detail="Wrong password")

    access_token=create_access_token(user_data.username)
    return {"status": "success", "message": "Login successful", "access_token": access_token,"token_type": "bearer"}

@app.get("/access-protected")
def access_protected_resource(authorization: str=Header(None)):
    if authorization is None or not authorization.startswith("Bearer"):
        raise HTTPException(status_code=401, detail="Authorization header missing")
    try:
        token = authorization.split(" ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"status": "success", "message": "Access protected resource successfully", "username": username}
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidSignatureError:
        raise HTTPException(status_code=401, detail="Invalid signature")
    
@app.get("/users")
def get_users():
    return user_db
