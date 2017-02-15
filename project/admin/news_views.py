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

#文件随机名
def random_file_name(filename):
    '''replace user uploads file with random file name '''
    file_extension = filename.rsplit('.', 1)[1]
    import uuid
    file_name = str(uuid.uuid4())
    return file_name + '.' + file_extension

#banner新闻主页
@admin.route('/banner',methods=['GET','POST'])
@login_required
def banner_list():
    page = request.args.get('page',1,type=int)
    pagination = Banner.query.order_by(Banner.id).paginate(
        page,per_page=current_app.config['FLASY_NEWS_PER_PAGE'],
        error_out=False
    )
    bannerlist = pagination.items
    return render_template('Banner/banner_index.html',bannerlist=bannerlist,
                           pagination=pagination)


#banner添加
@admin.route('/banner/add',methods=['GET','POST'])
@login_required
def add_banner():
    form = BannerForm()
    if form.validate_on_submit():
        news = Banner(
            title = form.title.data,
            time = form.time.data,
            content = form.content.data,
            # keywords = form.keywords.data,
        )

        file = request.files['photo']
        filename = random_file_name(secure_filename(file.filename))
        # filename = file.filename
        APP_ROOT = os.path.dirname(os.path.dirname(__file__))
        UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/upload')
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        file_path_name = filename
        news.photo = file_path_name

        db.session.add(news)
        db.session.commit()
        return redirect(url_for('project.admin.banner_list'))
    return render_template('Banner/banner_add.html', form=form)

#banner新闻修改
@admin.route('/banner/update/<int:id>',methods=['GET','POST'])
@login_required
def update_banner(id):
    banner_update = Banner.query.get(id)
    banner_photo = Banner.query.filter_by(id=id).first()
    form = BannerForm()
    form.photo.validators =[]
    if form.validate_on_submit():
        banner_update.title = form.title.data
        banner_update.time = form.time.data
        banner_update.content = form.content.data
        # banner_update.keywords = form.keywords.data

        file = request.files['photo']
        filename = random_file_name(secure_filename(file.filename))
        # file_path_name = random_file_name(secure_filename(file.filename))
        if filename:
            APP_ROOT = os.path.dirname(os.path.dirname(__file__))
            UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/upload')
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            file_path_name = filename
            banner_update.photo = file_path_name

        db.session.add(banner_update)
        db.session.commit()
        return redirect(url_for('project.admin.banner_list'))
    form.title.data = banner_update.title
    form.time.data = banner_update.time
    form.content.data = banner_update.content
    # form.keywords.data = banner_update.keywords
    return render_template('Banner/banner_edit.html', form=form,banner_photo=banner_photo)


#删除Banner信息
@admin.route('/banner/<int:id>',methods=['GET','POST'])
@login_required
def del_banner(id):
    Banner_list = Banner.query.get_or_404(id)
    db.session.delete(Banner_list)
    db.session.commit()
    return redirect(url_for('project.admin.banner_list'))

#Banner删除提示api
@admin.route("/api/delete",methods=['GET','POST'])
def api_banner_delete():
    Banner_id = request.form.get('id')
    banner = Banner.query.get(Banner_id)
    db.session.delete(banner)
    db.session.commit()
    return '1'

#校友会新闻
@admin.route('/news',methods=['GET','POST'])
@login_required
def news_list():
    page = request.args.get('page', 1, type=int)
    pagination = News.query.order_by(News.id).paginate(
        page,per_page=current_app.config['FLASY_NEWS_PER_PAGE'],
        error_out=False
    )
    newslist = pagination.items
    return render_template('News/news_index.html',newslist=newslist,
                           pagination=pagination)

#新闻置顶api
@admin.route('/api/top',methods=['GET','POST'])
def api_news_top():
    news_id = request.form.get('id')
    news = News.query.get(news_id)
    if not news.isTop:
        news.isTop = 1
        db.session.add(news)
        db.session.commit()
        return '1'
    else:
        news.isTop = 0
        db.session.add(news)
        db.session.commit()
        return '0'


