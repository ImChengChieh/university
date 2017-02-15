#!/user/bin/env python
# -*- coding: utf-8 -*-

import copy, datetime
from flask import request, jsonify, current_app
from flask_login import current_user
from project import db
from project.models import User, Role,Log,LogType
from . import api


# 删除文章的api
@api.route("/admin/delete", methods=["post"])
def delete_admin():
    try:
        admin_id = int(request.form.get("admin_id") or 0)
        admin = User.query.get(admin_id)
        if admin is None:
            return jsonify(success=False, msg="要删除的用户不存在！")
        db.session.delete(admin)
        db.session.commit()
        log = Log()
        address = request.remote_addr
        log.keep_log(page_name=u"删除管理员:<" + User.username + ">" + User.name, address=address,
                     logtype=LogType.DELETE, logpassword='',
                     admin_name=current_user.username, state=LogType.SUCCESS)
        return jsonify(success=True, msg="删除管理员成功！")
    except (), e:
        print e
        return jsonify(success=False, msg="删除失败，系统错误！")


# 获取用户列表
@api.route("/admin/list", methods=['post','get'])
def admin_list():
    args = request.form
    page = int(args.get("page") or 1)
    role_id = int(args.get("role") or 0)
    keywords = args.get("keywords") or False

    query_build = User.query

    # 根据文章类容查询
    if role_id:
        query_build = query_build.filter_by(role_id=role_id)

    # 根据标题模糊查询
    if keywords:
        query_build = query_build.filter(User.username.ilike('%' + keywords + '%'))
    query_build = query_build.order_by(User.id.desc())

    pagination = query_build.paginate(page=page, per_page=current_app.config["ADMIN_LIST_ADMIN"], error_out=False)

    # 将分页对象解析为包含分页json数据的response
    def pase_pagination(pag_obj, paras=[int, unicode, long, datetime.datetime,role_id]):
        pag_obj = copy.copy(pag_obj)
        items = pag_obj.items
        from flask import jsonify
        items_ = []
        for item in items:
            item_ = dict()
            if item.role_id:  # 使type外键加载，否则__dict__访问不到
                pass
            item_paras = item.__dict__

            for e in item_paras:
                if type(item_paras[e]) in paras:
                    item_[e] = str(item_paras[e])
            item_['rolename'] = item.role.name
            items_.append(item_)
        pag = pag_obj.__dict__
        pag.pop("query")
        pag["items"] = items_
        return jsonify(pag)

    return pase_pagination(pagination)

