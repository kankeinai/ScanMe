from dotenv import load_dotenv
import os
load_dotenv()
TOKEN = str(os.getenv('TOKEN'))
ADMIN = os.getenv('ADMIN')
