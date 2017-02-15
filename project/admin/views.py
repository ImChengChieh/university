#!/user/bin/env python
# -*- coding: utf-8 -*-
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
    ModifyPswForm,stateChoiceForm
from ..models import db,alumni,ActivReleased,VideoList,News,Interview,photoList,Banner,\
    AlumniIntro,User,Recuit,Cooperate,Contact,Enterprise
from sqlalchemy.sql.expression import or_,not_

from flask_mail import Message
from project import mail


UPLOAD_FOLDER = r"F:\Python\kongfu\college\project\static\upload"

# 后台默认页面
@admin.route("/")
@login_required
@admin_required
def def_page():
    return redirect(url_for(".admin_list"))

#修改管理员密码
@admin.route("/modify/password",methods=['GET','POST'])
@login_required
@admin_required
def modify_admin():
    form = ModifyPswForm()
    user = User.query.get(current_user.get_id())
    if form.validate_on_submit():
        if current_user.verify_passwrod(form.old_password.data):
            user.password = form.new_password.data
            db.session.add(user)
            db.session.commit()
            flash('密码修改成功！')
            return redirect(url_for('project.admin.index'))
        else:
            flash('原密码错误！')
    return render_template("admin/admin_modify.html",form=form)



# 后台首页
@admin.route("/index")
@login_required
@admin_required
def index():
    #校友入会
    #入会校友总数
    userCount = User.query.filter(not_(User.username == 'admin'))
    user = userCount.filter(not_(User.name == 'None')).count()
    #入会校友未审核
    clearNone=userCount.filter(not_(User.name == 'None'))
    user_Unverified = clearNone.filter(User.verify == 0).count()
    # 入会校友已经审核
    user_verified = user - user_Unverified
    #企业入会
    #企业入会总数
    verify = Enterprise.query.filter(not_(Enterprise.user_id == '1'))
    verify_Cooperate = verify.filter(Enterprise.CoporateName != None).count()
    # 企业入会总数已审核
    Cooperate_verify = verify.filter(Enterprise.verify == 1).count()
    # 企业入会总数未审核
    Cooperate_virify = verify_Cooperate - Cooperate_verify
    #Banner条数
    banner = Banner.query.filter(Banner.id).count()
    #新闻动态
    news = News.query.filter(News.id).count()
    #校友专访
    interview = Interview.query.filter(Interview.id).count()
    #校友招聘
    recuit = Recuit.query.filter(Recuit.id).count()
    #互助合作
    cooperate_index = Cooperate.query.filter(Cooperate.id).count()
    #校友简介
    introduce = AlumniIntro.query.filter(AlumniIntro.id).count()
    #校友会联络人
    contact = Contact.query.filter(Contact.id).count()
    #活动
    activity = ActivReleased.query.filter(ActivReleased.id).count()
    #照片
    photo = photoList.query.filter(photoList.id).count()
    #视频
    video = VideoList.query.filter(VideoList.id).count()
    #捐赠
    donation = alumni.query.filter(alumni.id).count()
    #友情链接
    link= FriendshipLink.query.filter(FriendshipLink.id).count()
    return render_template("admin/admin_index.html", user=user,user_Unverified=user_Unverified,
                           user_verified=user_verified,Cooperate_virify=Cooperate_virify,
                           Cooperate_verify=Cooperate_verify,verify_Cooperate=verify_Cooperate,banner=banner,
                           news=news,interview=interview,recuit=recuit,cooperate_index=cooperate_index,
                           introduce=introduce,contact=contact,activity=activity,photo=photo,
                           video=video,donation=donation,link=link)

#用户情况
@admin.route("/admin_list",methods=['GET','POST'])
@login_required
@admin_required
def user_index():
    search_form = SearchActivForm()
    choice_form = stateChoiceForm()
    if choice_form.validate_on_submit():
        types = choice_form.type.data
        state = User.query.filter(or_(User.state.like(types))).all()
        return render_template('admin/admin_list.html', choice_form=choice_form,
                               search_form=search_form,activities=state)
    if search_form.validate_on_submit():
        keywords = search_form.keywords.data
        # types = choice_form.type.data
        # state = User.query.filter(or_(User.state.like(types))).all()
        activities = User.query.filter(or_(User.username.like('%' + keywords + '%'),
                                                    )).all()
        return render_template('admin/admin_list.html', search_form=search_form,
                               activities=activities)
    page = request.args.get('page', 1, type=int)
    pagination = User.query.filter(not_(User.username == 'admin')).paginate(
        page, per_page=current_app.config['FLASY_NEWS_PER_PAGE'],
        error_out=False
    )
    user = pagination.items
    return render_template("admin/admin_list.html",activities=user,search_form=search_form,
                           pagination=pagination,choice_form=choice_form)

