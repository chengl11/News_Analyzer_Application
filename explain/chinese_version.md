提前安装：  
虚拟环境  
1. cd your-project
2. py -m venv env // 在一个名为 env 的文件夹中创建虚拟副本
3. .\env\Scripts\activate  // 激活该虚拟环境
4. deactivate  // 停止使用虚拟环境并返回到全局 Python
5. pip install virtualenv
6. pip install flask
7. pip install flask-script
8. pip install pysql
9. pip install flask-sqlalchemy
10. pip install flask-migrate
11. pip install PyPDF2
12. pip install google-cloud-storage
13. pip install --upgrade google-cloud-speech

可以通过运行 pip list 查看安装列表

创建settings.py文件，在文件中设置数据库名
在mysql中提前创建一个对应的数据库名，通过MYSQL WORKBENCH，
创建数据库方法:
create database newdatabase charset = utf8
调用该数据库方法：
use newdatabase
展示内部tables方法：
show tables
展示具体table中的每一项
desc user

3. 创建static文件夹存储静态文件，templates文件夹存储HTML文件，app.py文件用于激活项目
    1. 在app.py文件中
        1. 创建app.run()
        2. 导入Manager(app=app)
        3. 导入create_app()函数,因为没有创建app文件夹
4. 创建apps文件夹
    1. 创建__init__.py定义create_app()函数
5. 添加数据库(MYSQL))交互模块
    1. 创建一个exts文件夹，创建__init__.py定义db
    2. 在apps/__init__.py的create_app()函数中初始化db  
    3. 通过命令管理db：在app.py中创建migrate,在manager的命令中添加db,在main中改成manager.run()
    4. 在apps文件夹中创建user,article文件夹  
    5. 在user文件夹中创建__init__.py,view.py,models.py  
    6. 在models.py中创建User class继承db.Model  
    7. 在app.py导入User, 开始迁移同步，运行3个代码：  
        1. python3 app.py db init      //生成migrations文件夹  
        2. python3 app.py db migrate   //产生版本文件  
        3. python3 app.py db upgrade   //添加user table到新数据库中  
6. 添加注册模块
    1. 在apps/user/view.py中添加蓝图blueprint
    2. 添加user_center路由
    3. 添加register路由
    4. 添加login路由
    5. 在templates文件夹创建user文件夹再放入center.html,register.html,login.html
    6. 在apps/__init__.py的create_app()函数中注册蓝图
7. 添加文件上传file_upload模块
    1. 添加fileUpload.html
    2. 添加file_upload路由
    3. 引入extract_file.py 用来将上传的PDF文件转换成txt文件并保存在static/files文件夹中
8. 添加文字情感分析模块
    1. 在apps/article文件夹中引入sentiment_analysis.py
    2. 在file_upload路由中导入sentiment_analysis.py文件用来分析文字的情感
    3. 将分析好的数据传回fileUpload.html页面显示