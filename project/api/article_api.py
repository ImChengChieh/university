#!/user/bin/env python
# -*- coding: utf-8 -*-

import copy, datetime, os, uuid
from flask import request, jsonify, current_app, url_for, abort
from project import db
from project.models import Article, ArticleType, Log, LogType
from . import api
from flask_login import current_user


# 更新文章的api
@api.route("/article/update", methods=["post"])
def update_article():
    try:
        args = request.form
        article_id = int(args.get("id") or 0)
        article = Article.query.get(article_id) or Article()
        article.type_id = args['type_id']
        article.title = args.get("title")
        article.img = args.get("img")
        article.content = args.get("content")
        article.seo_title = args.get("seo_title") or article.title
        article.seo_keywords = args.get("seo_keywords")
        article.seo_description = args.get("seo_description")
        article.author = current_user.username

        db.session.add(article)
        db.session.commit()
        log = Log()
        address = request.remote_addr
        log.keep_log(page_name=u"修改文章:" + article.title, address=address, logtype=LogType.MODILY, logpassword='',
                     admin_name=current_user.username, state=LogType.SUCCESS)

        return jsonify(success=True, msg="更新成功！", article_id=article.id)
    except (), e:
        print e
        return jsonify(success=False, msg="更新失败,系统出错！")


# 删除文章的api
@api.route("/article/delete", methods=["post"])
def delete_article():
    try:
        article_id = int(request.form.get("article_id") or 0)
        article = Article.query.get(article_id)
        if article is None:
            return jsonify(success=False, msg="要删除的文章不存在！")
        db.session.delete(article)
        db.session.commit()
        log = Log()
        address = request.remote_addr
        log.keep_log(page_name=u"删除文章:" + article.title, address=address, logtype=LogType.DELETE, logpassword='',
                     admin_name=current_user.username, state=LogType.SUCCESS)
        return jsonify(success=True, msg="删除文章成功！")
    except (), e:
        print e
        return jsonify(success=False, msg="删除失败，系统错误！")


# 获取文章列表
@api.route("/article/list", methods=["post"])
def article_list():
    args = request.form
    page = int(args.get("page") or 1)
    type_id = int(args.get("type_id") or 0)
    keywords = args.get("keywords") or False

    query_build = Article.query

    # 根据文章类容查询
    if type_id:
        query_build = query_build.filter_by(type_id=type_id)

    # 根据标题模糊查询
    if keywords:
        query_build = query_build.filter(Article.title.ilike('%' + keywords + '%'))
    query_build = query_build.order_by(Article.id.desc())

    pagination = query_build.paginate(page=page, per_page=current_app.config["ARTICLE_LIST_ADMIN"], error_out=False)

    # 将分页对象解析为包含分页json数据的response
    def pase_pagination(pag_obj, paras=[int, unicode, long, datetime.datetime, ArticleType, bool]):
        pag_obj = copy.copy(pag_obj)
        items = pag_obj.items
        from flask import jsonify
        items_ = []
        for item in items:
            item_ = dict()
            if item.type:  # 使type外键加载，否则__dict__访问不到
                pass
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


# 上传文件
@api.route("/upload", methods=["post"])
def upload():
    try:
        file = request.files.get("file_cover")
        suffix = file.filename.rsplit(".")[len(file.filename.rsplit(".")) - 1]
        abpath = os.path.abspath(os.path.dirname(__file__) + "../../static/upload")

        if not os.path.exists(abpath):
            os.makedirs(abpath)

        filename = ".".join([str(uuid.uuid1()), suffix])
        destination = "/".join([abpath, filename])
        file.save(destination)
        return jsonify(success=True, file_path=url_for("static", filename="upload/" + filename))
    except (), e:
        print e
        return jsonify(success=False, msg="上传失败, 系统错误！")


# 置顶和取消置顶
@api.route("/article/top_or_cancel", methods=["post"])
def top_or_cancel():
    try:
        args = request.form
        id = args.get("article_id")
        article = Article.query.get(id)
        if not article:
            abort(401)
        top_article = Article.query.filter_by(top_to_index=True).first()
        article.top_to_index = True
        if top_article:
            top_article.top_to_index = False
        db.session.add(article, top_article)
        db.session.commit()
        return jsonify(success=True), 200
    except (), e:
        print e
        return jsonify(success=False), 500
