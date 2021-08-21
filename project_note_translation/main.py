import os

from util import *


def translate_project(in_path, out_path, suffix):
    """
    翻译项目
    :param in_path:
    :param out_path:
    :param suffix:
    """
    # 扫描路径中的所有文件
    for root, dirs, files in os.walk(in_path):
        for file in files:
            # 获取文件的输入路径
            in_file_path = os.path.join(root, file)
            # 获取文件的输出路径
            out_file_path = in_file_path.replace(in_path, out_path)
            # 若不是需要翻译的文件, 直接二进制读取复制
            if file.endswith('.' + suffix):
                print('翻译文件: ' + in_file_path)
                translate_note_and_write(in_file_path, out_file_path)
            else:
                print('拷贝文件: ' + in_file_path)
                copy_file(in_file_path, out_file_path)


if __name__ == '__main__':
    # 检查版本号
    arg.check_version()
    # 判断是否需要输出帮助文档
    if arg.need_print_help():
        arg.print_help()
    print('接收到输入路径: ' + arg.in_path)
    translate_project(arg.in_path, arg.out_path, arg.suffix)
    print('翻译完成, 输出路径为: ' + arg.out_path)
