# -*- coding: UTF-8 -*-
import os
from werkzeug.utils import secure_filename
from ..decorators import modify_required
from flask import render_template, redirect, url_for,flash,request, current_app,jsonify
from project.models import ArticleType, Article, FriendshipLink
from . import admin
from flask_login import login_required,current_user
from ..decorators import admin_required
from .forms import SearchAlumniForm,enrollmentForm
from ..models import db,User,Enterprise
from sqlalchemy.sql.expression import or_,not_


from flask_mail import Message
from project import mail

#校友入会审核
@admin.route("/verify/schoolfellow",methods=['GET','POST'])
@login_required
@admin_required
def fellow_list():
    search_form = SearchAlumniForm()
    if search_form.validate_on_submit():
        keywords = search_form.keywords.data
        activities = User.query.filter(or_(User.name.like('%' + keywords + '%'))).all()
        return render_template('admin/verify/schoolfellow_index.html', search_form=search_form,
                               activities=activities)
    page = request.args.get('page', 1, type=int)
    user = User.query.filter(not_(User.username=='admin'))
    pagination = user.filter(not_(User.name=='None')).paginate(
        page, per_page=current_app.config['FLASY_NEWS_PER_PAGE'],
        error_out=False
    )
    users = pagination.items
    return render_template("admin/verify/schoolfellow_index.html", activities=users,
                           search_form=search_form,pagination=pagination)

#添加校友入会
@admin.route("/verify/add_schoolfellow",methods=['GET','POST'])
@login_required
@admin_required
def add_schoolfellow():
    form = enrollmentForm()
    if form.validate_on_submit():
        user = User(
            name = form.name.data,
            sex = form.sex.data,
            status = form.status.data,
            grade = form.grade.data,
            birthday = form.birthday.data,
            contact = form.contact.data,
            phone = form.phone.data,
            email = form.email.data,
            username = form.phone.data,
            password = str(form.phone.data)[3:]
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('project.admin.fellow_list'))
    return render_template('admin/verify/schoolfellow_add.html', form=form)




#企业入会登记
@admin.route("/verify/company",methods=['GET','POST'])
@login_required
@admin_required
def company_list():
    search_form = SearchAlumniForm()
    if search_form.validate_on_submit():
        keywords = search_form.keywords.data
        activities = Enterprise.query.filter(or_(Enterprise.CoporateName.like('%' + keywords + '%'))).all()
        return render_template('admin/verify/company_verify.html', search_form=search_form,
                               activities=activities)
    page = request.args.get('page', 1, type=int)
    user = Enterprise.query.filter(not_(Enterprise.user_id == '1'))
    pagination = user.filter(not_(Enterprise.CoporateName=='None')).paginate(
        page, per_page=current_app.config['FLASY_NEWS_PER_PAGE'],
        error_out=False
    )
    users = pagination.items
    return render_template("admin/verify/company_verify.html", activities=users,
                           search_form=search_form,pagination=pagination)

#入会审核api
@admin.route('/api/veriry_list',methods=['GET', 'POST'])
def verify_api():
    User_id = request.form.get('id')
    user = User.query.get(User_id)
    if not user.verify :
        user.verify = True#已审核
        db.session.add(user)
        db.session.commit()
        return '1'

#企业入会审核api
@admin.route('/api/enterprise/veriry_list',methods=['GET', 'POST'])
def enterprise_verify_api():
    User_id = request.form.get('id')
    user = Enterprise.query.get(User_id)
    if not user.verify :
        user.verify = True#已审核
        db.session.add(user)
        db.session.commit()
        return '1'
