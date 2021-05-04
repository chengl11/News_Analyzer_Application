import os.path

from pdfminer.pdfparser import PDFParser,PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LTTextBoxVertical, LAParams, LTImage, LTCurve, LTFigure
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed

def convertPdfToText(filePath):
    print(filePath)
    # 以二进制读模式打开
    file = open(filePath, 'rb')
    #用文件对象来创建一个pdf文档分析器
    praser = PDFParser(file)
    # 创建一个PDF文档
    doc = PDFDocument()
    # 连接分析器 与文档对象
    praser.set_document(doc)
    doc.set_parser(praser)

    # 提供初始化密码
    # 如果没有密码 就创建一个空的字符串
    doc.initialize()

    # 检测文档是否提供txt转换，不提供就忽略
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # 创建PDf 资源管理器 来管理共享资源
        rsrcmgr = PDFResourceManager()
        # 创建一个PDF设备对象
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        # 创建一个PDF解释器对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        # 获得文档的目录（纲要）,文档没有纲要会报错
        #PDF文档没有目录时会报：raise PDFNoOutlines  pdfminer.pdfdocument.PDFNoOutlines
        # print(doc.get_outlines())

        # 用来计数页面，图片，曲线，figure，水平文本框等对象的数量
        num_page, num_image, num_curve, num_figure, num_TextBoxHorizontal, num_TextBoxVertical = 0, 0, 0, 0, 0, 0
        content_text = ''
        # 循环遍历列表，每次处理一个page的内容
        for page in doc.get_pages(): # doc.get_pages() 获取page列表
            num_page += 1  # 页面增一
            # 利用解释器的process_page()方法解析读取单独页数
            interpreter.process_page(page)
            # 接受该页面的LTPage对象
            layout = device.get_result()
            # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等 想要获取文本就获得对象的text属性，
            for x in layout:
                if hasattr(x, "get_text") or isinstance(x, LTTextBoxHorizontal) or isinstance(x, LTTextBoxVertical):
                    # 将'\xa0'替换成u' '空格，这个\xa0就是&nbps空格
                    results = x.get_text().replace(u'\xa0', u' ')
                    content_text += results
                # 如果x是水平文本对象的话
                if isinstance(x, LTTextBoxHorizontal):
                    num_TextBoxHorizontal += 1  # 水平文本框对象增一
                # 如果x是垂直文本对象的话
                if isinstance(x, LTTextBoxVertical):
                    num_TextBoxVertical += 1  # 水平文本框对象增一
                if isinstance(x, LTImage):  # 图片对象
                    num_image += 1
                if isinstance(x, LTCurve):  # 曲线对象
                    num_curve += 1
                if isinstance(x, LTFigure):  # figure对象
                    num_figure += 1
        return str(content_text)







    # # 用来计数页面，图片，曲线，figure，水平文本框等对象的数量
    # num_page, num_image, num_curve, num_figure, num_TextBoxHorizontal = 0, 0, 0, 0, 0
    #
    # # 循环遍历列表，每次处理一个page的内容
    # for page in PDFPage.create_pages(doc):
    #     num_page += 1  # 页面增一
    #     # 利用解释器的process_page()方法解析读取单独页数
    #     interpreter.process_page(page)
    #     # 接受该页面的LTPage对象
    #     layout = device.get_result()
    #     fileNames = os.path.splitext(filePath)
    #     # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象
    #     # 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等
    #     for x in layout:
    #         if hasattr(x, "get_text") or isinstance(x, LTTextBoxHorizontal):
    #             with open(fileNames[0] + '.txt','a+') as f:
    #                 # 将'\xa0'替换成u' '空格，这个\xa0就是&nbps空格
    #                 results = x.get_text().replace(u'\xa0', u' ')
    #                 f.write(results + '\n')
    #             document.add_paragraph(
    #                 results, style='ListBullet'  # 添加段落，样式为unordered list类型
    #             )
    #         document.save('./data/demo1.docx')  # 保存这个文档
    #
    #         # 如果x是水平文本对象的话
    #         if isinstance(x, LTTextBoxHorizontal):
    #             num_TextBoxHorizontal += 1  # 水平文本框对象增一
    #         if isinstance(x, LTImage):  # 图片对象
    #             num_image += 1
    #         if isinstance(x, LTCurve):  # 曲线对象
    #             num_curve += 1
    #         if isinstance(x, LTFigure):  # figure对象
    #             num_figure += 1
    #
    # print('对象数量：%s,页面数：%s,图片数：%s,曲线数：%s,'
    #       '水平文本框：%s,'%(num_figure,num_page,num_image,num_curve,num_TextBoxHorizontal))