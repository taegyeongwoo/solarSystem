from datetime import datetime
from flask import Blueprint, render_template, request, url_for, g, flash
from werkzeug.utils import redirect

# bp = Blueprint('home', __name__, url_prefix='/')
bp = Blueprint('main', __name__, url_prefix='/')

## 홈페이지
@bp.route('/')
def index():
    return render_template('index.html')

## 소개 페이지

# 회사 소개
@bp.route('/introduce/company')
def company() :
    return render_template('/introduce/company.html')

# 플랫폼 가이드 페이지 라우트 추가
@bp.route('/introduce/platform-guide')
def platform_guide():
    return render_template('/introduce/platform_guide.html')


## 시공사 등록 페이지



## 시공사 공고 페이지
@bp.route('/announcement')
def announcement() :
    return redirect(url_for('announcement._list'))


## 견적 문의 페이지

# 문의
@bp.route('/question')
def question() :
    return redirect(url_for('question._list'))