from datetime import datetime
from flask import Blueprint, render_template, request, url_for, g, flash
from werkzeug.utils import redirect
from .. import db

from solar.models import Question, Answer, User, Property  # Property 모델 추가
from solar.forms import QuestionForm, AnswerForm, PropertyForm  # PropertyForm 추가
from solar.views.auth_views import login_required

bp = Blueprint('announcement', __name__, url_prefix='/announcement')

'''
@bp.route('/list/')
def _list():
    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw', type=str, default='')
    question_list = Question.query.order_by(Question.create_date.desc())
    if kw:
        search = '%%{}%%'.format(kw)
        sub_query = db.session.query(Answer.question_id, Answer.content, User.username).join(User, Answer.user_id == User.id).subquery()
        question_list = question_list.join(User).outerjoin(sub_query, sub_query.c.question_id == Question.id). \
            filter(Question.subject.ilike(search) |  # 질문제목
                    Question.content.ilike(search) |  # 질문내용
                    User.username.ilike(search) |  # 질문작성자
                    sub_query.c.content.ilike(search) |  # 답변내용
                    sub_query.c.username.ilike(search)  # 답변작성자
                    ).distinct()
    question_list = question_list.paginate(page=page, per_page=10)
    return render_template('announcement/announcement_list.html', question_list=question_list, page=page, kw=kw)
'''
@bp.route('/detail/<int:question_id>/')
def detail(question_id) :
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    return render_template('announcement/announcement_detail.html', question=question, form=form)

@bp.route('/create/', methods=('GET', 'POST'))
@login_required
def create() :
    form = QuestionForm()
    if request.method == 'POST' and form.validate_on_submit() :
        question = Question(subject = form.subject.data, content = form.content.data, create_date = datetime.now(), user=g.user)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('announcement/announcement_form.html', form=form)

@bp.route('/modify/<int:question_id>', methods=('GET', 'POST'))
@login_required
def modify(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('announcement.detail', question_id=question_id))
    if request.method == 'POST':
        form = QuestionForm()
        if form.validate_on_submit():
            form.populate_obj(question)
            question.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect(url_for('announcement.detail', question_id=question_id))
    else:
        form = QuestionForm(obj=question)
    return render_template('announcement/announcement_form.html', form=form)
    
@bp.route('/delete/<int:question_id>')
@login_required
def delete(question_id) :
    question = Question.query.get_or_404(question_id)
    if g.user != question.user :
        flash('삭제권한이 없습니다')
        return redirect(url_for('announcement.detail', question_id=question_id))
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('announcement._list'))

@bp.route('/create_property', methods=['GET', 'POST'])
@login_required
def create_property():
    form = PropertyForm()
    if form.validate_on_submit():
        property = Property(
            user_id=g.user.id,  # 현재 로그인한 사용자의 ID를 설정
            property_id=form.property_id.data,
            capacity_type=form.capacity_type.data,
            current_status=form.current_status.data,
            remaining_sections=form.remaining_sections.data,
            land_contract=form.land_contract.data,
            observation_point=form.observation_point.data,
            annual_production=form.annual_production.data,
            power_sale_price=form.power_sale_price.data,
            annual_revenue=form.annual_revenue.data,
            remaining_revenue=form.remaining_revenue.data,
            accumulated_revenue=form.accumulated_revenue.data,
            land_price=form.land_price.data,
            system_price=form.system_price.data,
            available_finance=form.available_finance.data,
            manufacturer=form.manufacturer.data,
            system_capacity=form.system_capacity.data,
            model_type=form.model_type.data,
            max_output=form.max_output.data,
            conversion_efficiency=form.conversion_efficiency.data,
            output_warranty=form.output_warranty.data,
            product_warranty=form.product_warranty.data,
            monitoring_system=form.monitoring_system.data,
            service_cost=form.service_cost.data,
            inverter_manufacturer=form.inverter_manufacturer.data,
            inverter_type=form.inverter_type.data,
            max_capacity=form.max_capacity.data,
            inverter_efficiency=form.inverter_efficiency.data,
            inverter_warranty=form.inverter_warranty.data,
            inverter_monitoring_system=form.inverter_monitoring_system.data,
            inverter_service_cost=form.inverter_service_cost.data,
            structure_manufacturer=form.structure_manufacturer.data,
            structure_type=form.structure_type.data,
            construction_method=form.construction_method.data,
            incident_angle=form.incident_angle.data,
            fixing_type=form.fixing_type.data,
            structure_warranty=form.structure_warranty.data,
            included_in_price=form.included_in_price.data
        )
        db.session.add(property)
        db.session.commit()
        return redirect(url_for('announcement._list'))  # 리다이렉션 경로 수정

    return render_template('announcement/announcement_form.html', form=form)
