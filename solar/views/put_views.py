from flask import Blueprint, render_template, request, flash, g, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime
import uuid

from .. import db
from solar.models import Property, User
from solar.forms import PropertyForm
from solar.views.auth_views import login_required
import sys, os

bp = Blueprint('put', __name__, url_prefix='/')

# 발전소 판매 신청 폼 페이지
@bp.route('/put/plant-sale/')
def plant_sale():
    return render_template('put/plant_sale.html')


# 문자열을 안전하게 float으로 변환하는 함수
def to_float(value, default=0.0):
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


# 문자열을 안전하게 int로 변환하는 함수
def to_int(value, default=0):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

# 저장 경로
def save_file(file_field_name, subfolder):
    
    from flask import current_app
    BASE_UPLOAD_PATH = os.path.join(current_app.root_path, 'static', 'saved')

    file = request.files.get(file_field_name)
    if file and file.filename:
        original_filename = secure_filename(file.filename)
        upload_dir = os.path.join(BASE_UPLOAD_PATH, subfolder)
        os.makedirs(upload_dir, exist_ok=True)

        # 중복 방지: 같은 이름이 있으면 UUID 붙이기
        save_path = os.path.join(upload_dir, original_filename)
        if os.path.exists(save_path):
            name, ext = os.path.splitext(original_filename)
            new_filename = f"{name}_{uuid.uuid4().hex[:8]}{ext}"
            save_path = os.path.join(upload_dir, new_filename)
        else:
            new_filename = original_filename

        file.save(save_path)
        return new_filename
    return None

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 폼 제출 처리
@bp.route('/submit_sale', methods=['POST'])
@login_required
def submit_sale():
    user_id = g.user.id  # 현재 로그인 사용자 ID

    # 가격에 포함된 내용 (다중 선택 체크박스 처리)
    included_items = request.form.getlist('included_in_price')
    included_in_price = ', '.join(included_items) if included_items else None

    # 파일 업로드 처리
    def save_uploaded_file(field_name):
        file = request.files.get(field_name)
        if file and allowed_file(file.filename):
            filename = f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
            save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(save_path)
            return filename
        return None

    # 파일 업로드
    business_license_filename = save_file('business_license', 'registeration_certificate')
    power_license_filename = save_file('power_business_license', 'power_license')
    grid_contract_filename = save_file('grid_connection_contract', 'grid_connection')

    # Property 모델 인스턴스 생성
    new_property = Property(
        # 유저 관계
        user_id=user_id,

        # 물건 정보
        property_id=request.form.get('property_id', ''),
        capacity_type=request.form.get('capacity_type', ''),
        current_status=request.form.get('current_status', ''),
        remaining_sections=to_int(request.form.get('remaining_sections')),
        land_contract=request.form.get('land_contract', ''),

        # 발전/매매 정보
        observation_point=request.form.get('observation_point', ''),
        annual_production=to_float(request.form.get('annual_production')),
        power_sale_price=to_float(request.form.get('power_sale_price')),
        annual_revenue=to_float(request.form.get('annual_revenue')),
        remaining_revenue=to_float(request.form.get('remaining_revenue')),
        accumulated_revenue=to_float(request.form.get('accumulated_revenue')),

        # 가격 정보
        land_price=to_float(request.form.get('land_price')),
        system_price=to_float(request.form.get('system_price')),

        # 파이낸스 정보
        available_finance=request.form.get('available_finance', None),

        # 모듈 정보
        manufacturer=request.form.get('manufacturer', None),
        system_capacity=request.form.get('system_capacity', None),
        model_type=request.form.get('model_type', None),
        max_output=to_float(request.form.get('max_output')),
        conversion_efficiency=to_float(request.form.get('conversion_efficiency')),
        output_warranty=to_int(request.form.get('output_warranty')),
        product_warranty=to_int(request.form.get('product_warranty')),
        monitoring_system=request.form.get('monitoring_system', None),
        service_cost=to_float(request.form.get('service_cost')),

        # 인버터 정보
        inverter_manufacturer=request.form.get('inverter_manufacturer', None),
        inverter_type=request.form.get('inverter_type', None),
        max_capacity=to_float(request.form.get('max_capacity')),
        inverter_efficiency=to_float(request.form.get('inverter_efficiency')),
        inverter_warranty=to_int(request.form.get('inverter_warranty')),
        inverter_monitoring_system=request.form.get('inverter_monitoring_system', None),
        inverter_service_cost=to_float(request.form.get('inverter_service_cost')),

        # 구조물 정보
        structure_manufacturer=request.form.get('structure_manufacturer', None),
        structure_type=request.form.get('structure_type', None),
        construction_method=request.form.get('construction_method', None),
        incident_angle=to_float(request.form.get('incident_angle')),
        fixing_type=request.form.get('fixing_type', None),
        structure_warranty=to_int(request.form.get('structure_warranty')),

        # 가격에 포함된 내용
        included_in_price=included_in_price,

        # 서류
        business_registration_certificate=business_license_filename,
        power_business_license=power_license_filename,
        grid_connection_contract=grid_contract_filename,
    )

    # DB에 저장
    db.session.add(new_property)
    db.session.commit()

    flash("판매 신청이 완료되었습니다!")
    return redirect(url_for('main.index'))  # 본인의 마이페이지나 목록 페이지로 수정 가능

@bp.route('/announcement/list/')
def property_list() :
    page = request.args.get('page', default=1, type=int)
    kw = request.args.get('kw', default='', type=str)

    # 기본 쿼리
    property_query = Property.query.order_by(Property.id.desc())

    if kw:
        search = f"%%{kw}%%"
        property_query = property_query.join(User).filter(
            Property.property_id.ilike(search) |
            Property.system_capacity.ilike(search) |
            User.username.ilike(search)
        )
        
    # 페이징 된 property 목록
    property_list = property_query.paginate(page=page, per_page=10)
    return render_template('announcement/announcement_list.html', property_list=property_list, page=page, kw=kw)

@bp.route('/detail/<int:property_id>/')
def detail(property_id):
    property = Property.query.get_or_404(property_id)
    return render_template('announcement/announcement_detail.html', property=property)
