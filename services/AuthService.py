from datetime import datetime, timedelta

import jwt

SECRET_KEY = "my_secret_key"
ALGORITHM = "HS256"
EXPIRATION_TIME = timedelta(days=30)


def create_jwt_token(data: dict):
    # время истечения токена
    expiration = datetime.utcnow() + EXPIRATION_TIME

    data.update({"exp": expiration})
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return token

# функция для проверки JWT токена
def verify_jwt_token(token: str):
    try:
        decoded_data = jwt.decode(token,
                                  SECRET_KEY,
                                  algorithms=[ALGORITHM])
        return decoded_data
    except jwt.PyJWTError:
        return None
