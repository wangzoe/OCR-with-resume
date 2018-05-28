# 简历格式统一的转化：非PDF 到 PDF 到 PNG
# PNG的读取
# 内容的输出
# 正则表达，分类信息

from aip import AipOcr
from wand.image import Image
from wand.color import Color
import io
from PyPDF2 import PdfFileReader, PdfFileWriter
import ghostscript
import time
import re


APP_ID = '11293265'
API_KEY = 'FczPa3jOrR8pOkERD057nykE'
SECRET_KEY = 'U9GiGICphWGMsQzkB8ngXWuGkoTspW2W'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)


def get_pic_content(filepath):
    '''读取图片'''
    with open(filepath, 'rb') as fp:
        return fp.read()

def getPdfReader(filename):
    # 取PDF文件
    reader = memo.get(filename, None)
    if reader is None:
        reader = PdfFileReader(filename, strict=False)
        memo[filename] = reader
    return reader

def run_convert(filename, page, res=120):
    # PDF转JPG
    idx = page + 1
    pdfile = getPdfReader(filename)
    pageObj = pdfile.getPage(page)
    dst_pdf = PdfFileWriter()
    dst_pdf.addPage(pageObj)

    pdf_bytes = io.BytesIO()
    dst_pdf.write(pdf_bytes)
    pdf_bytes.seek(0)

    img = Image(file=pdf_bytes, resolution=res)
    img.format = 'png'
    img.compression_quality = 90
    img.background_color = Color("white")
    img_path = '%s%d.png' % (filename[:filename.rindex('.')], idx)
    img.save(filename=img_path)
    img.destroy()
    return img_path


#主程序：
memo = {}
''' 回头这里写一个循环处理文件夹内文件
'''
path = run_convert('CV of Chen Yutong_YITU.pdf',0)
print(time.time())

img = get_pic_content(path)
msg = client.basicGeneral(img)
# msg返回类型为字典
text = msg.get('words_result')
# 返回类型为list，但是里面嵌套dict，key均为words，value为不同的文字内容；通常一行为一对键值对
content = []
#所有内容形成一个list，一行内容一个元素
for j in text:
        content.append(j.get('words'))


#接下来做一点正则表达式的规则，提取关键信息：姓名、电话、邮件、公司，不知道正则的效果会怎样。。。

#电话的正则：
phoneReg = re.compile(r'\+?\(?\d{3,}\)?-?\(?\d{4,}\)?')
#姓名的正则：
nameReg = re.compile(r'[/u4e00-/u9fa5]{2,5}')
# 这只是选取了2-5个中文字符。怎么能是常见姓+中文字符，的匹配？
#邮箱的正则：
emailReg = re.compile(r'[a-zA-Z0-9_\-\.]+@.*')

