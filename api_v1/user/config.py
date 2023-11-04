import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY_BY_JWT = os.environ.get('SECRET_KEY_BY_JWT')
SECRET_KEY_BY_UserManager = os.environ.get('SECRET_KEY_BY_UserManager')