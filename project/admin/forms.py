# coding:utf-8
from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField, TextAreaField, ValidationError, \
    DateTimeField, DateField,FileField,RadioField,IntegerField
from wtforms.validators import InputRequired, Length, Regexp, EqualTo, IPAddress, equal_to,Email
from ..models import User, Role, Log, db, LogType,ActivReleased
from datetime import datetime, timedelta


# 日期表单类,修改了DateField()类
class My_DateField(DateTimeField):
    """
    Same as DateTimeField, except stores a `datetime.date`.
    """

    def __init__(self, label=None, validators=None, format='%Y-%m-%d', **kwargs):
        super(My_DateField, self).__init__(label, validators, format, **kwargs)

    def process_formdata(self, valuelist):
        if valuelist[0] == u'':
            self.data = datetime.strptime('2000-01-01', self.format).date()
        else:
            if valuelist:
                date_str = ' '.join(valuelist)
                try:
                    self.data = datetime.strptime(date_str, self.format).date()
                except ValueError:
                    self.data = None
                    raise ValueError(self.gettext(u'日期格式不正确，请检查！'))


class LoginForm(Form):
    username = StringField(u'账  号', validators=[InputRequired(message=u'请输入账号'),
                                               Length(0, 64, message=u'用户名不能超过64字符'),
                                               Regexp(regex='^[A-Za-z][A-Za-z0-9_]*$', flags=0,
                                                      message=u'用户名只能为字母或者数字及下划线')])
    password = PasswordField(u'密  码', validators=[InputRequired(message=u'请输入密码'),
                                                  Length(6, 64, message=u'密码长度不能低于6位'),
                                                  Regexp('^[A-Za-z0-9_]*$', flags=0, message=u'密码只能为字母或者数字及下划线')])
    remember_me = BooleanField(u'记住我')
    submit = SubmitField(u'登陆')


class RegisterAdminForm(Form):
    username = StringField(u'会员用户名', validators=[InputRequired(message=u'管理员姓名不能为空'),
                                                  Length(0, 64, message=u'用户名地址不能超过64字符'),
                                                  Regexp(ur'^[A-Za-z\u4e00-\u9fa5][A-Za-z0-9_\u4e00-\u9fa5]*$', 0,
                                                         u'用户名只能为中文，字母或者数字及下划线')])
    password = PasswordField(u'密码', validators=[InputRequired(message=u'密码不能为空'),
                                                    EqualTo('password2', message=u'两次密码必须相同')])
    password2 = PasswordField(u'确认密码', validators=[InputRequired(message=u'确认密码不能为空')])
    name = StringField(u'真实姓名', validators=[InputRequired(message=u'真实姓名不能为空'), Length(0, 64, )])
    location = StringField(u'你的地址', validators=[InputRequired(message='地址不能超过64字符')])
    about_me = TextAreaField(u'个人简介')
    submit = SubmitField(u'注册')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(u'用户名已被注册')


class EditAdminForm(Form):
    username = StringField(u'管理员姓名')
    role = SelectField(u'用户授权', coerce=int)  # 用户角色
    password = PasswordField(u'更改该用户密码')
    name = StringField(u'真实姓名', validators=[InputRequired(message=u'真实姓名不能为空'), Length(0, 64, )])
    location = StringField(u'您的地址', validators=[InputRequired(message=u'地址不能为空')])
    about_me = TextAreaField(u'个人简介')
    submit = SubmitField(u'修改')

    def __init__(self, admin, *args, **kwargs):
        super(EditAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.id).all()]
        pass
        self.admin = admin

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(u'用户名已被注册')


class DeleteAdminLog(Form):
    del_list = SelectField(u'删除', coerce=int)
    submit = SubmitField(u'删除')

    def __init__(self, *args, **kwargs):
        super(DeleteAdminLog, self).__init__(*args, **kwargs)
        self.del_list.choices = [(30, u'30天以前'), (60, u'60天以前'), (90, u'90天以以前'), (180, u'180天以前')]
        pass

    def del_logs(self, days):
        dellogs = Log.query.filter(Log.create_at < (datetime.utcnow() - timedelta(days=days))).all()
        record = len(dellogs)  # 获取删除数据长度
        for dellog in dellogs:
            db.session.delete(dellog)
        db.session.commit()
        return record


