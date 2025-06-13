import base64
import json
import os
import uuid

import pdfplumber
from fastapi import HTTPException
import ocrmypdf

from fastapi import APIRouter, UploadFile
from fastapi.params import Query, File
from starlette.responses import FileResponse

# 从环境变量读取 config.json 路径，未设置则用当前目录
config_file = os.environ.get("OCR_MY_PDF_CONFIG", "config.json")
with open(config_file, "r", encoding="utf-8") as f:
    config_json = json.load(f)

work_file_path = config_json.get("default_file_path", "./")

router = APIRouter()


@router.post("/upload_pdf_file")
async def upload_pdf_file(file: UploadFile = File(...)):
    # 读取上传的文件内容
    pdf_data = await file.read()
    file_path, file_name, new_file_path, new_file_name = gen_file_path()
    # 保存原始 PDF
    with open(file_path, "wb") as file:
        file.write(pdf_data)

    # 调用 OCR 处理
    ocrmypdf.ocr(file_path, new_file_path, deskew=True)
    # result = subprocess.run(['ocrmypdf', file_path, new_file_path], capture_output=True, text=True)
    # print(result.stdout)
    return {"old_file_name": file_name, "new_file_name": new_file_name}


@router.post("/upload_base64")
async def upload_base64(
        pdf_base64_data: str = Query(..., description="pdf文件的base64字符串")  # ... 表示必填参数
) -> dict:
    """
    处理PDF文件的OCR识别请求
    :param pdf_base64_data:
    :return: json
    """
    pdf_data = base64.b64decode(pdf_base64_data)
    file_path, file_name, new_file_path, new_file_name = gen_file_path()
    print(f"input_file_path: {file_path}")
    print(f"input_file_name: {file_name}")
    print(f"new_file_path: {new_file_path}")
    print(f"new_file_name: {new_file_name}")
    # 写入文件
    # wb 表示以“二进制写入”模式打开文件（write binary）。用于写入二进制数据（如图片、PDF等），而不是文本数据。
    with open(file_path, "wb") as file:
        file.write(pdf_data)

    # 调用 OCR 处理
    ocrmypdf.ocr(file_path, new_file_path, deskew=True)
    # result = subprocess.run(['ocrmypdf', file_path, new_file_path], capture_output=True, text=True)
    # print(result.stdout)

    # 这是一个 Python 字典（dict），不是 JSON 字符串。但 FastAPI 会自动将它序列化为 JSON 格式返回给前端，所以接口响应内容是 JSON。
    # 也可以用 json.dumps() 进行序列化。
    return {"old_file_name": file_name, "new_file_name": new_file_name}


@router.get("/ocr_and_get_pdf_file")
async def ocr_and_get_pdf_file(file_name: str) -> FileResponse:
    # 拼接文件路径
    file_path = os.path.join(work_file_path, file_name)
    # 检查文件是否存在
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="文件未找到")
    # 返回文件响应
    return FileResponse(file_path, filename=file_name)


@router.get("/ocr_and_get_base64")
async def ocr_and_get_base64(file_name: str) -> dict:
    # 拼接文件路径
    file_path = os.path.join(work_file_path, file_name)
    # 检查文件是否存在
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="文件未找到")
    # 返回文件的bas64编码
    with open(file_path, "rb") as file:
        pdf_data = file.read()
    pdf_base64_data = base64.b64encode(pdf_data).decode('utf-8')
    return {"pdf_base64_data": pdf_base64_data}

@router.get("/ocr_and_get_pdf_text")
async def ocr_and_get_pdf_text(file_name: str) -> dict:
    """
    获取PDF文件的文本内容
    :param file_name: PDF文件名
    :return: 包含文本内容的字典
    """
    file_path = os.path.join(work_file_path, file_name)
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="文件未找到")

    # 使用ocrmypdf提取文本
    try:
        with pdfplumber.open(file_path) as pdf:
            text = ''.join(page.extract_text() or '' for page in pdf.pages)
        # print(text)
        return {"text": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def gen_file_path(path: str = work_file_path) -> tuple:
    """
    生成一个唯一的文件路径
    """
    uuid_str = str(uuid.uuid4())
    file_path = work_file_path
    if not file_path.endswith("/"):
        file_path += "/"

    input_file_path = os.path.join(file_path, uuid_str + ".pdf")
    input_file_name = uuid_str + ".pdf"

    new_file_path = os.path.join(file_path, uuid_str + ".new.pdf")
    new_file_name = uuid_str + ".new.pdf"
    return input_file_path, input_file_name, new_file_path, new_file_name