#新闻添加
@admin.route('/news/add',methods=['GET','POST'])
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        news = News(
            type = form.type.data,
            title = form.title.data,
            time = form.time.data,
            content = form.content.data
        )

        file = request.files['photo']
        filename = random_file_name(secure_filename(file.filename))
        # filename = file.filename
        APP_ROOT = os.path.dirname(os.path.dirname(__file__))
        UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/upload')
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        file_path_name = filename
        news.photo = file_path_name

        db.session.add(news)
        db.session.commit()
        return redirect(url_for('project.admin.news_list'))
    return render_template('News/news_add.html', form=form)

#新闻修改
@admin.route('/news/update/<int:id>',methods=['GET','POST'])
@login_required
def update_news(id):
    form = NewsForm()
    news_update = News.query.get(id)
    news_photo = News.query.filter_by(id=id).first()
    if form.validate_on_submit():
        news_update.type = form.type.data
        news_update.title = form.title.data
        news_update.time = form.time.data
        news_update.content = form.content.data

        file = request.files['photo']
        filename = random_file_name(secure_filename(file.filename))
        # filename = file.filename
        if filename:
            APP_ROOT = os.path.dirname(os.path.dirname(__file__))
            UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/upload')
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            file_path_name = filename
            news_update.photo = file_path_name

        db.session.add(news_update)
        db.session.commit()
        return redirect(url_for('project.admin.news_list'))

    form.title.data = news_update.title
    form.time.data = news_update.time
    form.content.data = news_update.content
    form.photo.data = news_update.photo
    form.type.data = news_update.type
    return render_template('News/news_edit.html', form=form,news_photo=news_photo)


#删除新闻信息
@admin.route('/news/delete/<int:id>',methods=['GET','POST'])
@login_required
def del_news(id):
    News_list = News.query.get_or_404(id)
    db.session.delete(News_list)
    db.session.commit()
    return redirect(url_for('project.admin.news_list'))

#校友会删除提示api
@admin.route("/api/delete/alunmi",methods=['GET','POST'])
def api_alunmi_delete():
    News_id = request.form.get('id')
    news = News.query.get(News_id)
    db.session.delete(news)
    db.session.commit()
    return '1'

#校友专访
@admin.route('/interview',methods=['GET','POST'])
@login_required
def interview_list():
    page = request.args.get('page', 1, type=int)
    pagination = Interview.query.order_by(Interview.id).paginate(
         page,per_page=current_app.config['FLASY_NEWS_PER_PAGE'],
         error_out=False
     )
    interview = pagination.items
    return render_template('Interview/Interview_index.html', interview=interview,
                           pagination=pagination)

#添加校友专访
@admin.route('/interview/add',methods=['GET','POST'])
@login_required
def add_interview():
    form = InterviewForm()
    if form.validate_on_submit():
        interview = Interview(
            title=form.title.data,
            time=form.time.data,
            content=form.content.data,
        )

        file = request.files['photo']
        filename = random_file_name(secure_filename(file.filename))
        # filename = file.filename
        APP_ROOT = os.path.dirname(os.path.dirname(__file__))
        UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/upload')
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        file_path_name = filename
        interview.photo = file_path_name

        db.session.add(interview)
        db.session.commit()
        return redirect(url_for('project.admin.interview_list'))
    return render_template('Interview/Interview_add.html', form=form)

#修改校友专访
@admin.route('/interview/update/<int:id>',methods=['GET','POST'])
@login_required
def updte_interview(id):
    interview_updte = Interview.query.get(id)
    form = InterviewForm()
    if form.validate_on_submit():
        interview_updte.title=form.title.data
        interview_updte.time=form.time.data
        interview_updte.content=form.content.data

        file = request.files['photo']
        filename = random_file_name(secure_filename(file.filename))
        # filename = file.filename
        if filename:
            APP_ROOT = os.path.dirname(os.path.dirname(__file__))
            UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/upload')
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            file_path_name = filename
            interview_updte.photo = file_path_name

        db.session.add(interview_updte)
        db.session.commit()
        return redirect(url_for('project.admin.interview_list'))
    form.title.data=interview_updte.title
    form.time.data=interview_updte.time
    form.content.data=interview_updte.content
    form.photo.data =interview_updte.photo
    return render_template('Interview/Interview_edit.html', form=form,interview_updte=interview_updte)

