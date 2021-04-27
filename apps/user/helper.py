# # Goal of this file is to connect
# # user route to blueprint
# from flask import Flask
# from flask import Blueprint, render_template
# from flask import request, make_response
# from flask import render_template
# from flask import abort, redirect, url_for
# from PyPDF2 import PdfFileReader, PdfFileWriter

# # UPLOAD_FOLDER = "static"
# ALLOWED_EXTENSIONS = {'pdf'}

# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# def getOnlyFileName(filename):
#     return filename.rsplit('.', 1)[0]

# # Extract the PDF file, return a list contains contents of each page
# # input: file_name: the PDF file
# # return: a list contains contents of each page
# def fileExtract(file):

#     all_text = []

#     pdfReader = PdfFileReader(file)

#     for i in range(0, pdfReader.numPages):
#         page = pdfReader.getPage(i)
#         page_content_str = page.extractText()
#         all_text.append(page_content_str)

#     text_file = convertToTxt(file.filename, all_text)

#     return all_text

# # Convert all content of pdf file into a txt file and store it in static/files
# # input: list contains contents of each page of a pdf file
# # return: txt file
# def convertToTxt(file_name, all_text):
#     txt_file_name = getOnlyFileName(file_name) + ".txt"
#     text_file= open("static/files/%s" % txt_file_name, "w" )
#     for str_page in all_text:
#         text_file.write(str_page)
#     text_file.close()
#     return text_file