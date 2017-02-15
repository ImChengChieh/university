#!/user/bin/env python
# -*- coding: utf-8 -*-

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
    Contact,Enterprise
from flask import render_template, request, current_app, url_for
from sqlalchemy import or_, not_
import sqlalchemy as sa
from .preForms import memberForm, RegisterHomeForm, LoginHomeForm, CopMemberForm, CompetitionForm, \
    modifyForm,modifyEmailForm,ModifyPhoneForm
from ..models import User
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime

@main.errorhandler(404)
def page_not_found(e):
    return render_template('home/404.html'),404


@main.route('/')
def index():
    # 置顶新闻
    top_new = Article.query.filter_by(top_to_index=True).first()
    # 校友会简介
    intro = AlumniIntro.query.order_by(AlumniIntro.content).first()
    # banner新闻
    # banner_news = Article.query.filter(Article.type_id == 6).order_by(Article.id.desc()).all()
    banner_news = Banner.query.filter(Banner.id).order_by(Banner.id.desc()).limit(3).all()
    # 校友会新闻和学校新闻
    news = Article.query.filter(or_(Article.type_id == 1, Article.type_id == 2)).order_by(Article.id.desc()).limit(
        8).all()
    # 校友专访
    alumni_talks = Article.query.filter_by(type_id=4).order_by(Article.id.desc()).limit(4).all()
    # 友情链接
    friend_links = FriendshipLink.query.order_by(FriendshipLink.id.desc()).limit(5)
    # 新增校友
    alumnis = User.query.filter(not_(User.name == 'None'))
    add_alumnis = alumnis.filter(User.verify != 0).all()
    # 企业名单
    alumni_enterprise = alumni.query.order_by(alumni.department, alumni.name).all()
    # 活动题目
    activ_released = ActivReleased.query.filter(ActivReleased.id).order_by(ActivReleased.id.desc()).limit(3).all()
    # 视频文件
    video_list = photoList.query.filter(photoList.id).limit(1).all()
    # 动态新闻
    news_list = News.query.filter(News.id).order_by(News.isTop.desc()).limit(9).all()
    # 校友专访
    inter_alumni_index = Interview.query.filter(Interview.id).order_by(Interview.id.desc()).limit(4).all()
    return render_template('home/index.html', news=news, alumni_talks=alumni_talks, top_new=top_new,
                           friend_links=friend_links, banner_news=banner_news, add_alumni=add_alumnis,
                           alumni_enterprise=alumni_enterprise, activ_released=activ_released,
                           video_list=video_list, news_list=news_list, inter_alumni_index=inter_alumni_index,
                           intro=intro)


# 用户注册
@main.route('/register', methods=['GET', 'POST'])
def index_register():
    form = RegisterHomeForm()
    if form.validate_on_submit():
        user_in = User(
            username=form.username.data,
            password=form.password.data,
        )
        db.session.add(user_in)
        db.session.commit()
        flash(u'恭喜你注册成功，您可以在下方进行登陆。')
        return redirect(url_for('project.main.index_enter'))
    return render_template('home/index_register.html', form=form)


# 登录
@main.route('/login', methods=['GET', 'POST'])
def index_enter():
    form = LoginHomeForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None:
            if user.state == 0:
                flash('账号已冻结请联系管理员！')
            else:
                if user is not None and user.verify_passwrod(form.password.data):
                    login_user(user)
                    return redirect(request.args.get('next') or url_for('project.main.index'))
                flash('用户名或者密码错误.')
    return render_template('home/index_enters.html', form=form)


# 个人中心修改密码
@main.route('/modify/password', methods=['GET', 'POST'])
def index_password():
    form = modifyForm()
    # form = ModifyPhoneForm()
    user = User.query.get(current_user.get_id())
    if form.validate_on_submit():
        if current_user.verify_passwrod(form.old_password.data):
            user.password = form.new_password.data
            db.session.add(user)
            db.session.commit()
            flash('修改成功')
            return redirect(url_for('project.main.index'))
        else:
            flash('原密码错误')
    return render_template('home/change_password.html', form=form)

# #个人中心修改电话号码
# @main.route("/api/phone", methods=['GET', 'POST'])
# def modifyPhone():
#     old_phone = request.form.get('old_phone')
#     if current_user.phone != int(old_phone):
#         pass
#     else:
#         phone = request.form.get('new_phone')
#         current_user.phone = phone
#         db.session.add(current_user)
#         db.session.commit()
#     return ''


