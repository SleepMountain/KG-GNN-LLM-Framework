import os
from dotenv import load_dotenv
load_dotenv()
def GetEnv(key):
    return os.getenv(key)
