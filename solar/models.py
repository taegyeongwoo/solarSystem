from solar import db
from datetime import datetime

question_voter = db.Table(
    'question_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('question.id', db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), primary_key=True)
)

answer_voter = db.Table(
    'answer_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('answer_id', db.Integer, db.ForeignKey('answer.id', ondelete='CASCADE'), primary_key=True)
)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    # server_default = 1 : 최초로 생성한 User 모델 데이터의 id를 의미
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('question_set'))
    modify_date = db.Column(db.DateTime(), nullable=True)
    voter = db.relationship('User', secondary=question_voter, backref=db.backref('question_voter_set'))

class Answer(db.Model) :
    id = db.Column(db.Integer, primary_key = True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))
    question = db.relationship('Question', backref = db.backref('answer_set', ))
    content = db.Column(db.Text(), nullable = False)
    create_date = db.Column(db.DateTime(), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('answer_set'))
    modify_date = db.Column(db.DateTime(), nullable=True)
    voter = db.relationship('User', secondary=answer_voter, backref=db.backref('answer_voter_set'))

class User(db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

class Comment(db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('comment_set'))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    modify_date = db.Column(db.DateTime())
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), nullable=True)
    question = db.relationship('Question', backref=db.backref('comment_set'))
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id', ondelete='CASCADE'), nullable=True)
    answer = db.relationship('Answer', backref=db.backref('comment_set'))

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # User와의 관계 설정
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('properties', lazy=True))

    create_date = db.Column(db.DateTime(), nullable=False)  # 등록일시
    status = db.Column(db.String(50), nullable=False, default="심사전")  # 상태 (심사전/심사중/심사완료)
    status_result = db.Column(db.String(50), nullable=True)  # 심사 결과 (승인/거절)
    modify_date = db.Column(db.DateTime(), nullable=True)  # 수정일시

    # 신청자 정보
    applicant_name = db.Column(db.String(100), nullable=False)  # 신청자명
    phone = db.Column(db.String(20), nullable=False)  # 연락처
    email = db.Column(db.String(120), nullable=False)  # 이메일

    # 물건 정보
    plant_name = db.Column(db.String(100), nullable=False)  # 발전소명
    location = db.Column(db.String(100), nullable=False)  # 광역시/도
    sub_location = db.Column(db.String(100), nullable=False)  # 시/군/구
    capacity = db.Column(db.Float, nullable=False)  # 용량(W)
    current_status = db.Column(db.String(50), nullable=False)  # 현재 상태 (공사전/공사중/완공)
    completion_date = db.Column(db.Date, nullable=False)  # 준공(예정)일
    land_contract = db.Column(db.String(50), nullable=False)  # 토지 계약 (임대/매매)

    # 발전/매매 정보
    observation_point = db.Column(db.String(50), nullable=True)  # 관측지점
    annual_production = db.Column(db.Float, nullable=False)  # 연간발전량 (kWh)
    power_sale_price = db.Column(db.Float, nullable=False)  # 매전단가 (원)
    annual_revenue = db.Column(db.Float, nullable=False)  # 매전수입/년 (원)
    remaining_revenue = db.Column(db.Float, nullable=False)  # 잔존 매전수입 (원)
    accumulated_revenue = db.Column(db.Float, nullable=False)  # 누전수익 (원)

    # 가격 정보
    desired_price = db.Column(db.Float, nullable=False)  # 판매 희망가 (원)
    land_price = db.Column(db.Float, nullable=False)  # 토지 가격 (원)
    system_price = db.Column(db.Float, nullable=False)  # 시스템 가격 (원)

    # 모듈 정보
    manufacturer = db.Column(db.String(100))  # 제조사
    system_capacity = db.Column(db.String(50))  # 시스템 용량 (W)
    max_output = db.Column(db.Float)  # 최대출력 (W)
    conversion_efficiency = db.Column(db.Float)  # 변환효율 (%)
    output_warranty = db.Column(db.Integer)  # 출력보증 (년)
    product_warranty = db.Column(db.Integer)  # 제품보증 (년)
    monitoring_system = db.Column(db.String(10))  # 감시시스템 (유/무)
    service_cost = db.Column(db.Float)  # 서비스 비용 (원)

    # 인버터 정보
    inverter_manufacturer = db.Column(db.String(100))  # 제조사
    max_capacity = db.Column(db.Float)  # 최대용량 (W)
    inverter_efficiency = db.Column(db.Float)  # 변환효율 (%)
    inverter_warranty = db.Column(db.Integer)  # 제품보증 (년)
    inverter_monitoring_system = db.Column(db.String(10))  # 감시시스템 (유/무)
    inverter_service_cost = db.Column(db.Float)  # 서비스 비용 (원)

    # 구조물 정보
    structure_manufacturer = db.Column(db.String(100))  # 제조사
    construction_method = db.Column(db.String(50))  # 공법
    incident_angle = db.Column(db.Float)  # 입사각 (도)
    structure_product_warranty = db.Column(db.Integer)  # 제품보증 (년)

    # 추가 정보
    notes = db.Column(db.Text)  # 특이사항
    included_in_price = db.Column(db.String(500))  # 가격에 포함된 내용

    # 서류
    business_registration_certificate = db.Column(db.String(200), nullable=True)  # 사업자등록증
    power_business_license = db.Column(db.String(200), nullable=True)  # 발전사업 허가증
    grid_connection_contract = db.Column(db.String(200), nullable=True)  # 계통연계 계약서