#用户状态
@admin.route('/api/admin_list', methods=['GET', 'POST'])
def part():
    User_id = request.form.get('id')
    user = User.query.get(User_id)
    if not user.state :
        user.state = '1'
        #激活
        db.session.add(user)
        db.session.commit()
        return '1'
    else:
        user.state = '0'
        db.session.add(user)
        db.session.commit()
        return '0'




#管理 -》添加校友
@admin.route("/add_member",methods=['GET','POST'])
@login_required
@admin_required
def add_member():
    form = AddmemberssForm()
    if form.validate_on_submit():
        user = User(
            username = form.username.data,
            password = form.password.data
            # contact = form.contact.data,
            # CoporateName = form.CoporateName.data,
            # phone = form.phone.data,
            # email = form.email.data
        )
        db.session.add(user)
        db.session.commit()
        # flash(u'添加成功。。。')
        return redirect(url_for('project.admin.user_index'))
    return render_template('admin/admin_edit.html', form=form)

#管理 -》编辑校友
@admin.route('/add_member/edit/<int:id>',methods=['GET','POST'])
@login_required
def edit_member(id):
    user = User.query.get_or_404(id)
    form = AddmemberForm()
    if form.validate_on_submit():
        user.username = form.username.data
        # user.contact = form.contact.data
        # user.CoporateName = form.CoporateName.data
        # user.phone = form.phone.data
        # user.email = form.email.data
        db.session.add(user)
        db.session.commit()
        # flash('修改成功...')
        return redirect(url_for('project.admin.user_index'))
    form.username.data = user.username
    # form.contact.data = user.contact
    # form.CoporateName.data = user.CoporateName
    # form.phone.data = user.phone
    # form.email.data = user.email
    return render_template('admin/admin_edit.html',form=form)

#删除管理会员
@admin.route("/add_member/del/<int:id>",methods=['GET','POST'])
@login_required
@admin_required
def del_member(id):
    # del_donations = addAlumni.query.order_by(addAlumni.id).all()
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('project.admin.user_index'))


#删除目录
@admin.route("/add_contact/del/<int:id>",methods=['GET','POST'])
@login_required
@admin_required
def del_contact(id):
    # del_donations = addAlumni.query.order_by(addAlumni.id).all()
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('project.admin.contact_list'))


# 文章列表
# @admin.route("/articles")
# @login_required
# @admin_required
# def article_list():
#     article_types = ArticleType.query.order_by(ArticleType.superior, ArticleType.id).all()
#     return render_template("admin/article_list.html", article_types=article_types)


# 添加文章页面
@admin.route("/article/add")
@login_required
@admin_required
def article_add():
    article_types = ArticleType.query.order_by(ArticleType.superior, ArticleType.id).all()
    return render_template("admin/article_edit.html", article_types=article_types)



@admin.route("/friendshiplink/add",methods=['GET', 'POST'])
@login_required
@admin_required
def friendshiplink_add():
    form = FriendlyLinkForm()
    if form.validate_on_submit():
        addLink = FriendshipLink(
            title=form.title.data,
            link=form.link.data
        )

        file = request.files['img']
        filename = random_file_name(secure_filename(file.filename))
        # filename = file.filename
        APP_ROOT = os.path.dirname(os.path.dirname(__file__))
        UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/upload')
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        file_path_name = filename
        addLink.img = file_path_name

        db.session.add(addLink)
        db.session.commit()
        return redirect(url_for('project.admin.friendshiplink'))
    return render_template("admin/friendshiplink_add.html", form=form)


@admin.route("/friendshiplink/update/<id>",methods=['GET', 'POST'])
@login_required
@admin_required
def friendshiplink_update(id):
    # friendshiplink = FriendshipLink.query.filter_by(id=id).first()
    link_update = FriendshipLink.query.get(id)
    link_img = FriendshipLink.query.filter_by(id=id).first()
    form = updateLinkForm()
    form.img.validators =[]
    if form.validate_on_submit():
        link_update.title = form.title.data
        link_update.link = form.link.data

        file = request.files['img']
        # filename = file.filename
        filename = random_file_name(secure_filename(file.filename))
        if filename:
            APP_ROOT = os.path.dirname(os.path.dirname(__file__))
            UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/upload')
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            file_path_name = filename
            link_update.img = file_path_name

        db.session.add(link_update)
        db.session.commit()
        return redirect(url_for('project.admin.friendshiplink'))
    form.title.data = link_update.title
    form.link.data = link_update.link
    return render_template("admin/friendshiplink_edit.html",form=form,link_img=link_img)


