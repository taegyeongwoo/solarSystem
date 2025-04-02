from flask import Blueprint, render_template, request, flash, g, redirect, url_for
from werkzeug.utils import secure_filename, redirect

from .. import db
from solar.models import Property
from solar.forms import PropertyForm
from solar.views.auth_views import login_required

bp = Blueprint('put', __name__, url_prefix='/')

## 신청폼
@bp.route('/put/plant-sale/')
def plant_sale():
    return render_template('put/plant_sale.html')

@bp.route('/submit_sale', methods=['POST'])
@login_required
def submit_sale():
    user_id = g.user.id  # 현재 로그인 사용자 ID

    # 1) 폼에서 문자열/숫자 데이터 가져오기
    applicant_name = request.form.get('applicant_name')
    phone = request.form.get('phone')
    email = request.form.get('email')
    plant_name = request.form.get('plant_name')
    capacity = request.form.get('capacity')
    address = request.form.get('address')
    completion_date = request.form.get('completion_date')
    desired_price = request.form.get('desired_price')

    # (중략) 나머지 필드들도 모두 request.form.get('필드명')으로 가져오기
    capacity_type = request.form.get('capacity_type')
    current_status = request.form.get('current_status')
    remaining_sections = request.form.get('remaining_sections')
    land_contract = request.form.get('land_contract')
    observation_point = request.form.get('observation_point')
    annual_production = request.form.get('annual_production')
    power_sale_price = request.form.get('power_sale_price')
    # ... 등등 필요한 필드를 계속 가져옵니다.

    # 2) 파일 업로드 (예: 사업자등록증, 발전사업허가증 등)
    business_license = request.files.get('business_license')
    if business_license:
        filename = secure_filename(business_license.filename)
        # 예시) 로컬 저장 (실무에서는 UPLOAD_FOLDER 설정 or S3 업로드)
        # business_license.save(os.path.join(UPLOAD_FOLDER, filename))

    # 3) DB 모델 객체 생성
    # 실제 프로젝트에서는 user_id (현재 로그인 사용자 ID)도 함께 저장
    # 폼에서 가져온 데이터 (문자열이므로 숫자는 float/ int 변환)
    new_property = Property(
        # 유저 관계
        user_id=user_id,

        # 물건 정보
        property_id=request.form.get('property_id', ''),  # 폼 name="property_id"가 없으면 기본 ''
        capacity_type=request.form.get('capacity_type', ''),
        current_status=request.form.get('current_status', ''),
        remaining_sections=int(request.form.get('remaining_sections', 0)),
        land_contract=request.form.get('land_contract', ''),

        # 발전/매매 정보
        observation_point=request.form.get('observation_point', ''),
        annual_production=float(request.form.get('annual_production', 0.0)),
        power_sale_price=float(request.form.get('power_sale_price', 0.0)),
        annual_revenue=float(request.form.get('annual_revenue', 0.0)),
        remaining_revenue=float(request.form.get('remaining_revenue', 0.0)),
        accumulated_revenue=float(request.form.get('accumulated_revenue', 0.0)),

        # 가격 정보
        land_price=float(request.form.get('land_price', 0.0)),
        system_price=float(request.form.get('system_price', 0.0)),

        # 파이낸스 정보
        available_finance=request.form.get('available_finance', None),

        # 모듈 정보
        manufacturer=request.form.get('manufacturer', None),
        system_capacity=request.form.get('system_capacity', None),
        model_type=request.form.get('model_type', None),
        max_output=float(request.form.get('max_output', 0.0)),
        conversion_efficiency=float(request.form.get('conversion_efficiency', 0.0)),
        output_warranty=int(request.form.get('output_warranty', 0)),
        product_warranty=int(request.form.get('product_warranty', 0)),
        monitoring_system=request.form.get('monitoring_system', None),
        service_cost=float(request.form.get('service_cost', 0.0)),

        # 인버터 정보
        inverter_manufacturer=request.form.get('inverter_manufacturer', None),
        inverter_type=request.form.get('inverter_type', None),
        max_capacity=float(request.form.get('max_capacity', 0.0)),
        inverter_efficiency=float(request.form.get('inverter_efficiency', 0.0)),
        inverter_warranty=int(request.form.get('inverter_warranty', 0)),
        inverter_monitoring_system=request.form.get('inverter_monitoring_system', None),
        inverter_service_cost=float(request.form.get('inverter_service_cost', 0.0)),

        # 구조물 정보
        structure_manufacturer=request.form.get('structure_manufacturer', None),
        structure_type=request.form.get('structure_type', None),
        construction_method=request.form.get('construction_method', None),
        incident_angle=float(request.form.get('incident_angle', 0.0)),
        fixing_type=request.form.get('fixing_type', None),
        structure_warranty=int(request.form.get('structure_warranty', 0)),

        # 가격에 포함된 내용
        included_in_price=request.form.get('included_in_price', None),
    )

    # 4) DB에 저장
    db.session.add(new_property)
    db.session.commit()

    flash("판매 신청이 완료되었습니다!")  # 플래시 메시지
    return redirect(url_for('/mypage/reservation.html'))  # 신청 완료 후 이동할 페이지