# 个人中心企业信息
@main.route('/modify/enterprise/<int:id>', methods=['GET', 'POST'])
def index_enterprise(id):
    company_detail = Enterprise.query.filter_by(user_id=id).all()
    return render_template('home/user_center_enterprise.html',company_detail=company_detail)


# 个人中心入会信息
@main.route('/modify/user/<int:id>', methods=['GET', 'POST'])
def index_modify(id):
    user_detail = User.query.get_or_404(id)
    form = modifyEmailForm()
    if form.validate_on_submit():
        old_email = form.old_email.data
        if old_email == current_user.email:
            current_user.email = form.new_email.data
            db.session.add(current_user)
            db.session.commit()

    preform = ModifyPhoneForm()
    if preform.validate_on_submit():
        old_phone = preform.old_phone.data
        if int(old_phone) == current_user.phone:
            current_user.phone = preform.new_phone.data
            db.session.add(current_user)
            db.session.commit()
    return render_template('home/user_center.html',user_detail=user_detail,
                           form=form,preform=preform)


# 校友专访
@main.route('/alumni_interview', methods=['GET', 'POST'])
def alumni_inter():
    page = request.args.get('page', 1, type=int)
    pagination = Interview.query.order_by(Interview.id).paginate(
        page, per_page=current_app.config['FLASY_NEWS_PER_PAGE'],
        error_out=False
    )
    inter_alumni = pagination.items
    return render_template('home/alumni_interview.html', pagination=pagination, inter_alumni=inter_alumni)


# 校友专访详情
@main.route('/alumni_interview/detail/<int:id>')
def alumni_interview_details(id):
    interview_details = Interview.query.get(id)
    return render_template('home/alumni_interview_details.html', interview_details=interview_details)


# banner详情
@main.route('/banner_news/banner/<int:id>')
def banner_news(id):
    banner_detail = Banner.query.get(id)
    return render_template('home/banner_detail.html', banner_detail=banner_detail)


# 校友会简介介绍
@main.route('/summary', methods=['GET', 'POST'])
def summary():
    intro = AlumniIntro.query.order_by(AlumniIntro.content).first()
    return render_template('home/summary.html', Alumni_Intro=intro)


# 校友招聘
@main.route('/recruit', methods=['GET', 'POST'])
def recruit():
    reccuit = Recuit.query.order_by(Recuit.id).all()
    return render_template('home/recruit.html', reccuit=reccuit)


# 校友互助
@main.route('/cooperate', methods=['GET', 'POST'])
def cooperate():
    operate = Cooperate.query.order_by(Cooperate.id).all()
    return render_template('home/cooperate.html', operate=operate)


# 校友名录
@main.route('/user', methods=['GET', 'POST'])
def user():
    user = User.query.order_by(User.id)
    username = user.filter(not_(User.username == 'admin'))
    users = username.filter(not_(User.name == 'None')).all()
    user_count = username.filter(not_(User.name == 'None')).count()
    return render_template('home/user.html',user=users,user_count=user_count)


# 校友联络人
@main.route('/contact_user', methods=['GET', 'POST'])
def contact_user():
    users = Contact.query.order_by(Contact.id).all()
    # users= user.filter(not_(User.name == 'None')).all()
    return render_template('home/contact_user.html', user=users)


# 捐赠名录
@main.route('/donation', methods=['GET', 'POST'])
def donation():
    donation = alumni.query.filter(not_(User.username == 'admin')).all()
    return render_template('home/donations.html', donation=donation)


# 查看所有入会企业
@main.route('/enterprise', methods=['GET', 'POST'])
def enter():
    enterprise = Enterprise.query.filter(not_(Enterprise.user_id == '1'))
    enterprises = enterprise.filter(not_(Enterprise.CoporateName)).all()
    return render_template('home/enterprise.html', enterprise=enterprises)


