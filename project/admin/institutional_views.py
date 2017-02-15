# -*- coding: UTF-8 -*-
import os
from werkzeug.utils import secure_filename
from ..decorators import modify_required
from flask import render_template, redirect, url_for,flash,request, current_app,jsonify
from project.models import ArticleType, Article, FriendshipLink
from . import admin
from flask_login import login_required,current_user
from ..decorators import admin_required
from .forms import AlumniForm,updateAlumniForm,ActivReleasedForm,UpdateActivForm,\
    SearchActivForm,VideoPublishForm,SearchAlumniForm,NewsForm,InterviewForm,\
    PhotoPublishForm,BannerForm,SummaryForm,UpdateSummaryForm,AddmemberForm,\
    SchoolForm,NoticeForm,AddmemberssForm,SearchAlumniForm,FriendlyLinkForm,updateLinkForm,\
    RecuitForm,CoperateForm,ModifyPswForm
from ..models import db,alumni,ActivReleased,VideoList,News,Interview,photoList,Banner,\
    AlumniIntro,User,Recuit,Cooperate,Contact    #School,Notice,
from sqlalchemy.sql.expression import or_,not_

from flask_mail import Message
from project import mail

#校友会简介
@admin.route('/summary',methods=['GET','POST'])
@login_required
def summary_list():
    page = request.args.get('page', 1, type=int)
    pagination = AlumniIntro.query.order_by(AlumniIntro.id).paginate(
        page,per_page=current_app.config['FLASY_BANNER_PER_PAGE'],
        error_out=False
    )
    intro = pagination.items
    return render_template('alumnusIntro/alumnusIntro_index.html', intro=intro,
                           pagination=pagination)

#编辑校友会简介
@admin.route('/summary/edit',methods=['GET', 'POST'])
@login_required
def edit_summary():
    form = SummaryForm()
    if form.validate_on_submit():
        intro = AlumniIntro(
            title=form.title.data,
            content=form.content.data,
        )
        db.session.add(intro)
        db.session.commit()
        # flash(u'添加成功。。。')
        return redirect(url_for('project.admin.summary_list'))
    return render_template('alumnusIntro/alumnusIntro_edit.html', form=form)

#修改校友会简介
@admin.route('/summary/update/<int:id>',methods=['GET','POST'])
@login_required
def update_summary(id):
    update_intro = AlumniIntro.query.get_or_404(id)
    form = UpdateSummaryForm()
    if form.validate_on_submit():
        update_intro.title = form.title.data
        update_intro.content = form.content.data
        db.session.add(update_intro)
        db.session.commit()
        flash('修改成功...')
        return redirect(url_for('project.admin.summary_list'))
    form.title.data = update_intro.title
    form.content.data = update_intro.content
    return render_template('alumnusIntro/alumnusIntro_edit.html',form=form)


#删除校友会简介
@admin.route("/summary/<int:id>",methods=['GET','POST'])
@login_required
@admin_required
def del_summary(id):
    # del_donations = addAlumni.query.order_by(addAlumni.id).all()
    del_summary = AlumniIntro.query.get_or_404(id)
    db.session.delete(del_summary)
    db.session.commit()
    return redirect(url_for('project.admin.summary_list'))

#校友联系名录
@admin.route("/contact",methods=['GET','POST'])
@login_required
@admin_required
def contact_list():
    search_form = SearchAlumniForm()
    if search_form.validate_on_submit():
        keywords = search_form.keywords.data
        activities = Contact.query.filter(or_(Contact.username.like('%' + keywords + '%'),
                                              Contact.CoporateName.like('%' + keywords + '%')
                                                    )).all()
        return render_template('Contact/contact_list.html', search_form=search_form,
                               activities=activities)
    page = request.args.get('page', 1, type=int)
    # user = User.query.filter(not_(User.username=='admin'))
    pagination = Contact.query.order_by(Contact.id).paginate(
        page, per_page=current_app.config['FLASY_NEWS_PER_PAGE'],
        error_out=False
    )
    users = pagination.items
    return render_template("Contact/contact_list.html", activities=users,
                           search_form=search_form,pagination=pagination)

#添加校友名录
@admin.route("/contact/add",methods=['GET','POST'])
@login_required
@admin_required
def contact_add():
    form = AddmemberForm()
    if form.validate_on_submit():
        user = Contact(
            username=form.username.data,
            CoporateName=form.CoporateName.data,
            grade = form.grade.data,
            phone=form.phone.data,
            email=form.email.data,
            weixin=form.weixin.data
        )
        db.session.add(user)
        db.session.commit()
        # flash(u'添加成功。。。')
        return redirect(url_for('project.admin.contact_list'))
    return render_template('Contact/contact_edit.html', form=form)

#编辑校友
@admin.route('/add_contact/edit/<int:id>',methods=['GET','POST'])
@login_required
def edit_contact(id):
    user = Contact.query.get_or_404(id)
    # search_form = SearchActivForm()
    form = AddmemberForm()

    if form.validate_on_submit():
        user.username = form.username.data
        # user.contact = form.contact.data
        user.CoporateName = form.CoporateName.data
        user.grade = form.grade.data
        user.phone = form.phone.data
        user.email = form.email.data
        user.weixin = form.weixin.data
        db.session.add(user)
        db.session.commit()
        # flash('修改成功...')
        return redirect(url_for('project.admin.contact_list'))
    form.username.data = user.username
    # form.contact.data = user.contact
    form.CoporateName.data = user.CoporateName
    form.grade.data = user.grade
    form.phone.data = user.phone
    form.email.data = user.email
    form.weixin.data=user.weixin
    return render_template('Contact/contact_edit.html',form=form)

#校友联络人删除提示api
@admin.route("/api/delete/user_contact",methods=['GET','POST'])
def api_user_contact_delete():
    User_id = request.form.get('id')
    user = Contact.query.get(User_id)
    db.session.delete(user)
    db.session.commit()
    return '1'