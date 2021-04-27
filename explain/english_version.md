pre-requirement install：  
1. cd your-project
2. py -m venv env // create venv in env
3. .\env\Scripts\activate  // active venv
4. deactivate  // stop venv
5. pip install virtualenv
6. pip install flask
7. pip install flask-script
8. pip install pysql
9. pip install flask-sqlalchemy
10. pip install flask-migrate
11. pip install PyPDF2
12. pip install google-cloud-storage
13. pip install --upgrade google-cloud-speech

run pip list to watch pip list

1. create settings.py and add MYSQL database name
2. create database newdatabase charset = utf8  // create database in MYSQL WORKBENCH\
3. create static folder to store css/files/js，templates folder to store HTML，app.py to active whole project
    1. in app.py
        1. create app.run()
        2. add Manager(app=app)
        3. add create_app() function
4. create apps folder
    1. create __init__.py and add create_app()
5. add database module
    1. create exts folder，create __init__.py and define db
    2. in apps/__init__.py, in create_app() init db  
    3. manage db by using command：create migrate in app.py, add db in manager, change app.run() to manager.run() in main()
    4. create user,article folder in apps folder
    5. in user folder create __init__.py, view.py, models.py  
    6. in models.py create User class and extends db.Model  
    7. in app.py add User, run 3 commands in terminal 
        1. python3 app.py db init      // init migrations folder
        2. python3 app.py db migrate   // create version file
        3. python3 app.py db upgrade   // add user table into new database
6. add login module
    1. in apps/user/view.py add blueprint
    2. add user_center router
    3. add register router
    4. add logi router
    5. in templates, create user folder and create center.html,register.html,login.html in it
    6. in apps/__init__.py, in create_app() register blueprint
7. add file_upload module
    1. add fileUpload.html
    2. add file_upload router
    3. add extract_file.py to transfer uploaded PDF file to txt file and store it in static/files folder
8. add sentiment_analysis module
    1. in apps/article folder add sentiment_analysis.py
    2. in file_upload router add sentiment_analysis.py to analyze sentiment of a txt file
    3. transfer all data back to fileUpload.html and present them