# 友情链接
@admin.route("/frendshiplink")
@login_required
@admin_required
def friendshiplink():
    page = request.args.get('page', 1, type=int)
    pagination = FriendshipLink.query.order_by(FriendshipLink.id).paginate(
         page,per_page=current_app.config['FLASY_BANNER_PER_PAGE'],
         error_out=False
     )
    links = pagination.items
    return render_template("admin/frendshiplink.html",links=links,pagination=pagination)


@admin.errorhandler(403)
def permission(e):
    return render_template('admin/403.html'), 403


@admin.errorhandler(404)
def page_not_found(e):
    return render_template('admin/404.html'), 404


@admin.errorhandler(500)
def internal_server_error(e):
    return render_template('admin/500.html'), 500


#捐赠名单
@admin.route("/donations/alumni",methods=['GET', 'POST'])
@login_required
@admin_required
def Alumni_donations():
    form = SearchAlumniForm()
    page = request.args.get('page', 1, type=int)
    if form.validate_on_submit():
        keywords = form.keywords.data
        alumnis=alumni.query.filter(or_(alumni.department.like('%'+keywords+'%'),
                                        alumni.name.like('%'+keywords+'%'),
                                        alumni.company.like('%' + keywords + '%'),
                                        alumni.money.like('%' + keywords + '%'),
                                    )).all()
        return render_template('admin/alumni_donations.html',form=form,alumnis=alumnis)
    pagination = alumni.query.order_by(alumni.id).paginate(
        page,per_page=current_app.config['FLASK_ALUMNIS_PER_PAGE'],error_out=False
    )
    alumnis = pagination.items
    # alumnislist = alumni.query.order_by(alumni.id).all()
    return render_template('admin/alumni_donations.html',
                           pagination=pagination,
                           alumnis=alumnis,form=form)



#添加新校友捐赠名单
@admin.route('/donations/addAlumni',methods=['GET', 'POST'])
@login_required
# @admin_required
def add_alumni():
    form = AlumniForm()
    if form.validate_on_submit():
        addAlum = alumni(
            department = form.department.data,
            name = form.name.data,
            type = form.type.data,
            company = form.company.data,
            money = form.money.data
        )
        db.session.add(addAlum)
        db.session.commit()
        flash(u'添加成功。。。')
        return redirect(url_for('project.admin.Alumni_donations'))
    return render_template('admin/addAlumni.html', form=form)


#修改新校友捐赠名单
@admin.route('/donations/updateAlumi/<int:id>',methods=['GET','POST'])
@login_required
def update_alumni(id):
    add_alumni = alumni.query.get_or_404(id)
    form = updateAlumniForm()
    if form.validate_on_submit():
        add_alumni.department = form.department.data
        add_alumni.name = form.name.data
        add_alumni.type = form.type.data
        add_alumni.company = form.company.data
        add_alumni.money = form.money.data
        db.session.add(add_alumni)
        db.session.commit()
        flash('修改成功...')
        return redirect(url_for('project.admin.Alumni_donations'))
    form.department.data = add_alumni.department
    form.name.data = add_alumni.name
    form.type.data = add_alumni.type
    form.company.data = add_alumni.company
    form.money.data = add_alumni.money
    return render_template('admin/updateAlumni.html',form=form)

#删除捐赠名单
@admin.route("/donations/alumni/<int:id>",methods=['GET','POST'])
@login_required
@admin_required
def del_alumni(id):
    # del_donations = addAlumni.query.order_by(addAlumni.id).all()
    del_alumni = alumni.query.get_or_404(id)
    db.session.delete(del_alumni)
    db.session.commit()
    return redirect(url_for('project.admin.Alumni_donations'))

def random_file_name(filename):
    '''replace user uploads file with random file name '''
    file_extension = filename.rsplit('.', 1)[1]
    import uuid
    file_name = str(uuid.uuid4())
    return file_name + '.' + file_extension


#后台活动发布
@admin.route("/activity/add",methods=['GET','POST'])
@login_required
@admin_required
def add_activity():
    form = ActivReleasedForm()
    if form.validate_on_submit():
        ActivRele = ActivReleased(
            # activPic=form.activPic.data,
            title = form.title.data,
            startime = form.startime.data,
            deadline = form.deadline.data,
            duration = form.duration.data,
            introduce = form.introduce.data,
            cost = form.cost.data,
            people = form.people.data,
            location = form.location.data
        )
        file = request.files['activPic']
        filename = random_file_name(secure_filename(file.filename))
        # filename = secure_filename(file.filename)
        APP_ROOT = os.path.dirname(os.path.dirname(__file__))
        UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/upload')
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        # file_path_name = url_for('static', filename='images/' + filename),
        # file_path_name = ''.join([dir_name, filename])
        file_path_name=filename,
        ActivRele.activPic = file_path_name
        db.session.add(ActivRele)
        db.session.commit()
        flash('添加成功。。。')
        return redirect(url_for('project.admin.activity'))
    return render_template('activity/activity_add.html',form=form)


