#!/user/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from collections import OrderedDict
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager
from project import db


# 文章类型
class ArticleType(db.Model):
    __tablename__ = "tb_article_type"
    # 编号
    id = db.Column(db.Integer, primary_key=True)
    # 类型名称
    name = db.Column(db.String(20), nullable=False)
    # 上级ID
    superior = db.Column(db.Integer, default=0)

    @staticmethod
    def init_data():
        print "Note:"
        print "Init article type..."
        types = [u"校友会新闻", u"学校新闻", u"组织机构", u"校友专访", u"通知公告", u"banner新闻"]
        for type_name in types:
            type_ = ArticleType()
            type_.name = type_name
            db.session.add(type_)
        db.session.commit()
        print "Note:"
        print "Successful!"

    def __str__(self):
        return self.name


# 文章
class Article(db.Model):
    __tablename__ = "tb_articles"

    # 编号
    id = db.Column(db.Integer, primary_key=True)
    # 发布日期
    create_at = db.Column(db.DateTime, default=datetime.utcnow())
    # 文章类型
    type_id = db.Column(db.Integer, db.ForeignKey("tb_article_type.id"))
    type = db.relationship("ArticleType")
    # 标题
    title = db.Column(db.String(255), nullable=False)
    # 封面图片地址
    img = db.Column(db.String(255))
    # 文章类容
    content = db.Column(db.Text)
    # 排序
    rank = db.Column(db.Integer, default=0)
    # seo标题
    seo_title = db.Column(db.Text)
    # seo关键字
    seo_keywords = db.Column(db.Text)
    # seo描述信息
    seo_description = db.Column(db.Text)
    # 作者
    author = db.Column(db.String(64))
    # 文章来源
    source = db.Column(db.String(255))
    # 点击量
    clicked = db.Column(db.Integer, default=0)
    # 置顶
    top = db.Column(db.Boolean, default=False)
    # 首页置顶
    top_to_index = db.Column(db.Boolean, default=False)


# 活动-用户多对多表


# 活动表
class Activity(db.Model):
    __tablename__ = "tb_activities"
    id = db.Column(db.Integer, primary_key=True)
    # 标题
    title = db.Column(db.String(255), nullable=False)
    # 发布日期
    create_at = db.Column(db.DateTime, default=datetime.utcnow())
    # 封面图片地址
    img = db.Column(db.String(255))
    # 文章类容
    content = db.Column(db.Text)
    # 点击量
    clicked = db.Column(db.Integer, default=0)
    # 置顶
    top = db.Column(db.Boolean, default=False)
    # 是否开启
    is_active = db.Column(db.Boolean, default=True)


# 友情链接
class FriendshipLink(db.Model):
    __tablename__ = 'tb_friendshiplink'
    # 编号
    id = db.Column(db.Integer, primary_key=True)
    # 标题
    title = db.Column(db.String(255), nullable=False)
    # 链接地址
    link = db.Column(db.String(255), nullable=False)
    # 封面图片地址
    img = db.Column(db.String(255))


# 权限
class Permission:
    FOLLOW = 0x01  # 游客
    CHECK = 0X02  # 检查
    WRITE_ARTICLES = 0X04  # 添加文章
    ADMINISTER = 0X80  # 管理员


# 角色表
class Role(db.Model):
    __tablename__ = "tb_roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)

    # users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {'User': (Permission.FOLLOW |
                          Permission.CHECK, True),

                 'Moderator': (Permission.FOLLOW |
                               Permission.CHECK |
                               Permission.WRITE_ARTICLES, False),
                 'Administator': (0xff, False)
                 }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
            db.session.commit()


