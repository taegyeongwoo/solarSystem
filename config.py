import os

BASE_DIR = os.path.dirname(__file__)
UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'solar\\static\\saved\\')

# 데이터 베이스 접속 주소
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'solar.db'))
# SQLAlchemy 이벤트 처리 옵션
SQLALCHEMY_TRACK_MODIFICATIONS = False

# 디버그 모드 활성화
DEBUG = True

SECRET_KEY = "dev"
