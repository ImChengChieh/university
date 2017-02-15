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

# 组织活动，活动专栏-》活动详情
@main.route('/activity_apply', methods=['GET', 'POST'])
def activity_apply():
    page = request.args.get('page', 1, type=int)
    pagination = ActivReleased.query.filter(ActivReleased.id).order_by(ActivReleased.id.desc()).paginate(
        page, per_page=current_app.config['FLASY_NEWS_PER_PAGE'],
        error_out=False
    )
    activ_releaslist = pagination.items
    return render_template('home/activity_apply.html', activ_releaslist=activ_releaslist,
                           current_time=datetime.date(datetime.now()), pagination=pagination)

# 活动回顾
@main.route('/activity_review', methods=['GET', 'POST'])
def activity_review():
    activity_review = ActivReleased.query.order_by(ActivReleased.id).all()
    return render_template('home/activity_review.html', activity_review=activity_review,
                           current_time=datetime.date(datetime.now()))

# 报名活动
@main.route('/api/part', methods=['GET', 'POST'])
def part():
    active_id = request.form.get('data-use')
    # find activity
    active = ActivReleased.query.get(active_id)  # 查询活动对应映射关系，即对应数据库的一行
    # 查询当前用户以及ID是否存在
    if current_user in active.users.all():  # 当前用户在活动表中关系
        return '2'

    # active.users.append(current_user)#活动表中添加参加活动的用户，中间表中自动添加，完全可以忽略中间关系表
    current_user.tb_activreleased.append(active)
    try:
        db.session.add(active)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return '0'

    return '1'

# 组织活动详情
@main.route('/activity_apply/details/<int:id>', methods=['GET', 'POST'])
def activity_apply_details(id):
    activ_released = ActivReleased.query.get(id)
    return render_template('home/activity_apply_details.html', activ=activ_released,
                           current_time=datetime.date(datetime.now()))
