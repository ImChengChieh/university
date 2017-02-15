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

# 导航栏动态新闻
@main.route('/news/new_alumni', methods=['GET', 'POST'])
def new_alumni():
    page = request.args.get('page', 1, type=int)
    pagination = News.query.filter(News.type == 0).order_by(News.id.desc()).paginate(
        page, per_page=current_app.config['FLASY_NEWS_PER_PAGE'],
        error_out=False
    )
    news_alumni = pagination.items
    return render_template('home/new_alumni.html', news_alumni=news_alumni, pagination=pagination)


# 新闻动态-》校友会新闻详情
@main.route('/new_alumni_SingleNews/<int:id>', methods=['GET', 'POST'])
def new_alumni_SingleNews(id):
    alumni_detail = News.query.get(id)
    return render_template('home/new_alumni_SingleNews.html', alumni_detail=alumni_detail)


# 新闻动态-》学校公告
@main.route('/news/notice', methods=['GET', 'POST'])
def school_notice():
    page = request.args.get('page', 1, type=int)
    pagination = News.query.filter(News.type == 2).order_by(News.id.desc()).paginate(
        page, per_page=current_app.config['FLASY_NEWS_PER_PAGE'],
        error_out=False
    )
    notice_list = pagination.items
    return render_template('home/school_notice.html', notice_list=notice_list, pagination=pagination)



# 新闻动态-》学校新闻
@main.route('/news/school_news', methods=['GET', 'POST'])
def school_news_list():
    page = request.args.get('page', 1, type=int)
    pagination = News.query.filter(News.type == 1).order_by(News.id.desc()).paginate(
        page, per_page=current_app.config['FLASY_NEWS_PER_PAGE'],
        error_out=False
    )
    school_list = pagination.items
    return render_template('home/scholl_news_list.html', school_list=school_list,pagination=pagination)

# 学校新闻
@main.route('/news/school')
def school_news():
    page = request.args.get('page', 1, type=int)
    pager = Article.query.filter_by(type_id=2).order_by(Article.id.desc()) \
        .paginate(page=page,per_page=current_app.config['ARTICLE_LIST_LEN'],
                  error_out=False)
    news_list = pager.items
    return render_template('home/school_news.html', pager=pager, news_list=news_list)