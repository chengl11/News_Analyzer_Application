from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from flask_marshmallow import Marshmallow
import urllib.parse
import io
import sys
import requests
from marshmallow import fields
from bs4 import BeautifulSoup

from applications.service.route_auth import check_auth


admin_news_ingester = Blueprint('admin_news_ingester', __name__, url_prefix='/admin/newsIngester')
ma = Marshmallow()

# ----------------------------------------------------------
# -------------------------  news feed ingester ------------
# ----------------------------------------------------------


@admin_news_ingester.route('/')
@login_required
def index():
    return render_template('admin/newsIngester.html')


@admin_news_ingester.route('/ingest', methods=['POST'])
@login_required
def ingest():
    url = request.form.get('url')
    rule = request.form.get('rule')
    if url and rule:
        url = urllib.parse.unquote(url)
        # sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
        response= requests.get(url)
        print(response.status_code)
        print(response.encoding)
        print(response.apparent_encoding)
        response.encoding = 'utf-8'
        result = response.text
        bs = BeautifulSoup(result,'html.parser')
        a = ''
        data=bs.find_all(rule)
        for i in data:
            a +=i.text + '\n'
        res = {"msg": "ingest sucess", "code": 200, "data": a}
        return jsonify(res)
    else:
        res = {"msg": "href or rule is required", "code": 999}
        return jsonify(res)
