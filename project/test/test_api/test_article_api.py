#!/user/bin/env python
# -*- coding: utf-8 -*-
from flask import url_for, json
from project.models import Article
from base import BaseTestCase


class TestArticleApi(BaseTestCase):
    # 发布文章测试
    def test_update_article(self):
        response = self.add_article()
        self.assertTrue(response.status_code == 200)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertTrue(json_response['success'] == True)

    # 获取文章列表测试
    def test_get_articles(self):
        response = self.add_article()
        self.assertTrue(response.status_code == 200)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertTrue(json_response['success'] == True)

        response = self.client.post(url_for('project.api.article_list'), data={
            "type_id": "1",
            "keywords": "测试"
        })

        json_response = json.loads(response.data.decode('utf-8'))
        self.assertTrue(len(json_response["items"]) != 0)

    # 删除文章测试
    def test_delete_article(self):
        response = self.add_article()
        self.assertTrue(response.status_code == 200)
        json_response = json.loads(response.data.decode('utf-8'))
        article_id = json_response["article_id"]

        response = self.client.post(url_for('project.api.delete_article'), data={
            "article_id": article_id
        })
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertTrue(json_response['success'] == True)

    # 添加一篇测试文章的方法
    def add_article(self):
        response = self.client.post(url_for('project.api.update_article'),
                                    data={
                                        "id": "",
                                        "type_id": "1",
                                        "title": "测试文章",
                                        "img": "",
                                        "content": "测试文章测试文章测试文章测试文章",
                                        "seo_title": "",
                                        "seo_keywords": "",
                                        "seo_description": "",
                                    })
        return response
