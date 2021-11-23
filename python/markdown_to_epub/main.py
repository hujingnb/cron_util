import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import pypandoc
from agrs import arg


def get_file_str_by_path(path: str, skip_file: list) -> str:
    """
    获取路径下所有 md 文件的内容
    """
    # 等待翻译的内容
    result = ''
    # 读取路径下所有文件
    files = os.listdir(path)
    files.sort()
    for file in files:
        # 跳过非 md 文件
        if not file.endswith('.md'):
            continue
        if file in skip_file:
            continue
        filename = os.path.join(path, file)
        with open(filename, 'r') as f:
            result += f.read()
    return result


if __name__ == '__main__':
    if arg.need_print_help():
        arg.print_help()
    # 等待翻译的内容
    convert_str = ''
    # 读取路径下所有文件
    if arg.in_path:
        convert_str = get_file_str_by_path(arg.in_path, arg.skip_file)
    # 读取文件内容
    elif arg.in_file:
        with open(arg.in_file, 'r') as f:
            convert_str = f.read()
    else:
        arg.print_help()
    pypandoc.convert_text(source=convert_str, to='epub', format='md', outputfile=arg.out_file)