#修改活动发布
@admin.route("/activity/update/<int:id>",methods=['GET','POST'])
@login_required
def update_activity(id):
    activ_released=ActivReleased.query.get_or_404(id)
    form = UpdateActivForm()
    if form.validate_on_submit():
        # activ_released.activPic = form.activPic.data
        activ_released.title = form.title.data
        activ_released.duration = form.duration.data
        activ_released.deadline = form.deadline.data
        activ_released.startime = form.startime.data
        activ_released.introduce = form.introduce.data
        activ_released.cost = form.cost.data
        activ_released.people = form.people.data
        activ_released.location = form.location.data

        #图片上传
        file = request.files['activPic']
        filename = random_file_name(secure_filename(file.filename))
        # filename = secure_filename(file.filename)
        if filename:
            APP_ROOT = os.path.dirname(os.path.dirname(__file__))
            UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/upload')
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            file_path_name = filename,
            activ_released.activPic = file_path_name

        db.session.add(activ_released)
        db.session.commit()
        return redirect(url_for('project.admin.activity'))
    form.activPic.data = activ_released.activPic
    form.title.data = activ_released.title
    form.duration.data = activ_released.duration
    form.deadline.data = activ_released.deadline
    form.startime.data = activ_released.startime
    form.introduce.data = activ_released.introduce
    form.cost.data = activ_released.cost
    form.people.data = activ_released.people
    form.location.data = activ_released.location
    return render_template('activity/activity_edit.html', form=form,activ_released=activ_released)

#删除活动发布
@admin.route('/activity/<int:id>',methods=['GET','POST'])
@login_required
def del_activ(id):
    activity_released=ActivReleased.query.get_or_404(id)
    db.session.delete(activity_released)
    db.session.commit()
    return redirect(url_for('project.admin.activity'))


#搜索活动发布
@admin.route('/activity',methods=['GET','POST'])
@login_required
def activity():
    search_form = SearchActivForm()
    if search_form.validate_on_submit():
        keywords = search_form.keywords.data
        activities=ActivReleased.query.filter(or_(ActivReleased.title.like('%'+keywords+'%'),
                                              ActivReleased.cost.like('%'+keywords+'%')
                                                  )).all()
        return render_template('activity/activity_index.html',search_form=search_form,
                               activities=activities)
    page = request.args.get('page', 1, type=int)
    pagination = ActivReleased.query.order_by(ActivReleased.id).paginate(
         page,per_page=current_app.config['FLASY_NEWS_PER_PAGE'],
         error_out=False
     )
    activ_released = pagination.items
    return render_template('activity/activity_index.html', activities=activ_released,
                           search_form=search_form,pagination=pagination)


# simeditor上传
@admin.route('/upload/img', methods=['post'])
def upload_img_to_redactor_editor():
    file = request.files['file']
    if file:
        filename = file.filename
        import os
        APP_ROOT = os.path.dirname(os.path.dirname(__file__))
        UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/images')
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        path = url_for('static', filename='upload/' + filename)
        return jsonify(success=True, file_path=path)
    else:
        return jsonify(success=False, msg='上传失败')



#活动发布删除提示api
@admin.route("/api/delete/activity",methods=['GET','POST'])
def api_activity_delete():
    ActivReleased_id = request.form.get('id')
    activity = ActivReleased.query.get(ActivReleased_id)
    db.session.delete(activity)
    db.session.commit()
    return '1'


#捐赠校友删除提示api
@admin.route("/api/delete/alumni",methods=['GET','POST'])
def api_alumni_delete():
    alumni_id = request.form.get('id')
    alumnis = alumni.query.get(alumni_id)
    db.session.delete(alumnis)
    db.session.commit()
    return '1'

#删除友情链接
@admin.route("/api/delete/links",methods=['GET','POST'])
def api_links_delete():
    links_id = request.form.get('id')
    link = FriendshipLink.query.get(links_id)
    db.session.delete(link)
    db.session.commit()
    return '1'


#邮件发送
@admin.route("/api/send_email",methods=['GET', 'POST'])
def send_email():
    email = request.form.get('email')
    msg = Message(subject="西南科技大学成都校友会土建分会", sender='2476159529@qq.com', recipients=[email])
    msg.html = "尊敬的用户您好,现您已经通过校友会审核，恭喜您成为校友会会员！"
    mail.send(msg)
    return '成功了！'

