from solar import db

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

    # 물건 정보
    property_id = db.Column(db.String(50), nullable=False)
    capacity_type = db.Column(db.String(50), nullable=False)  # 용량 구분
    current_status = db.Column(db.String(50), nullable=False)  # 현재 상태
    remaining_sections = db.Column(db.Integer, nullable=False)  # 잔존 구획수
    land_contract = db.Column(db.String(50), nullable=False)  # 토지 계약
    
    # 발전/매매정보
    observation_point = db.Column(db.String(50), nullable=False)  # 관측지점
    annual_production = db.Column(db.Float, nullable=False)  # 연간발전량
    power_sale_price = db.Column(db.Float, nullable=False)  # 매전단가
    annual_revenue = db.Column(db.Float, nullable=False)  # 매전수입/년
    remaining_revenue = db.Column(db.Float, nullable=False)  # 잔존 매전수입
    accumulated_revenue = db.Column(db.Float, nullable=False)  # 누전수익

    # 가격정보
    land_price = db.Column(db.Float, nullable=False)  # 토지 가격
    system_price = db.Column(db.Float, nullable=False)  # 시스템 가격

    # 파이낸스 정보
    available_finance = db.Column(db.String(200))  # 이용가능한 신판회사
    
    # 모듈 정보
    manufacturer = db.Column(db.String(100))  # 제조사
    system_capacity = db.Column(db.String(50))  # 시스템 용량
    model_type = db.Column(db.String(50))  # 형식
    max_output = db.Column(db.Float)  # 최대출력
    conversion_efficiency = db.Column(db.Float)  # 변환효율
    output_warranty = db.Column(db.Integer)  # 출력보증 (년)
    product_warranty = db.Column(db.Integer)  # 제품보증 (년)
    monitoring_system = db.Column(db.String(10))  # 감시시스템 (유/무)
    service_cost = db.Column(db.Float)  # 서비스 비용

    # 인버터 정보
    inverter_manufacturer = db.Column(db.String(100))  # 제조사
    inverter_type = db.Column(db.String(50))  # 형식
    max_capacity = db.Column(db.Float)  # 최대용량
    inverter_efficiency = db.Column(db.Float)  # 변환효율
    inverter_warranty = db.Column(db.Integer)  # 제품보증 (년)
    inverter_monitoring_system = db.Column(db.String(10))  # 감시시스템 (유/무)
    inverter_service_cost = db.Column(db.Float)  # 서비스 비용

    # 구조물 정보
    structure_manufacturer = db.Column(db.String(100))  # 제조사
    structure_type = db.Column(db.String(50))  # 형식
    construction_method = db.Column(db.String(50))  # 공법
    incident_angle = db.Column(db.Float)  # 입사각 (도)
    fixing_type = db.Column(db.String(50))  # 고정형태 (고정형/가변형/추적형)
    structure_warranty = db.Column(db.Integer)  # 제품보증 (년)
    
    # 가격에 포함된 내용
    included_in_price = db.Column(db.String(500))  # 가격에 포함된 내용 (다중 선택형)

