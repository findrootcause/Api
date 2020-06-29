import os

DB_HOST = '127.0.0.1'
DB_PORT = 3306
DB_NAME = 'findcause'
DB_USER = 'root'
DB_PASSWORD = 'password'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_ROOT = os.path.join(BASE_DIR, 'upload')
MEDIA_URL = '/upload/'