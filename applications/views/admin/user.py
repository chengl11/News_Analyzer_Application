from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from flask_marshmallow import Marshmallow
from marshmallow import fields

from applications.models import db
from applications.models.admin import User
from applications.service.route_auth import check_auth

admin_user = Blueprint('adminUser', __name__, url_prefix='/admin/user')
ma = Marshmallow()

# ----------------------------------------------------------
# -------------------------  user manage --------------------------
# ----------------------------------------------------------


@admin_user.route('/')
@login_required
def index():
    return render_template('admin/user.html')


# ==========================================================
#                              query user
# ==========================================================


class UserSchema(ma.Schema):
    id = fields.Integer()
    username = fields.Str()
    status = fields.Bool()
    create_at = fields.DateTime()
    update_at = fields.DateTime()


@admin_user.route('/table')
@login_required
def table():
    page = request.args.get('page', type=int)
    limit = request.args.get('limit', type=int)
    user = User.query.paginate(page=page, per_page=limit, error_out=False)
    role_schema = UserSchema(many=True)
    output = role_schema.dump(user.items)
    res = {
        'msg': "",
        'code': 0,
        'data': output,
        'count': 1,
        'limit': "10"

    }
    return jsonify(res)


# ==========================================================
#                              add user
# ==========================================================


@admin_user.route('/insert', methods=['GET', 'POST'])
@login_required
def insert():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username and password:
            if User.query.filter_by(username=username).first() is None:
                user = User(username=username)
                user.set_password(password)
                db.session.add(user)
                db.session.commit()

                res = {"msg": "add sucess", "code": 200}
                return jsonify(res)

            else:
                res = {"msg": "user already exist", "code": 999}
                return jsonify(res)
        else:
            res = {"msg": "username or password is required", "code": 999}
            return jsonify(res)


    else:
        return render_template('admin/user_add.html')


# ==========================================================
#                              delete user
# ==========================================================


@admin_user.route('/delete', methods=['POST'])
@login_required
def delete():
    id = request.form.get('id')
    if User.query.filter_by(id=id).first() is not None:
        u = User.query.filter_by(id=id).first()
        if u.username == "admin":
            res = {"msg": "'admin' user does not allow deletion", "code": 400}
            return jsonify(res)
    else:
        res = {"msg": "user not fund", "code": 200}
        return jsonify(res)
    user = User.query.filter_by(id=id).delete()
    db.session.commit()
    if user:
        res = {"msg": "delete sucesse", "code": 200}
        return jsonify(res)
    else:
        res = {"msg": "delete fail", "code": 999}
        return res


# ==========================================================
#                              update user
# ==========================================================


@admin_user.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        if username and role:
            if password is None:
                if User.query.filter_by(id=id).first() is not None:
                    user = User.query.filter_by(id=id).update({'username': username, 'role': role})
                    db.session.commit()

                    res = {"msg": "update sucess", "code": 200}
                    return jsonify(res)

                else:
                    res = {"msg": "user already exist", "code": 200}
                    return jsonify(res)
            else:
                user = User.query.filter_by(id=id).first()
                if user is not None:
                    User.query.filter_by(id=id).update({'username': username, 'role': role})
                    user.set_password(password)
                    db.session.commit()

                    res = {"msg": "update sucess", "code": 200}
                    return jsonify(res)

                else:
                    res = {"msg": "user not fund", "code": 200}
                    return jsonify(res)

        else:
            res = {"msg": "username or password is required", "code": 999, "test": str(username)}
            return jsonify(res)
    else:
        user = User.query.filter_by(id=id).first()
        return render_template('admin/user_edit.html', user=user)


# ==========================================================
#                              update user status
# ==========================================================

@admin_user.route('/update/status', methods=['POST'])
@login_required
def ustatus():
    id = request.form.get('id')
    status = request.form.get('status')
    if id and status:
        user = User.query.filter_by(id=id).update({'status': status})
        if user:
            db.session.commit()
        res = {"msg": "update sucess", "code": 200}
        return jsonify(res)
    return {"msg": "update fail", "code": 999}


@admin_user.route('/batchRemove',methods=['GET','POST'])
@login_required
def batchRemove():
    ids = request.form.getlist('ids[]')
    user = User.query.filter(User.id.in_(ids)).delete(synchronize_session=False)
    db.session.commit()
    if user:
        res = {"msg": "delete sucess", "code": 200}
        return jsonify(res)
    else:
        res = {"msg": "delete fail", "code": 999}
        return res


