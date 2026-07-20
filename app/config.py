import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    DEBUG = True
    APPOINTMENTS_API_URL = os.getenv(
        "APPOINTMENTS_API_URL",
        "http://127.0.0.1:5000/api/appointments",
    )
    APPOINTMENTS_API_TIMEOUT = int(os.getenv("APPOINTMENTS_API_TIMEOUT", "5"))
