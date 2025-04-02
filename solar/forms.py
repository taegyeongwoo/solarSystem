from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, FloatField, IntegerField, SelectField
from wtforms.fields import EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email, Optional

class QuestionForm(FlaskForm) :
    subject = StringField('제목', validators = [DataRequired('제목은 필수 입력 사항입니다.')])
    content = TextAreaField('내용', validators = [DataRequired('내용은 필수 입력 사항입니다.')])

class AnswerForm(FlaskForm) :
    content = TextAreaField('내용', validators = [DataRequired('내용은 필수 입력 사항입니다.')])

class UserCreateForm(FlaskForm) :
    username = StringField('사용자 이름', validators=[DataRequired(), Length(min=3, max=25)])
    password1 = PasswordField('비밀번호', validators=[DataRequired(), EqualTo('password2', '비밀번호가 일치하지 않습니다.')])
    password2 = PasswordField('비밀번호 확인', validators=[DataRequired()])
    email = EmailField('이메일', [DataRequired(), Email()])

class UserLoginForm(FlaskForm) :
    username = StringField('사용자 이름', validators = [DataRequired(), Length(min=3, max=25)])
    password = PasswordField('비밀번호', validators=[DataRequired()])

class CommentForm(FlaskForm) :
    content = TextAreaField('내용', validators=[DataRequired()])

class PropertyForm(FlaskForm):
    # 물건 정보
    property_id = StringField('물건 ID', validators=[DataRequired()])
    capacity_type = SelectField('용량 구분', choices=[('small', '소형'), ('medium', '중형'), ('large', '대형')], validators=[DataRequired()])
    current_status = SelectField('현재 상태', choices=[('pre_construction', '공사전'), ('under_construction', '공사중'), ('completed', '완공')], validators=[DataRequired()])
    remaining_sections = IntegerField('잔존 구획수', validators=[DataRequired()])
    land_contract = SelectField('토지 계약', choices=[('lease', '임대'), ('purchase', '매매')], validators=[DataRequired()])
    
    # 발전/매매정보
    observation_point = StringField('관측지점', validators=[DataRequired()])
    annual_production = FloatField('연간발전량', validators=[DataRequired()])
    power_sale_price = FloatField('매전단가', validators=[DataRequired()])
    annual_revenue = FloatField('매전수입/년', validators=[DataRequired()])
    remaining_revenue = FloatField('잔존 매전수입', validators=[DataRequired()])
    accumulated_revenue = FloatField('누전수익', validators=[DataRequired()])
    
    # 가격정보
    land_price = FloatField('토지 가격', validators=[DataRequired()])
    system_price = FloatField('시스템 가격', validators=[DataRequired()])
    
    # 파이낸스 정보
    available_finance = StringField('이용가능한 신판회사', validators=[Optional()])
    
    # 모듈 정보
    manufacturer = StringField('제조사', validators=[Optional()])
    system_capacity = SelectField('시스템 용량', choices=[('low', '저용량'), ('medium', '중용량'), ('high', '고용량')], validators=[Optional()])
    model_type = StringField('형식', validators=[Optional()])
    max_output = FloatField('최대출력 (W)', validators=[Optional()])
    conversion_efficiency = FloatField('변환효율 (%)', validators=[Optional()])
    output_warranty = IntegerField('출력보증 (년)', validators=[Optional()])
    product_warranty = IntegerField('제품보증 (년)', validators=[Optional()])
    monitoring_system = SelectField('감시시스템', choices=[('yes', '유'), ('no', '무')], validators=[Optional()])
    service_cost = FloatField('서비스 비용', validators=[Optional()])
    
    # 인버터 정보
    inverter_manufacturer = StringField('제조사', validators=[Optional()])
    inverter_type = StringField('형식', validators=[Optional()])
    max_capacity = FloatField('최대용량 (kW)', validators=[Optional()])
    inverter_efficiency = FloatField('변환효율 (%)', validators=[Optional()])
    inverter_warranty = IntegerField('제품보증 (년)', validators=[Optional()])
    inverter_monitoring_system = SelectField('감시시스템', choices=[('yes', '유'), ('no', '무')], validators=[Optional()])
    inverter_service_cost = FloatField('서비스 비용', validators=[Optional()])
    
    # 구조물 정보
    structure_manufacturer = StringField('제조사', validators=[Optional()])
    structure_type = StringField('형식', validators=[Optional()])
    construction_method = SelectField('공법', choices=[('method1', '공법1'), ('method2', '공법2')], validators=[Optional()])
    incident_angle = FloatField('입사각 (도)', validators=[Optional()])
    fixing_type = SelectField('고정형태', choices=[('fixed', '고정형'), ('adjustable', '가변형'), ('tracking', '추적형')], validators=[Optional()])
    structure_warranty = IntegerField('제품보증 (년)', validators=[Optional()])
    
    # 가격에 포함된 내용
    included_in_price = StringField('가격에 포함된 내용', validators=[Optional()])