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

def random_file_name(filename):
    '''replace user uploads file with random file name '''
    file_extension = filename.rsplit('.', 1)[1]
    import uuid
    file_name = str(uuid.uuid4())
    return file_name + '.' + file_extension

#照片列表
@admin.route('/photo',methods=['GET','POST'])
@login_required
def photo():
    page = request.args.get('page', 1, type=int)
    pagination = photoList.query.order_by(photoList.id).paginate(
         page,per_page=current_app.config['FLASY_NEWS_PER_PAGE'],
         error_out=False
     )
    photo = pagination.items
    return render_template('video/photo_index.html',photo=photo,pagination=pagination)

#添加照片信息
@admin.route('/photo/add',methods=['GET','POST'])
@login_required
def add_photo():
    form = PhotoPublishForm()
    if form.validate_on_submit():
         photoes = photoList(
             activ_id = form.activ.data,
             title = form.title.data,
             time =  form.time.data
         )
         # photoes.activ.append(ActivReleased.query.get(form.activ.data))

         file = request.files['photo']
         filename = random_file_name(secure_filename(file.filename))
         # filename = file.filename
         APP_ROOT = os.path.dirname(os.path.dirname(__file__))
         UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/upload')
         file_path = os.path.join(UPLOAD_FOLDER, filename)
         file.save(file_path)
         file_path_name = filename
         photoes.photo = file_path_name

         db.session.add(photoes)
         db.session.commit()
         return redirect(url_for('project.admin.photo'))
    return render_template('video/photo_edit.html',form=form)

#照片资料删除提示api
@admin.route("/api/delete/photo",methods=['GET','POST'])
def api_photo_delete():
    photo_id = request.form.get('id')
    photo = photoList.query.get(photo_id)
    db.session.delete(photo)
    db.session.commit()
    return '1'

#视频列表
@admin.route('/video',methods=['GET','POST'])
@login_required
def video():
    page = request.args.get('page', 1, type=int)
    pagination = VideoList.query.order_by(VideoList.id).paginate(
         page,per_page=current_app.config['FLASY_NEWS_PER_PAGE'],
         error_out=False
     )
    videolist = pagination.items
    return render_template('video/video_index.html',videolist=videolist,pagination=pagination)

#添加视频信息
@admin.route('/video/add',methods=['GET','POST'])
@login_required
def add_video():
    form = VideoPublishForm()
    if form.validate_on_submit():
         videopuli = VideoList(
             title = form.title.data,
             time =  form.time.data,
             activ_id=form.activ.data,
         )
         # videopuli.activ.append(ActivReleased.query.get(form.activ.data))

         file = request.files['video']
         filename = random_file_name(secure_filename(file.filename))
         # filename = file.filename
         APP_ROOT = os.path.dirname(os.path.dirname(__file__))
         UPLOAD_FOLDER = os.path.join(APP_ROOT,'static/upload')
         file_path = os.path.join(UPLOAD_FOLDER, filename)
         file.save(file_path)
         file_path_name = filename
         videopuli.video = file_path_name

         db.session.add(videopuli)
         db.session.commit()
         return redirect(url_for('project.admin.video'))
    return render_template('video/video_edit.html',form=form)

#删除视频信息
@admin.route('/video/<int:id>',methods=['GET','POST'])
@login_required
def del_video(id):
    video_list = VideoList.query.get_or_404(id)
    db.session.delete(video_list)
    db.session.commit()
    return redirect(url_for('project.admin.video'))

#删除照片信息
@admin.route('/video/<int:id>',methods=['GET','POST'])
@login_required
def del_photo(id):
    photo_list = photoList.query.get_or_404(id)
    db.session.delete(photo_list)
    db.session.commit()
    return redirect(url_for('project.admin.photo'))

#视频删除提示api
@admin.route("/api/delete/video",methods=['GET','POST'])
def api_video_delete():
    video_id = request.form.get('id')
    video = VideoList.query.get(video_id)
    db.session.delete(video)
    db.session.commit()
    return '1'