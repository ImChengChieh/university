#!/user/bin/env python
# -*- coding: utf-8 -*-

import copy, datetime, os, uuid
from flask import request, jsonify, current_app, url_for
from project import db
from project.models import FriendshipLink, Log, LogType
from . import api
from flask_login import current_user


# 更新友情链接的api
@api.route("/friendshiplink/update", methods=["post"])
def update_friendshiplink():
    try:
        args = request.form
        friendshiplink_id = int(args.get("id") or 0)
        friendshiplink = FriendshipLink.query.get(friendshiplink_id) or FriendshipLink()
        friendshiplink.title = args.get("title")
        friendshiplink.img = args.get("img")
        friendshiplink.link = args.get("link")

        db.session.add(friendshiplink)
        db.session.commit()
        log = Log()
        address = request.remote_addr
        log.keep_log(page_name=u"修改合作伙伴:<" + friendshiplink.title + ">", address=address,
                     logtype=LogType.MODILY, logpassword='',
                     admin_name=current_user.username, state=LogType.SUCCESS)

        return jsonify(success=True, msg="更新成功！", article_id=friendshiplink.id)
    except (), e:
        print e
        return jsonify(success=False, msg="更新失败,系统出错！")


# 删除友情链接的api
@api.route("/friendshiplink/delete", methods=["post"])
def delete_frindshiplink():
    try:
        friendshiplink_id = int(request.form.get("friendshiplink_id") or 0)
        friendshiplink = FriendshipLink.query.get(friendshiplink_id)
        if friendshiplink is None:
            return jsonify(success=False, msg="要删除的合作伙伴不存在！")
        db.session.delete(friendshiplink)
        db.session.commit()
        log = Log()
        address = request.remote_addr
        log.keep_log(page_name=u"删除合作伙伴:<" + friendshiplink.title + ">", address=address,
                     logtype=LogType.DELETE, logpassword='',
                     admin_name=current_user.username, state=LogType.SUCCESS)
        return jsonify(success=True, msg="删除合作伙伴成功！")
    except (), e:
        print e
        return jsonify(success=False, msg="删除失败，系统错误！")


# 获取合作伙伴列表
@api.route("/friendshiplink/list", methods=["post"])
def friendshiplink_list():
    args = request.form
    page = int(args.get("page") or 1)
    type_id = int(args.get("type_id") or 0)
    keywords = args.get("keywords") or False

    query_build = FriendshipLink.query

    # 根据文章类容查询
    if type_id:
        query_build = query_build.filter_by(type_id=type_id)

    # 根据标题模糊查询
    if keywords:
        query_build = query_build.filter(FriendshipLink.title.ilike('%' + keywords + '%'))
    query_build = query_build.order_by(FriendshipLink.id.desc())

    pagination = query_build.paginate(page=page, per_page=current_app.config["ARTICLE_LIST_LEN"], error_out=False)

    # 将分页对象解析为包含分页json数据的response
    def pase_pagination(pag_obj, paras=[int, unicode, long, datetime.datetime]):
        pag_obj = copy.copy(pag_obj)
        items = pag_obj.items
        from flask import jsonify
        items_ = []
        for item in items:
            item_ = dict()
            item_paras = item.__dict__
            for e in item_paras:
                if type(item_paras[e]) in paras:
                    item_[e] = str(item_paras[e])
            items_.append(item_)

        pag = pag_obj.__dict__
        pag.pop("query")
        pag["items"] = items_
        return jsonify(pag)

    return pase_pagination(pagination)