class User(UserMixin, db.Model):
    __tablename__ = "tb_users"
    id = db.Column(db.Integer, primary_key=True)
    # 用户名
    username = db.Column(db.String(255), unique=True, index=True)
    # 密码
    password_hash = db.Column(db.String(128))
    # 注册时间
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    # 真实姓名
    name = db.Column(db.String(64))
    # 真实姓名
    province = db.Column(db.String(64))
    city = db.Column(db.String(64))
    # 最后登陆时间
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    # 角色外键id
    role_id = db.Column(db.Integer, db.ForeignKey('tb_roles.id'), default=3)
    # 个人简介
    about_me = db.Column(db.Text())

    # 性别
    sex = db.Column(db.Boolean(), default=0)
    # 身份选择
    status = db.Column(db.Integer())
    # 入学班级
    grade = db.Column(db.String(255))
    # 联系人
    contact = db.Column(db.String(255))
    # 出身日期
    birthday = db.Column(db.Date)
    # 验证信息
    identInfor = db.Column(db.Text)
    # 电话
    phone = db.Column(db.BigInteger())
    # 邮箱
    email = db.Column(db.String(255), index=True)

    # 账号状态。1默认激活状态
    state = db.Column(db.Boolean, default=1)
    # 入会审核,0默认为审核中
    verify = db.Column(db.Boolean, default=0)
    enter = db.relationship('Enterprise', backref=db.backref('tb_users'),uselist=False )

    @property
    def password(self):
        raise AttributeError(u'密码不可读取')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_passwrod(self, password):
        return check_password_hash(self.password_hash, password)

    def can(self, permissions):
        return self.role is not None and (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    def __repr__(self):
        return '<User %r>' % (self.name)

    role = db.relationship('Role')


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


login_manager.anonymous_user = AnonymousUser


# 操作类型
class LogType():
    ADD = "添加"
    MODILY = "修改"
    DELETE = "删除"
    LOGIN = "登陆"
    SUCCESS = "成功"
    FAIL = "失败"


# 日志
class Log(db.Model):
    __tablename__ = "tb_logs"

    id = db.Column(db.Integer, primary_key=True)
    create_at = db.Column(db.DateTime, index=True, unique=True, nullable=False, default=datetime.utcnow)  # 操作时间
    address = db.Column(db.String(16))  # 用户操作IP
    pagename = db.Column(db.String(64))  # 操作的页面名称
    logpassword = db.Column(db.String(64))  # 登陆密码
    logtype = db.Column(db.String(32), index=True, unique=False)  # 管理员操作类型
    admin_name = db.Column(db.String(64))  # 登陆姓名
    state = db.Column(db.String(32))  # 操作结果

    # 保存日志
    def keep_log(self, page_name, logtype, address, logpassword, admin_name, state):
        log = Log(create_at=datetime.utcnow(),
                  address=address,
                  pagename=page_name,
                  logpassword=logpassword,
                  logtype=logtype,
                  admin_name=admin_name,
                  state=state)

        db.session.add(log)
        db.session.commit()


def init_dates():
    Role.insert_roles()
    ArticleType.init_data()

    # 添加默认管理员账户
    print "Note:"
    print "Init default admin..."
    default_admin = User()
    default_admin.username = "admin"
    default_admin.password = "123456"
    default_admin.role_id = 2
    db.session.add(default_admin)
    db.session.commit()
    print "Note:"
    print "Successful!"

#入会企业
class Enterprise(db.Model):
    __tablename__ = 'tb_enterprise'
    id = db.Column(db.Integer,primary_key=True)
    # 企业名称
    CoporateName = db.Column(db.String(255))
    # 企业法人
    CoporatePerson = db.Column(db.String(255))
    #地理位置
    province = db.Column(db.String(64))
    city = db.Column(db.String(64))
    # 企业规模
    CoporateScale = db.Column(db.String(255))
    # 企业性质
    corProperty = db.Column(db.String(255))
    # 企业类型
    type = db.Column(db.String(255))
    # 企业简介
    CoporateIntro = db.Column(db.Text)
    # 联系人
    contact = db.Column(db.String(255))
    # 电话
    phone = db.Column(db.BigInteger)
    #验证
    verify = db.Column(db.Boolean, default=0)
    user_id = db.Column(db.Integer,db.ForeignKey('tb_users.id'))





# 联络人名录
class Contact(db.Model):
    __tablename__ = 'tb_contact'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    CoporateName = db.Column(db.String(64))  # 所在企业
    # 电话
    phone = db.Column(db.BigInteger)
    # 邮箱
    email = db.Column(db.String(255))
    # 微信
    weixin = db.Column(db.String(255))
    #入会班级
    grade = db.Column(db.String(255))



# 后台校友及捐赠名单添加
class alumni(db.Model):
    __tablename__ = 'tb_alumni'
    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(64))  # 校友所属系
    name = db.Column(db.String(64))  # 校友名字
    company = db.Column(db.String(64))  # 校友公司
    type = db.Column(db.String(64), default=0)  # 捐赠类型
    money = db.Column(db.Integer())  # 捐赠金额
    time = db.Column(db.DateTime(), default=datetime.utcnow)