# 校友会员通道
@main.route('/member', methods=['GET', 'POST'])
# @login_required
def member():
    form = memberForm()
    user = User.query.filter_by(username=current_user.username).first()
    # user = User()
    if form.validate_on_submit():
        user.name = form.name.data
        user.sex = form.sex.data
        user.status = form.status.data
        user.grade = form.grade.data
        user.birthday = form.birthday.data
        user.contact = form.contact.data
        user.identInfor = form.identInfor.data
        user.phone = form.phone.data
        user.email = form.email.data
        db.session.add(user)
        # try:
        db.session.commit()
        # except SQLAlchemyError, e:
        #     print e
        # flash('您现在可以登录了!')
        return redirect(url_for('project.main.transfer'))
    # form.username.data = user.username
    return render_template('home/member.html', form=form)

#页面提示
@main.route('/member/transfer',methods=['GET', 'POST'])
def transfer():
    return render_template('home/skip.html')

# 企业会员通道
@main.route('/CoporateMember', methods=['GET', 'POST'])
def CorporateMember():
    form = CopMemberForm()
    enterprise = Enterprise()
    # user = User.query.filter_by(username=current_user.username).first()
    if form.validate_on_submit():
        enterprise.CoporateName = form.name.data
        enterprise.CoporatePerson = form.legalPerson.data
        enterprise.CoporateScale = form.scale.data
        enterprise.corProperty = form.corProperty.data
        enterprise.type = form.type.data
        enterprise.CoporateIntro = form.intro.data
        enterprise.contact = form.contact.data
        enterprise.phone = form.phone.data
        enterprise.user_id = current_user.id
        enterprise.province=current_user.province
        enterprise.city = current_user.city
        db.session.add(enterprise)
        db.session.commit()
        return redirect(url_for('project.main.transfer'))
    return render_template('home/CorporateMember.html', form=form)


# 登出用户
@main.route('/logout')
def logout():
    logout_user()
    # flash(u'您已经退出')
    return redirect(url_for('project.main.index'))


# 专访详情页
@main.route('/talk/detail/<int:id>')
def talk_detail(id):
    news = Article.query.get_or_404(id)
    news.clicked = (news.clicked or 0) + 1
    db.session.add(news)
    db.session.commit()
    return render_template("home/talk_detail.html", news=news)


# 校友会章程
@main.route('/org/rule')
def org_rule():
    return render_template('home/org_rule.html')


# 友情链接
@main.route('/links', methods=['GET', 'POST', 'OPTIONS'])
def friendlink():
    links = FriendshipLink.query.order_by(FriendshipLink.id).all()
    return render_template("home/friendlink.html", links=links)


# 地理位置获取省份api enterprise.user_id
@main.route("/api/province", methods=['GET', 'POST'])
def api_province():
    province = request.form.get('s_province')
    current_user.province = province
    db.session.add(current_user)
    db.session.commit()
    return ''



# 地理位置获取地级市api
@main.route("/api/city", methods=['GET', 'POST'])
def api_city():
    city = request.form.get('s_city')
    current_user.city = city
    db.session.add(current_user)
    db.session.commit()
    return ''


