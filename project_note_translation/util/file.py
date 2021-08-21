import os
import re
from .translation import youdao_translation


def translate_note_and_write(in_file_path: str, out_file_path: str):
    """
    将文件中的注释翻译后写出到新的路径下
    :param in_file_path:
    :param out_file_path:
    """
    mk_file_dir(out_file_path)
    # 读取文件内容
    with open(in_file_path, 'r') as f:
        content = f.read()
    ret_content = content
    # 从文件中提取注释内容并翻译
    # 提取多行注释
    more_pattern = re.compile(r'/\*[\s\S]*?\*/')
    note_more_lines = more_pattern.findall(content)
    for note in note_more_lines:
        note = str(note)
        tran_content = note
        # 多行注释掐头去尾. 防止翻译将字符替换了, 导致报错
        ind1 = tran_content.find('\n')
        if ind1 != -1:
            tran_content = tran_content[ind1 + 1:]
        ind2 = tran_content.rfind('\n')
        if ind2 != -1:
            tran_content = tran_content[:ind2]
        # 若仍然以注释的开始结束符号作为开头和结尾
        # 说明这时单行注释, 将其替换掉
        if tran_content.startswith('/*'):
            tran_content = tran_content[2:]
        if tran_content.endswith('*/'):
            tran_content = tran_content[:-2]
        # 将翻译内容替换
        tran = youdao_translation(tran_content)
        ret_content = ret_content.replace(tran_content, tran)
    # 提取单行注释
    # 将多行注释从内容中去掉, 防止单行注释提取的时候重复匹配
    sub_content = re.sub(more_pattern, '', content)
    for line_re in ['//.*\n', '#.*\n']:
        line_pattern = re.compile(line_re)
        note_lines = line_pattern.findall(sub_content)
        for note in note_lines:
            tran_note = str(note)
            # 去掉换行符. 因为翻译会将换行符去掉, 导致输出内容错误
            tran_note = tran_note.replace('\n', '')
            if tran_note.startswith('//'):
                tran_note = tran_note[2:]
            tran = youdao_translation(tran_note)
            ret_content = ret_content.replace(tran_note, tran)
    # 将结果写出
    with open(out_file_path, 'w') as w:
        w.write(ret_content)


def copy_file(in_file_path: str, out_file_path: str):
    """
    复制文件
    :param in_file_path:
    :param out_file_path:
    """
    mk_file_dir(out_file_path)
    with open(in_file_path, 'rb') as f, open(out_file_path, 'wb') as w:
        # 读取文件内容
        content = f.read()
        # 输入文件到新路径下
        w.write(content)


def mk_file_dir(file_path):
    """
    为文件创建文件夹
    :param file_path:
    """
    out_dir_path = os.path.dirname(file_path)
    os.makedirs(out_dir_path, exist_ok=True)