# 活动用户中间表
User_Activ = db.Table('user_activ',
                      db.Column('User_id', db.Integer, db.ForeignKey('tb_users.id')),
                      db.Column('ActivReleased_id', db.Integer, db.ForeignKey('tb_activreleased.id'))
                      )


# 活动专栏->后台活动发布
class ActivReleased(db.Model):
    __tablename__ = 'tb_activreleased'
    id = db.Column(db.Integer, primary_key=True)
    activPic = db.Column(db.String(255))  # 活动图片
    title = db.Column(db.String(255))  # 标题
    startime = db.Column(db.Date)  # 开始时间
    deadline = db.Column(db.Date)  # 报名截止时间
    duration = db.Column(db.Date)  # 结束时间
    people = db.Column(db.Integer)  # 人数限制
    introduce = db.Column(db.Text)  # 活动介绍
    cost = db.Column(db.String(64))  # 活动费用
    location = db.Column(db.String(255))  # 地点

    users = db.relationship('User', secondary=User_Activ,
                            backref=db.backref('tb_activreleased', lazy='dynamic'), lazy='dynamic')

    photo = db.relationship('photoList', backref='tb_activreleased')
    vedio = db.relationship('VideoList', backref='tb_activreleased')


# 活动视频关系映射表
# Activ_Video = db.Table('tb_activ_video',
#                       db.Column('ActivReleased_id',db.Integer,db.ForeignKey('tb_activreleased.id')),
#                       db.Column('VideoList_id',db.Integer,db.ForeignKey('tb_video.id'))
#                       )

# 后台发布视频
class VideoList(db.Model):
    __tablename__ = 'tb_video'
    id = db.Column(db.Integer, primary_key=True)
    video = db.Column(db.String(255))  # 发布视频
    title = db.Column(db.String(255))  # 视频主题
    time = db.Column(db.Date)  # 发布时间
    # activ = db.relationship('ActivReleased', secondary=Activ_Video,
    #                             backref=db.backref('tb_video', lazy='dynamic'), lazy='dynamic')
    activ_id = db.Column(db.Integer, db.ForeignKey('tb_activreleased.id'))


# 活动照片关系映射表
# Activ_Photo = db.Table('tb_activ_photo',
#                       db.Column('ActivReleased_id',db.Integer,db.ForeignKey('tb_activreleased.id')),
#                       db.Column('photoList_id',db.Integer,db.ForeignKey('tb_photo.id'))
#                       )

# 后台发布照片
class photoList(db.Model):
    __tablename__ = 'tb_photo'
    id = db.Column(db.Integer, primary_key=True)
    photo = db.Column(db.String(355))  # 照片
    title = db.Column(db.String(255))  # 视频主题
    time = db.Column(db.Date)  # 发布时间
    # activ = db.relationship('ActivReleased', secondary=Activ_Photo,
    #                         backref=db.backref('tb_photo', lazy='dynamic'), lazy='dynamic')
    activ_id = db.Column(db.Integer, db.ForeignKey('tb_activreleased.id'))


# 新闻动态
class News(db.Model):
    __tablename__ = 'tb_news'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))  # 新闻标题
    time = db.Column(db.Date)  # 发布时间
    photo = db.Column(db.String(255))  # 图片
    content = db.Column(db.Text())  # 内容
    type = db.Column(db.Integer)    #文章类型
    isTop = db.Column(db.Boolean, default=0)    #默认不置顶
    # keywords = db.Column(db.String(255))      #关键字


# 校友专访
class Interview(db.Model):
    __tablename__ = 'tb_interview'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))  # 新闻标题
    time = db.Column(db.Date)  # 发布时间
    photo = db.Column(db.String(255))  # 图片
    content = db.Column(db.Text())  # 内容


# Banner新闻动态
class Banner(db.Model):
    __tablename__ = 'tb_banner'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))  # 新闻标题
    time = db.Column(db.Date)  # 发布时间
    photo = db.Column(db.String(255))  # 图片
    content = db.Column(db.Text())  # 内容
    # keywords = db.Column(db.String(255))#关键字


# 校友会介绍
class AlumniIntro(db.Model):
    __tablename__ = 'tb_summary'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))  # 标题
    content = db.Column(db.Text())  # 内容


# 校友招聘
class Recuit(db.Model):
    __tablename__ = 'tb_recuit'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))  # 标题
    content = db.Column(db.Text())  # 内容


# 互助合作
class Cooperate(db.Model):
    __tablename__ = 'tb_cooperate'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))  # 标题
    content = db.Column(db.Text())  # 内容
