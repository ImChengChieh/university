# -*- coding: UTF-8 -*-
import os
import re
import json
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import distinct, func

from flask import Flask, request, render_template, url_for, make_response, flash, redirect

from project.utils.uploader import Uploader
from . import main
from ..models import db, Article, FriendshipLink, ArticleType, alumni, ActivReleased, \
    VideoList, News, Interview, photoList, Banner, AlumniIntro, User_Activ, Cooperate, Recuit, \
    Contact  # Notice, School,
from flask import render_template, request, current_app, url_for
from sqlalchemy import or_, not_
import sqlalchemy as sa
from .preForms import memberForm, RegisterHomeForm, LoginHomeForm, CopMemberForm, CompetitionForm, modifyForm
from ..models import User
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime

# 视频活动
@main.route('/multimedia/video', methods=['GET', 'POST'])
def multimedia_video():
    video = VideoList.query.order_by(VideoList.title, VideoList.video).all()
    activs = ActivReleased.query.all()
    return render_template('home/multimedia_video.html', video=video, activs=activs)

#照片活动
@main.route('/multimedia/photo', methods=['GET', 'POST'])
def multimedia_photo():
    photos = photoList.query.order_by(photoList.title, photoList.photo).all()
    activs = ActivReleased.query.all()
    return render_template('home/multimedia_photo.html', photos=photos, activs=activs)


#分类活动图片集合
@main.route('/picture_video/gather/<int:activ_id>',methods=['GET', 'POST'])
def picture_gather(activ_id):
    activ_pic = ActivReleased.query.get(activ_id)
    return render_template('home/picture_more.html', activ_pic=activ_pic)

#分类活动视频集合
@main.route('/picture_video/gather_video/<int:activ_id>',methods=['GET', 'POST'])
def video_gather(activ_id):
    activ_video = ActivReleased.query.get(activ_id)
    return render_template('home/video_more.html', activ_video=activ_video)