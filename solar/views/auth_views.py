from flask import Blueprint, url_for, render_template, flash, request, session, g, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from functools import wraps

from solar import db
from solar.forms import UserCreateForm, UserLoginForm
from solar.models import User, Property, Question, PropertyLike

import functools

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/signup', methods=('GET', 'POST'))
def signup() :
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit() :
        user = User.query.filter_by(username=form.username.data).first()
        if not user :
            user = User(username=form.username.data,
                        password=generate_password_hash(form.password1.data),
                        email=form.email.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))
        else :
            flash('이미 존재하는 사용자입니다.')
    return render_template('auth/signup.html', form=form)

@bp.route('/auth/admin/dashboard')
def admin_dashboard():
    return render_template('auth/admin_dashboard.html')

@bp.route('/auth/mypage')
def mypage():
    user_id = session.get('user_id')
    user = User.query.get(user_id)

    # 최근 3개의 거래 내역 (예: 모든 거래 상태 포함)
    latest_properties = (
        Property.query
        .filter_by(user_id=user_id)
        .order_by(Property.create_date.desc())
        .limit(3)
        .all()
    )

    question_list = Question.query.filter_by(user_id=user_id) \
                                  .order_by(Question.create_date.desc()) \
                                  .paginate(page=request.args.get('page', 1, type=int), per_page=5)
    
    liked_properties = []

    if g.user:
        liked_properties = Property.query \
            .join(PropertyLike, Property.id == PropertyLike.property_id) \
            .filter(PropertyLike.user_id == g.user.id) \
            .order_by(Property.create_date.desc()) \
            .all()
    
    return render_template('auth/mypage.html', user=user, question_list=question_list, latest_properties=latest_properties, liked_properties=liked_properties)

@bp.route('/login', methods=['GET', 'POST'])
def login() :
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit() :
        error = None
        # form에서 입력한 username을 가져와서 데이터베이스에 입력되어 있는지 확인
        user = User.query.filter_by(username=form.username.data).first()
        if not user :
            error = "존재하지 않는 사용자입니다."
        # user.password : 데이터 베이스에 저장되어 있는 비밀번호
        # form.password.data : form에서 입력한 password
        # 이 둘을 비교
        elif not check_password_hash(user.password, form.password.data) :
            error = "비밀번호가 올바르지 않습니다."
        if error is None :
            session.clear()
            # user.id : 데이터베이스에 저장되어 있는 사용자의 id
            session['user_id'] = user.id

            ## 로그인 성공 시 사용자 유형에 따라 분기
            return redirect(url_for('main.index'))
        flash(error)
    return render_template('auth/login.html', form=form)

@bp.route('/logout')
def logout() :
    session.clear()
    return redirect(url_for('main.index'))

@bp.before_app_request
def load_logged_in_user() :
    user_id = session.get('user_id')
    if user_id is None :
        g.user = None
    else :
        g.user = User.query.get(user_id)

def login_required(view) :
    @functools.wraps(view)
    def wrapped_view(**kwargs) :
        if g.user is None :
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