class QueryLogsForm(Form):
    date1 = My_DateField(u'开始日期')
    date2 = My_DateField(u'结束日期')
    user_operation = StringField(u'操作员')
    loginip = StringField(u'登陆IP', validators=[IPAddress(message=u'IP地址格式不对，请检查')])
    operration_type = SelectField(u'操作类型', coerce=str)
    remarks = StringField(u'备注')  # 备注
    submit = SubmitField(u'查询')

    def __init__(self, *args, **kwargs):
        super(QueryLogsForm, self).__init__(*args, **kwargs)
        log_ = [('', '全部')]
        log1_ = ()
        logtype = LogType.__dict__  # 获取日志类型字典
        for logs in dir(LogType):  # 清除系统类型的属性
            if '__' in logs:
                logtype.pop(logs)
            else:
                log1_ = (logtype[logs], '　›' + logtype[logs])  # 将类型字典转换成列表元组，只取字典的值作为2个参数
                log_.append(log1_)
        logtype = log_
        self.operration_type.choices = logtype
        pass

    def validate_date1(self, field):
        if self.date2.data < field.data:
            raise ValidationError(u'结束日期不能小于开始日期，请检查日期！')

#管理员修改密码
class ModifyPswForm(Form):
    old_password = StringField(u'旧密码', validators=[InputRequired(message=u'旧密码不正确')])
    new_password = PasswordField('新密码',validators=[Length(min=6, max=20, message='6到20位字符，建议由数字，字母和符号2种以上的组合'),
                                             InputRequired(message='请输入新密码')])
    repassword = PasswordField('确认密码', validators=[EqualTo('new_password', message='两次输入不一致')])
    submit = SubmitField('确认')


#后台校友添加
class AlumniForm(Form):
    department = StringField(u'班级',validators=[InputRequired(message=u'班级不能为空'),
                                                Regexp(ur'[A-Za-z\u4e00-\u9fa5][A-Za-z0-9_\u4e00-\u9fa5]{1,64}', 0,
                                                       message=u'用户名只能为中文，字母或者数字及下划线')])

    name = StringField(u'姓名',validators=[InputRequired(message=u'姓名不能为空'),
                                        Regexp(ur'[A-Za-z\u4e00-\u9fa5][A-Za-z0-9_\u4e00-\u9fa5]{1,64}', 0,
                                        message=u'用户名只能为中文，字母或者数字及下划线')])
    type = SelectField(u'类型', coerce=int, choices=[(0, u'企业'), (1, u'个人')],
                          validators=[InputRequired()])
    company = StringField(u'名称',validators=[InputRequired(message=u'名称不能为空')])
    money = StringField(u'金额',validators=[InputRequired(message=u'金额不能为空')])
    submit = SubmitField(u'添加')

#后台校友修改
class updateAlumniForm(Form):
    department = StringField(u'系别', validators=[Length(0,64)] )
    name = StringField(u'姓名',validators=[Length(0,64)])
    type = SelectField(u'类型', coerce=int, choices=[(0, u'企业'), (1, u'个人')], default=0,
                       validators=[InputRequired()])
    company = StringField(u'名称')
    money = StringField(u'金额')
    submit = SubmitField(u'修改')

#后台校友搜索
class SearchAlumniForm(Form):
    keywords = StringField(u'搜索')
    submit = SubmitField(u'搜索')

#后台活动发布
class ActivReleasedForm(Form):
    activPic = FileField(u'活动图片')
    title = StringField(u'活动标题',validators=[InputRequired(message=u'标题不能为空')])
    startime = StringField(u'开始时间',validators=[InputRequired(message=u'开始时间不能为空')])
    deadline = StringField(u'报名截止时间',validators=[InputRequired(message=u'截止时间时间不能为空')])
    duration =  StringField(u'结束时间',validators=[InputRequired(message=u'结束时间不能为空')])
    introduce = TextAreaField(u'活动简介',validators=[InputRequired(message=u'简介不能为空')])
    cost = StringField(u'活动费用',validators=[InputRequired(message=u'费用不能为空')])
    people = StringField(u'活动人数',validators=[InputRequired(message=u'人数不能为空')])
    location = StringField(u'活动地点',validators=[InputRequired(message=u'地点不能为空')])
    submit = SubmitField(u'提交保存')

#后台活动修改
class UpdateActivForm(Form):
    activPic = FileField(u'活动图片')
    title = StringField(u'活动标题',validators=[InputRequired(message=u'标题不能为空')])
    startime = StringField(u'开始时间',validators=[InputRequired(message=u'开始时间不能为空')])
    deadline = StringField(u'报名截止', validators=[InputRequired(message=u'截止时间时间不能为空')])
    duration =  StringField(u'结束时间',validators=[InputRequired(message=u'结束时间不能为空')])
    introduce = TextAreaField(u'活动简介',validators=[InputRequired(message=u'简介不能为空')])
    people = StringField(u'活动人数',validators=[InputRequired(message=u'人数不能为空')])
    cost = StringField(u'活动费用',validators=[InputRequired(message=u'费用不能为空')])
    location = StringField(u'活动地点',validators=[InputRequired(message=u'地点不能为空')])
    submit = SubmitField(u'提交保存')

