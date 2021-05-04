# flask session key
SECRET_KEY = '12345678'

# flask-fileuploads config
UPLOADED_FILES_DEST = 'static/upload' # file save folder path, this is required；
UPLOADED_FILES_ALLOW = ['txt','pdf']  # enabled file suffix
UPLOADED_FILES_DENY = ['html', 'py'] # disabled file suffix

# debug config
DEBUG_TB_ENABLED = False
DEBUG_TB_INTERCEPT_REDIRECTS = True