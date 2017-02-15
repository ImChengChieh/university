# coding:utf-8
from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField, TextAreaField, ValidationError, \
    DateTimeField, DateField, RadioField, IntegerField
from wtforms.validators import InputRequired, Length, Regexp, EqualTo, IPAddress, equal_to, Email
from ..models import User, Role, Log, db, LogType
from datetime import datetime, timedelta

#注册
class RegisterHomeForm(Form):
    username = StringField(u'账号',validators=[InputRequired(message=u'账户不能为空!'),
                                             Regexp(ur'[A-Za-z\u4e00-\u9fa5][A-Za-z0-9_\u4e00-\u9fa5]{1,64}', 0,
                                                    message=u'用户名只能为中文，字母或者数字及下划线')])
    password = PasswordField(u'密码',validators=[InputRequired(message=u'密码不能为空!'),
                                               EqualTo('repassword',message=u'密码必须一致'),])
    repassword = PasswordField(u'确认密码',validators=[InputRequired(message=u'确认密码不能为空!')])
    submit = SubmitField(u'立即注册')


    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('账号已经被注册！')


    def validate_password(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('密码不能为空!')


    def validate_accept(self, field):
        if not field.data:
            raise ValidationError('同意《校友会章程》')

#登录
class LoginHomeForm(Form):
    username = StringField(u'账号', validators=[InputRequired(),
                                              Regexp('[A-Za-z\u4e00-\u9fa5][A-Za-z0-9_\u4e00-\u9fa5]{1,64}', 0,
                                                     message=u'用户名只能为中文，字母或者数字及下划线')])
    password = PasswordField(u'密码', validators=[InputRequired() ])
    submit = SubmitField(u'登录')

    def validate_password(self, field):
        if User.query.filter_by(password=field.data).first():
            raise ValidationError('密码错误!')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            pass
        else:
            raise ValidationError('请先注册账号！')

#修改密码
class modifyForm(Form):
    old_password = StringField (u'旧密码',validators=[InputRequired(message=u'旧密码不正确')])
    new_password = PasswordField('新密码',
                                 validators=[Length(min=6, max=20, message='6到20位字符，建议由数字，字母和符号2种以上的组合'),
                                             InputRequired(message='请输入新密码')])
    repassword = PasswordField('确认密码', validators=[EqualTo('new_password', message='两次输入不一致')])
    submit = SubmitField('确认')

#修改邮箱
class modifyEmailForm(Form):
    old_email = StringField (u'原邮箱',validators=[InputRequired(message=u'原邮箱不正确' ),Email()])
    new_email = StringField('新邮箱',
                                 validators=[Length(min=6, max=20),InputRequired(message='请输入新邮箱'),Email()])
    submit = SubmitField('提交')

#修改电话号码
class ModifyPhoneForm(Form):
    old_phone = StringField (u'原号码',validators=[InputRequired(message=u'原号码不正确' )])
    new_phone = StringField('新号码',validators=[InputRequired(message='请输入新邮箱')])
    submit = SubmitField('提交')

# 校友入会通道
class memberForm(Form):
    name = StringField(u'您的姓名', validators=[InputRequired(),
                                                Regexp(ur'[A-Za-z\u4e00-\u9fa5][A-Za-z0-9_\u4e00-\u9fa5]{1,64}', 0,
                                                       message=u'用户名只能为中文，字母或者数字及下划线')])
    sex = RadioField(u'您的性别', coerce=int, choices=[(0, u' 男'), (1, u'女')],
                     validators=[InputRequired()])
    status = SelectField(u'身份选择', coerce=int, choices=[(1, u'学院教职工'), (2, u'学院特聘人员'),
                                                       (3, u'毕业研究生'),(4,u'全日制本科毕业生'),
                                                       (5,u'城市学院毕业生'),(6,u'网络教育毕业生'),
                                                       (7,u'成教自考生')])
    grade = StringField(u'入学班级')
    contact = StringField(u'联络人')
    # provice = SelectField(u'当前所在地',choices=[(u'四川'),(u'云南')])
    # city = SelectField(u'当前市',choices=[(u'成都'),(u'昆明')])
    birthday = StringField(u'出生日期')
    identInfor = TextAreaField(u'验证信息')
    phone = IntegerField(u'联系电话', validators=[InputRequired()])
    email = StringField(u'联络邮箱', validators=[InputRequired(), Length(1, 64), Email()])
    accept = BooleanField(u'同意《校友会章程》')
    submit = SubmitField(u'申请登记')

    # def __init__(self):
        # self.provice.choices =

    # def validate_username(self,field):
    #     if User.query.filter_by(username=field.data).first():
    #         raise ValidationError('账号已经被注册！')

    # def validate_email(self, field):
    #     if User.query.filter_by(email=field.data).first():
    #         raise ValidationError('邮箱已经被注册!')

    # def validate_accept(self,field):
    #     if not field.data:
    #         raise ValidationError('同意《校友会章程》')

#企业会员通道
class CopMemberForm(Form):

    name = StringField(u'校友企业名称',validators=[InputRequired(),
                                                Regexp(ur'[A-Za-z\u4e00-\u9fa5][A-Za-z0-9_\u4e00-\u9fa5]{1,64}', 0,
                                                       message=u'用户名只能为中文，字母或者数字及下划线')])
    legalPerson = StringField(u'企业法人代表',validators=[
                                                Regexp(ur'[A-Za-z\u4e00-\u9fa5][A-Za-z0-9_\u4e00-\u9fa5]{1,64}', 0,
                                                       message=u'用户名只能为中文，字母或者数字及下划线')])
    scale = SelectField(u'公司规模',coerce=int,choices=[(1,u'大型'),(2,u'中型'),(3,u'小型')])
    corProperty = SelectField(u'企业性质',coerce=int,choices=[(1,u'全民'),(2,u'集体'),(3,u'股份'),
                                                       (4,u'私营'),(5,u'外商投资')])
    type = SelectField(u'企业类型',coerce=int,choices=[(1,u'工业'),(2,u'建筑业'),(3,u'批发和零售业'),
                                                    (4,u'交通运输、邮政业'),(5,u'住宿和餐饮业')])
    intro = TextAreaField(u'企业简介')
    contact = StringField(u'校友联络人')
    phone = IntegerField(u'联系电话')
    submit = SubmitField(u'申请登记')

#活动报名
class CompetitionForm(Form):
    compet = IntegerField(u'参赛人数')
    submit = SubmitField(u'我要报名')