#删除校友专访
@admin.route('/interview/<int:id>',methods=['GET','POST'])
@login_required
def del_interview(id):
    Interview_list = Interview.query.get_or_404(id)
    db.session.delete(Interview_list)
    db.session.commit()
    return redirect(url_for('project.admin.interview_list'))

#校友专访删除提示api
@admin.route("/api/delete/interview",methods=['GET','POST'])
def api_interview_delete():
    News_id = request.form.get('id')
    interview = Interview.query.get(News_id)
    db.session.delete(interview)
    db.session.commit()
    return '1'

#校友招聘
@admin.route('/recuit',methods=['GET','POST'])
@login_required
def recuit_list():
    page = request.args.get('page', 1, type=int)
    pagination = Recuit.query.order_by(Recuit.id).paginate(
        page,per_page=current_app.config['FLASY_BANNER_PER_PAGE'],
        error_out=False
    )
    recuitmen = pagination.items
    return render_template('recuitment/recuitment_index.html', recuitmen=recuitmen,
                           pagination=pagination)

#编辑校友招聘
@admin.route('/recuit/edit',methods=['GET', 'POST'])
@login_required
def edit_recuit():
    form = RecuitForm()
    if form.validate_on_submit():
        recuit = Recuit(
            title=form.title.data,
            content=form.content.data,
        )
        db.session.add(recuit)
        db.session.commit()
        # flash(u'添加成功。。。')
        return redirect(url_for('project.admin.recuit_list'))
    return render_template('recuitment/recuitment_edit.html', form=form)

#修改校友招聘
@admin.route('/recuit/update/<int:id>',methods=['GET','POST'])
@login_required
def update_recuit(id):
    update_recuit = Recuit.query.get_or_404(id)
    form = RecuitForm()
    if form.validate_on_submit():
        update_recuit.title = form.title.data
        update_recuit.content = form.content.data
        db.session.add(update_recuit)
        db.session.commit()
        flash('修改成功...')
        return redirect(url_for('project.admin.recuit_list'))
    form.title.data = update_recuit.title
    form.content.data = update_recuit.content
    return render_template('recuitment/recuitment_update.html',form=form)

#互助合作
@admin.route('/cooperate',methods=['GET','POST'])
@login_required
def cooperate_list():
    page = request.args.get('page', 1, type=int)
    pagination = Cooperate.query.order_by(Cooperate.id).paginate(
        page,per_page=current_app.config['FLASY_BANNER_PER_PAGE'],
        error_out=False
    )
    cooperate = pagination.items
    return render_template('cooperate/cooperate_index.html', cooperate=cooperate,
                           pagination=pagination)

#添加合作互助
@admin.route('/cooperate/edit',methods=['GET', 'POST'])
@login_required
def edit_cooperate():
    form = CoperateForm()
    if form.validate_on_submit():
        cooperate = Cooperate(
            title=form.title.data,
            content=form.content.data,
        )
        db.session.add(cooperate)
        db.session.commit()
        # flash(u'添加成功。。。')
        return redirect(url_for('project.admin.cooperate_list'))
    return render_template('cooperate/cooperate_edit.html', form=form)

#修改互助合作
@admin.route('/cooperate/update/<int:id>',methods=['GET','POST'])
@login_required
def update_cooperate(id):
    update_cooperate = Cooperate.query.get_or_404(id)
    form = CoperateForm()
    if form.validate_on_submit():
        update_cooperate.title = form.title.data
        update_cooperate.content = form.content.data
        db.session.add(update_cooperate)
        db.session.commit()
        flash('修改成功...')
        return redirect(url_for('project.admin.cooperate_list'))
    form.title.data = update_cooperate.title
    form.content.data = update_cooperate.content
    return render_template('cooperate/cooperate_update.html',form=form)