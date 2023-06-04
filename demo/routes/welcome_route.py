# welcome_route.py
from flask import Blueprint		# 블루프린트 패키지 import

# 라우트 네임 = welcome, 실행파일명 = __name__, 적용 url = /welcome
bp = Blueprint('welcome', __name__, url_prefix = '/welcome')

@bp.route('/')
def naming():
    return "hello, welcome to David's web"