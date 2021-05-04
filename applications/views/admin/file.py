import os


from flask import Blueprint, request, render_template, jsonify, current_app
from flask_login import login_required
from flask_marshmallow import Marshmallow
from marshmallow import fields
from sqlalchemy import desc

from applications.models import db
from applications.models.admin import File
from applications.service.route_auth import check_auth
from applications.service.upload import files
from applications.service.pdfTool import convertPdfToText

ma = Marshmallow()
admin_file = Blueprint('adminFile', __name__, url_prefix='/admin/file')


@admin_file.route('/')
@login_required
def index():
    return render_template('admin/file.html')


class FileSchema(ma.Schema):  # 序列化类
    id = fields.Integer()
    name = fields.Str()
    href = fields.Str()
    mime = fields.Str()
    size = fields.Str()
    ext = fields.Str()
    create_time = fields.DateTime()


@admin_file.route('/table')
@login_required
def table():
    page = request.args.get('page', type=int)
    limit = request.args.get('limit', type=int)
    files = File.query.order_by(desc(File.create_time)).paginate(page=page, per_page=limit, error_out=False)
    count = File.query.count()
    role_schema = FileSchema(many=True)
    output = role_schema.dump(files.items)
    res = {
        'msg': "",
        'code': 0,
        'data': output,
        'count': count,
        'limit': "10"

    }
    return jsonify(res)


@admin_file.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST' and 'file' in request.files:
        filename = files.save(request.files['file'])
        file_url = files.url(filename)
        file_path = files.path(filename);
        mime = request.files['file'].content_type
        upload_url = current_app.config.get("UPLOADED_FILES_DEST")
        size = os.path.getsize(upload_url + '/' + filename)
        suffix = os.path.splitext(filename)[1].lower()
        file = File(name=filename, href=file_url, path=file_path, mime=mime, size=size, ext=suffix)
        db.session.add(file)
        db.session.commit()
        res = {
            "msg": "upload sucess",
            "code": 0,
            "data":
                {"src": file_url}
        }
        return jsonify(res)

    return render_template('admin/file_add.html')


@admin_file.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():
    id = request.form.get('id')
    file_name = File.query.filter_by(id=id).first().name
    file = File.query.filter_by(id=id).delete()
    db.session.commit()
    upload_url = current_app.config.get("UPLOADED_FILES_DEST")
    os.remove(upload_url + '/' + file_name)
    if file:
        res = {"msg": "delete sucess", "code": 200}
        return jsonify(res)
    else:
        res = {"msg": "delete fail", "code": 999}
        return res


@admin_file.route('/batchRemove', methods=['GET', 'POST'])
@login_required
def batchRemove():
    ids = request.form.getlist('ids[]')
    file_name = File.query.filter(File.id.in_(ids)).all()
    upload_url = current_app.config.get("UPLOADED_FILES_DEST")
    for p in file_name:
        os.remove(upload_url + '/' + p.name)
    file = File.query.filter(File.id.in_(ids)).delete(synchronize_session=False)
    db.session.commit()
    if file:
        res = {"msg": "delete sucess", "code": 200}
        return jsonify(res)
    else:
        res = {"msg": "delete fail", "code": 999}
        return res

@admin_file.route('/convertToText', methods=['GET', 'POST'])
@login_required
def convertToText():
    id = request.form.get('id')
    file_name = File.query.filter_by(id=id).first().name
    suffix = os.path.splitext(file_name)[1].lower()
    if suffix == '.pdf':
        file_path = files.path(file_name)
        content = convertPdfToText(file_path)
        res = {"msg": "convert sucess", "code": 200, "data":{"text": content}}
        return jsonify(res)
    else:
        res = {"msg": "only support pdf file", "code": 999}
        return res

@admin_file.route('/keywords', methods=['GET'])
@login_required
def getContentKeywords():
    id = request.form.get('id')
    file_name = File.query.filter_by(id=id).first().name
    suffix = os.path.splitext(file_name)[1].lower()
    if suffix == '.pdf':
        file_path = files.path(file_name)
        content = convertPdfToText(file_path)
        # 使用NLP提取关键词、摘要

        # 1、生成词频柱状图（保存图片）
        # 2、解析关键词
        # 3、提取摘要
        # 以上信息需保存数据库



        res = {"msg": "convert sucess", "code": 200, "data":{"text": content}}
        return jsonify(res)
    else:
        res = {"msg": "only support pdf file", "code": 999}
        return res