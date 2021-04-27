from flask import Blueprint, render_template
from flask import request, make_response
from flask import abort, redirect, url_for
from werkzeug.utils import secure_filename


import os

from apps.article.extract_file import fileExtract
from apps.article.extract_file import allowed_file

from apps.article.sentiment_analysis import analyze
from apps.article.sentiment_analysis import print_result


from apps.user.models import User
from exts import db

user_bp = Blueprint("user", __name__)


@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        repassword = request.form.get("repassword")
        
        # check two password inputs are same
        if password == repassword:
            # create user
            user = User()
            user.username = username
            user.password = password

            db.session.add(user)
            db.session.commit()
            return redirect(url_for('user.user_center'))   # redirect to user_center()
        else:
            return render_template("user/register.html", msg="passwords not match!")

    return render_template("user/register.html")

@user_bp.route('/')
def user_center():
    # 查询数据库中的数据
    users = User.query.all()    # select * from user
    print(users)    # [<User 1>, <User 2>, <User 3>, <User 4>]
    return render_template('user/center.html', users=users)

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # select * from user where username = 'xxx'
        user_list = User.query.filter_by(username=username)
        print("111111111111111111user_list: ", user_list)
        for u in user_list:
            print("22222222each: ", u.username)
            if (u.password == password):
                return redirect(url_for('user.file_upload'))   # redirect to user_center()

        else:
            return render_template("user/login.html", msg='username or password is wrong!')

        return redirect(url_for('user.user_center'))   # redirect to user_center()

    return render_template("user/login.html")

@user_bp.route('/search')
def search():
    keyword = request.args.get('search')    # username
    # find
    user_list = User.query.filter(User.username.contains(keyword));
    
    return render_template('user/center.html', users=user_list)


@user_bp.route('/delete')
def delete():
    id = request.args.get('id')    # username
    # find user
    user = User.query.get(id)
    # 将对象放到缓存中准备删除
    db.session.delete(user)
    # 提交删除
    db.session.commit()
    
    return redirect(url_for('user.user_center'))

@user_bp.route("/file_upload", methods=["GET", "POST"])
def file_upload():
    # print(request.files)
    if request.method == "POST":
        # check if the post request has the file part
        if "file" not in request.files:
            return render_template("user/fileUpload.html", msg="post request doesn't have file part")
        file = request.files.get("file")

        # submit an empty part without filename
        if file.filename == '':
            return render_template("user/fileUpload.html", msg="no file selected")

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # file.save("static/files/%s" % filename)
            all_texts = fileExtract(file)   # get all texts in txt file splitted by page
            # txt_file.save("static/files/%s" % txt_file)
            result_list = analyze(all_texts[0])
            #print(result_list)
            return render_template("user/fileUpload.html", msg="upload file {} success".format(filename), result=result_list, filename=filename)

    return render_template("user/fileUpload.html")