@main.route('/upload/', methods=['GET', 'POST', 'OPTIONS'])
def upload():
    """UEditor文件上传接口

    config 配置文件
    result 返回结果
    """
    mimetype = 'application/json'
    result = {}
    action = request.args.get('action')

    # 解析JSON格式的配置文件
    with open(os.path.join(current_app.static_folder, 'vendors', 'ueditor', 'php',
                           'config.json')) as fp:
        try:
            # 删除 `/**/` 之间的注释
            CONFIG = json.loads(re.sub(r'\/\*.*\*\/', '', fp.read()))
        except:
            CONFIG = {}

    if action == 'config':
        # 初始化时，返回配置文件给客户端
        result = CONFIG

    elif action in ('uploadimage', 'uploadfile', 'uploadvideo'):
        # 图片、文件、视频上传
        if action == 'uploadimage':
            fieldName = CONFIG.get('imageFieldName')
            config = {
                "pathFormat": CONFIG['imagePathFormat'],
                "maxSize": CONFIG['imageMaxSize'],
                "allowFiles": CONFIG['imageAllowFiles']
            }
        elif action == 'uploadvideo':
            fieldName = CONFIG.get('videoFieldName')
            config = {
                "pathFormat": CONFIG['videoPathFormat'],
                "maxSize": CONFIG['videoMaxSize'],
                "allowFiles": CONFIG['videoAllowFiles']
            }
        else:
            fieldName = CONFIG.get('fileFieldName')
            config = {
                "pathFormat": CONFIG['filePathFormat'],
                "maxSize": CONFIG['fileMaxSize'],
                "allowFiles": CONFIG['fileAllowFiles']
            }

        if fieldName in request.files:
            field = request.files[fieldName]
            uploader = Uploader(field, config, current_app.static_folder)
            result = uploader.getFileInfo()
        else:
            result['state'] = '上传接口出错'

    elif action in ('uploadscrawl'):
        # 涂鸦上传
        fieldName = CONFIG.get('scrawlFieldName')
        config = {
            "pathFormat": CONFIG.get('scrawlPathFormat'),
            "maxSize": CONFIG.get('scrawlMaxSize'),
            "allowFiles": CONFIG.get('scrawlAllowFiles'),
            "oriName": "scrawl.png"
        }
        if fieldName in request.form:
            field = request.form[fieldName]
            uploader = Uploader(field, config, current_app.static_folder, 'base64')
            result = uploader.getFileInfo()
        else:
            result['state'] = '上传接口出错'

    elif action in ('catchimage'):
        config = {
            "pathFormat": CONFIG['catcherPathFormat'],
            "maxSize": CONFIG['catcherMaxSize'],
            "allowFiles": CONFIG['catcherAllowFiles'],
            "oriName": "remote.png"
        }
        fieldName = CONFIG['catcherFieldName']

        if fieldName in request.form:
            # 这里比较奇怪，远程抓图提交的表单名称不是这个
            source = []
        elif '%s[]' % fieldName in request.form:
            # 而是这个
            source = request.form.getlist('%s[]' % fieldName)

        _list = []
        for imgurl in source:
            uploader = Uploader(imgurl, config, current_app.static_folder, 'remote')
            info = uploader.getFileInfo()
            _list.append({
                'state': info['state'],
                'url': info['url'],
                'original': info['original'],
                'source': imgurl,
            })

        result['state'] = 'SUCCESS' if len(_list) > 0 else 'ERROR'
        result['list'] = _list

    else:
        result['state'] = '请求地址出错'

    result = json.dumps(result)

    if 'callback' in request.args:
        callback = request.args.get('callback')
        if re.match(r'^[\w_]+$', callback):
            result = '%s(%s)' % (callback, result)
            mimetype = 'application/javascript'
        else:
            result = json.dumps({'state': 'callback参数不合法'})

    res = make_response(result)
    res.mimetype = mimetype
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Headers'] = 'X-Requested-With,X_Requested_With'
    return res

# 文章列表页面
# @main.route('/article/list/', methods=['GET', 'POST'])
# def article_list():
#     page = request.args.get('page', 1, type=int)
#     type_id = request.args.get('type_id', 1, type=int)
#     type_name = ArticleType.query.filter_by(id=type_id).first().name
#     # 热门文章
#     hot = Article.query.filter(sa.and_(Article.img != None, Article.type_id == type_id)).order_by(
#         Article.clicked.desc()).limit(5).all()
#
#     # 最新文章
#     newest = Article.query.filter(sa.and_(Article.img != None, Article.type_id == type_id)).order_by(
#         Article.create_at.desc()).limit(5).all()
#
#     # 文章分页列表
#     article_l = Article.query.filter_by(type_id=type_id).order_by(Article.id.desc()). \
#         paginate(page=page,
#                  per_page=
#                  current_app.config[
#                      'ARTICLE_LIST_LEN'],
#                  error_out=False)
#     return render_template("article/list.html", article_l=article_l, hot=hot, newest=newest, type_id=type_id,
#                            type_name=type_name)


# 搜索页
# @main.route('/search', methods=['get', 'post'])
# def search():
#     page = request.args.get('page', type=int) or 1
#     keywords = request.args.get('keywords') or request.form.get('keywords', type=str) or ''
#
#     # 热门文章
#     hot = Article.query.filter(Article.img != None).order_by(
#         Article.clicked.desc()).limit(5).all()
#
#     # 最新文章
#     newest = Article.query.filter(Article.img != None).order_by(
#         Article.create_at.desc()).limit(
#         5).all()
#
#     # 文章分页列表
#     article_l = Article.query.filter(Article.title.like('%' + keywords + '%')).order_by(Article.id.desc()). \
#         paginate(page=page,
#                  per_page=
#                  current_app.config[
#                      'ARTICLE_LIST_LEN'],
#                  error_out=False)
#     return render_template("search.html", article_l=article_l, hot=hot, newest=newest, keywords=keywords)