#后台活动搜索
class SearchActivForm(Form):
    keywords = StringField(u'搜索')
    submit = SubmitField(u'搜索')

#校友联络人搜索
class SearchAlumniForm(Form):
    keywords = StringField(u'搜索')
    submit = SubmitField(u'搜索')

#视频发布
class VideoPublishForm(Form):
    activ = SelectField(u'活动名称',coerce=int)
    video = FileField(u'发布视频',validators=[InputRequired(message=u'视频不能为空')])
    # photo = FileField(u'发布照片')
    title = StringField(u'图像主题',validators=[InputRequired(message=u'主题不能为空')])
    time = StringField(u'发布时间',validators=[InputRequired(message=u'时间不能为空')])
    submit = SubmitField(u'提交保存')

    def __init__(self, *args, **kwargs):
        super(VideoPublishForm, self).__init__(*args, **kwargs)
        self.activ.choices = [(active.id, active.title)
                              for active in ActivReleased.query.order_by(ActivReleased.title).all()]

#照片发布
class PhotoPublishForm(Form):
    activ = SelectField(u'活动名称',coerce=int)
    photo = FileField(u'发布照片',validators=[InputRequired(message=u'照片不能为空')])
    title = StringField(u'图像主题',validators=[InputRequired(message=u'主题不能为空')])
    time = StringField(u'发布时间',validators=[InputRequired(message=u'时间不能为空')])
    submit = SubmitField(u'提交保存')

    def __init__(self,  *args, **kwargs):
        super(PhotoPublishForm, self).__init__(*args, **kwargs)
        self.activ.choices = [(active.id, active.title)
                                       for active in ActivReleased.query.order_by(ActivReleased.title).all()]

##新闻动态
class NewsForm(Form):
    type = SelectField(u'新闻类型',coerce=int,choices=[(0,u'校友会新闻'),(1,u'学校新闻'),(2,u'通知公告')],default=0,
                       validators=[InputRequired()])
    title = StringField(u'新闻标题',validators=[InputRequired(message=u'标题不能为空')])
    time = StringField(u'发布时间',validators=[InputRequired(message=u'时间不能为空')])
    photo = FileField(u'新闻图片')
    content =TextAreaField(u'新闻正文',validators=[InputRequired(message=u'正文不能为空')])
    submit = SubmitField(u'提交保存')

#管理员
class AddmemberssForm(Form):
    username=StringField('会员名称')
    password=PasswordField('会员密码',validators=[InputRequired(message=u'密码不能为空'),
                                            EqualTo('password2',message='密码必须一致')])
    password2=PasswordField('确认密码',validators=[InputRequired()])
    submit = SubmitField('保存提交')


#校友专访
class InterviewForm(Form):
    title = StringField(u'专访标题',validators=[InputRequired(message=u'标题不能为空')])
    time = StringField(u'发布时间',validators=[InputRequired(message=u'时间不能为空')])
    photo = FileField(u'专访照片')
    content =TextAreaField(u'专访正文',validators=[InputRequired(message=u'正文不能为空')])
    submit = SubmitField(u'提交保存')

##新闻动态
class BannerForm(Form):
    title = StringField(u'新闻标题',validators=[InputRequired(message=u'标题不能为空')])
    time = StringField(u'发布时间',validators=[InputRequired(message=u'时间不能为空')])
    photo = FileField(u'新闻文件')
    content =TextAreaField(u'新闻正文',validators=[InputRequired(message=u'正文不能为空')])
    keywords = StringField(u'关键字词')
    submit = SubmitField(u'提交保存')

#学校新闻
class SchoolForm(Form):
    title = StringField(u'新闻标题',validators=[InputRequired(message=u'标题不能为空')])
    time = StringField(u'发布时间',validators=[InputRequired(message=u'时间不能为空')])
    photo = FileField(u'新闻文件')
    content =TextAreaField(u'新闻正文',validators=[InputRequired(message=u'正文不能为空')])
    submit = SubmitField(u'提交保存')

