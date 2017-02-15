# coding:utf-8
import time
from datetime import datetime
from flask import redirect, url_for, flash, render_template, request, make_response, current_app, abort
from flask_login import logout_user, login_required, current_user, login_user
from .forms import LoginForm, RegisterAdminForm, EditAdminForm, DeleteAdminLog, QueryLogsForm
from ..models import User, Role, db, Log, LogType
from . import admin
from ..decorators import admin_required


# 登陆
@admin.route('/adminlogin', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  # 如果已登陆则跳到主界面
        return redirect(url_for('project.admin.index'))
    form = LoginForm()
    if form.validate_on_submit():
        log = Log()
        address = request.remote_addr
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            flash(u'用户名或者密码错误')
            return render_template("admin/adminlogin.html", form=form, name=form.username.data)
        if user.role_id != 2:
            flash(u'没有权限')
            return render_template("admin/adminlogin.html", form=form, name=form.username.data)
        if user is not None and user.verify_passwrod(form.password.data):
            login_user(user, form.remember_me.data)
            # 保存日志
            log.keep_log(page_name=u"管理员登陆", address=address, logtype=LogType.LOGIN, logpassword="",
                         admin_name=form.username.data, state=LogType.SUCCESS)
            return redirect(request.args.get('next') or url_for('project.admin.index'))
        # 登陆失败保存密码日志
        log.keep_log(page_name=u"管理员登陆", address=address, logtype=LogType.LOGIN, logpassword=form.password.data,
                     admin_name=form.username.data, state=LogType.FAIL)
        flash(u'用户名或者密码错误')
    return render_template("admin/base.html", form=form, name=form.username.data)


# 退出登陆
@admin.route('/loginout')
@login_required
def logout():
    logout_user()
    flash(u'退出登陆成功')
    return redirect(url_for('project.admin.login'))


# 管理员注册页面
@admin.route('/register', methods=['GET', 'POST'])
@login_required
@admin_required
def register():
    form = RegisterAdminForm()
    if form.validate_on_submit():
        log = Log()
        address = request.remote_addr
        user = User(username=form.username.data,
                    password=form.password.data,
                    name=form.name.data,
                    location=form.location.data,
                    about_me=form.about_me.data)
        db.session.add(user)
        db.session.commit()
        log.keep_log(page_name=u"管理员新增:" + form.username.data, address=address, logtype=LogType.ADD, logpassword='',
                     admin_name=current_user.id, state=LogType.SUCCESS)
        flash(u'会员注册成功！')
        return redirect(url_for('project.admin.login'))
    return render_template('admin/adminregister.html', form=form)


# 管理员列表

@admin.route('/admin_list', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_list():
    admin_role = Role.query.order_by(Role.id).all()
    return render_template('admin/admin_list.html', admin_role=admin_role)


# 修改管理员资料
@admin.route("/admin/update/<int:id>", methods=["GET", "post"])
@login_required
@admin_required
def update_admin(id):
    admin = User.query.get_or_404(id) or User()
    form = EditAdminForm(admin=admin)
    if form.validate_on_submit():
        log = Log()
        address = request.remote_addr
        try:
            admin.role = Role.query.get(form.role.data)
            admin.name = form.name.data
            admin.about_me = form.about_me.data
            admin.location = form.location.data
            if form.password.data:  # 如果输入了密码则更新密码
                admin.password = form.password.data
            db.session.add(admin)
            db.session.commit()
            form.username.data = admin.username
            flash(u'管理员资料修改成功！')
            log.keep_log(page_name=u"管理员资料修改:" + form.username.data, address=address, logtype=LogType.MODILY,
                         logpassword='',
                         admin_name=current_user.id, state=LogType.SUCCESS)

        except (), e:
            print e
            flash(u'系统错误，信息修改失败')
            return redirect(url_for('project.admin.update'))
    else:
        form.username.data = admin.username
        form.role.data = admin.role_id
        form.name.data = admin.name
        form.about_me.data = admin.about_me
        form.location.data = admin.location
    return render_template('admin/adminedit.html', form=form)


# 用户操作日志表
@admin.route('/admin/logs', methods=['GET', 'POST'])
@login_required
@admin_required
def logs():
    del_log_form = DeleteAdminLog()  # 删除日志表单
    del_log_form.del_list.data = del_log_form.del_list.data or 90
    log = Log.query.order_by(Log.id.desc())
    querlogsform = QueryLogsForm()
    if querlogsform.loginip.data == '':
        querlogsform.loginip.data = '0.0.0.0'

    # 查询表单提交
    if querlogsform.validate_on_submit():
        # 从form表单获取数据
        remarks = (querlogsform.remarks.data) or ''  # 备注
        date1 = str((querlogsform.date1.data)) or '2000-01-01'  # 时间段1
        date2 = str((querlogsform.date2.data)) or '2000-01-01'  # 时间段2
        user_operation = (querlogsform.user_operation.data) or ''  # 操作用户名
        loginip = (querlogsform.loginip.data) or '0.0.0.0'  # 登陆IP
        operration_type = (querlogsform.operration_type.data) or '0'  # 操作类型

    else:
        # 从cookie获取参数
        remarks = request.cookies.get('remarks') or ''  # 备注
        date1 = request.cookies.get('date1') or '2000-01-01'  # 时间段1
        date2 = request.cookies.get('date2') or '2000-01-01'  # 时间段2
        user_operation = request.cookies.get('user_operation') or ''  # 操作用户名
        loginip = request.cookies.get('loginip') or '0.0.0.0'  # 登陆IP
        operration_type = request.cookies.get('operration_type') or ''  # 操作类型
        # 对查询表单赋值
        querlogsform.remarks.data = remarks
        querlogsform.date1.data = datetime.strptime(date1, '%Y-%m-%d').date()
        querlogsform.date2.data = datetime.strptime(date2, '%Y-%m-%d').date()
        querlogsform.user_operation.data = user_operation
        querlogsform.loginip.data = loginip
        querlogsform.operration_type.data = operration_type

    # 查询过滤
    if remarks != '':
        log = log.filter(Log.pagename.like('%' + remarks + '%'))
    if date1 != '2000-01-01' and date2 != '2000-01-01':
        log = log.filter(Log.create_at.between(time.strftime(date1), time.strftime(date2 + ' 23:59:59')))
    if user_operation != '':
        log = log.filter(Log.admin_name.like('%' + user_operation + '%'))
    if loginip != '0.0.0.0':
        log = log.filter(Log.address.like('%' + loginip + '%'))
    if operration_type != '0':
        log = log.filter(Log.logtype.like('%' + operration_type + '%'))
    page = request.args.get('page', type=int) or 1
    # 用户操作日志分页表
    log = log.paginate(page=page,
                       per_page=
                       current_app.config[
                           'ADMIN_LIST_LOG'],
                       error_out=False)
    resp = make_response(render_template('admin/adminlogs_list.html', log=log,
                                         del_log_form=del_log_form, querlogsform=querlogsform))

    resp.set_cookie('remarks', remarks)
    resp.set_cookie('date1', date1.format('%Y-%m-%d'))
    resp.set_cookie('date2', date2.format('%Y-%m-%d'))
    resp.set_cookie('user_operation', user_operation)
    resp.set_cookie('loginip', loginip)
    resp.set_cookie('operration_type', operration_type)
    return resp


# 删除日志
@admin.route('/logs/dellog', methods=['GET', 'POST'])
@login_required
@admin_required
def del_logs():
    del_log_form = DeleteAdminLog()  # 删除日志表单
    if del_log_form.validate_on_submit():
        del_day = int(del_log_form.del_list.data) or 30
        record = del_log_form.del_logs(days=del_day)
        log = Log()
        address = request.remote_addr
        log.keep_log(page_name=u"删除日志:删除" + str(del_day) + "天前数据，本次删除" + str(record) + "条数据", address=address,
                     logtype=LogType.DELETE, logpassword='',
                     admin_name=current_user.username, state=LogType.SUCCESS)
    return redirect(url_for('project.admin.logs'))