#通知公告
class NoticeForm(Form):
    title = StringField(u'新闻标题',validators=[InputRequired(message=u'标题不能为空')])
    time = StringField(u'发布时间',validators=[InputRequired(message=u'时间不能为空')])
    photo = FileField(u'新闻文件')
    content =TextAreaField(u'新闻正文',validators=[InputRequired(message=u'正文不能为空')])
    submit = SubmitField(u'提交保存')

##校友会
class SummaryForm(Form):
    title = StringField(u'简介标题',validators=[InputRequired(message=u'标题不能为空')])
    content =TextAreaField(u'简介正文',validators=[InputRequired(message=u'正文不能为空')])
    submit = SubmitField(u'提交保存')

##校友会
class UpdateSummaryForm(Form):
    title = StringField(u'简介标题')
    content =TextAreaField(u'简介正文')
    submit = SubmitField(u'提交保存')

#校友招聘
class RecuitForm(Form):
    title = StringField(u'简介标题',validators=[InputRequired(message=u'标题不能为空')])
    content =TextAreaField(u'简介正文',validators=[InputRequired(message=u'正文不能为空')])
    submit = SubmitField(u'提交保存')

#互助合作
class CoperateForm(Form):
    title = StringField(u'简介标题',validators=[InputRequired(message=u'标题不能为空')])
    content =TextAreaField(u'简介正文',validators=[InputRequired(message=u'正文不能为空')])
    submit = SubmitField(u'提交保存')

#管理会员
class AddmemberForm(Form):
    username = StringField(u'姓名',validators=[InputRequired(message=u'用户名不能为空')])
    CoporateName =StringField(u'所在单位',validators=[InputRequired(message=u'所在单位不能为空')])
    grade = StringField(u'所在班级', validators=[InputRequired(message=u'所在班级不能为空')])
    phone = StringField(u'联系电话',validators=[InputRequired(message=u'电话不能为空')])
    email = StringField(u'电子邮件',validators=[InputRequired(message=u'邮件不能为空')])
    weixin = StringField(u'微信账号', validators=[InputRequired(message=u'微信不能为空')])
    submit = SubmitField(u'提交保存')

#友情链接添加
class FriendlyLinkForm(Form):
    title = StringField(u'合作伙伴',validators=[InputRequired(message=u'合作伙伴不能为空')])
    link = StringField(u'友情链接',validators=[InputRequired(message=u'合作伙伴不能为空')])
    img = FileField(u'封面图片',validators=[InputRequired(message=u'封面图片不能为空')] )
    submit = SubmitField(u'添加')

#友情链接修改
class updateLinkForm(Form):
    title = StringField(u'合作伙伴', validators=[InputRequired(message=u'合作伙伴不能为空')])
    link = StringField(u'友情链接', validators=[InputRequired(message=u'合作伙伴不能为空')])
    img = FileField(u'封面图片', validators=[InputRequired(message=u'封面图片不能为空')])
    submit = SubmitField(u'修改')

#友情链接搜索
class SearchLinkForm(Form):
    keywords = StringField(u'搜索')
    submit = SubmitField(u'搜索')

#入会审核类型操作选择
class stateChoiceForm(Form):
    type = SelectField(u'操作类型', coerce=int, choices=[(0, u'冻结账户'), (1, u'解冻账户')], default=0)
    submit = SubmitField(u'搜索')

#添加校友入会
class enrollmentForm(Form):
    name = StringField(u'姓名', validators=[InputRequired(message=u'姓名不能为空'),
                                            Regexp(ur'[A-Za-z\u4e00-\u9fa5][A-Za-z0-9_\u4e00-\u9fa5]{1,64}', 0,
                                                   message=u'用户名只能为中文，字母或者数字及下划线')])
    sex = RadioField(u'性别', coerce=int, choices=[(0, u' 男'), (1, u'女')],
                     validators=[InputRequired(message=u'性别不能为空')])
    status = SelectField(u'身份', coerce=int, validators=[InputRequired(message=u'身份不能为空')],choices=[(1, u'学院教职工'), (2, u'学院特聘人员'),
                                                       (3, u'毕业研究生'), (4, u'全日制本科毕业生'),
                                                       (5, u'城市学院毕业生'), (6, u'网络教育毕业生'),
                                                       (7, u'成教自考生')])
    grade = StringField(u'班级',validators=[InputRequired(message=u'班级不能为空')])
    contact = StringField(u'联络人')
    birthday = StringField(u'出生日期')
    phone = IntegerField(u'电话', validators=[InputRequired(message=u'电话不能为空')])
    email = StringField(u'邮箱', validators=[InputRequired(message=u'邮箱不能为空'), Length(1, 64), Email()])
    submit = SubmitField(u'提交保存')


