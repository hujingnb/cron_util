"""
命令行读取
@author hujing
"""
import getopt
import os
import sys


class Args:
    """
    用于处理全局参数
    """

    def __init__(self):
        self.in_path = None
        self.in_file = None
        self.out_file = None
        self.show_help = False
        self.skip_file = []
        tmp, args = getopt.getopt(sys.argv[1:], 'p:f:o:s:h', ['path=', 'out=', 'file=', 'skip=', 'help'])
        # 读取参数
        for comm in tmp:
            # 帮助文档
            if comm[0] == '-h' or comm[0] == '--help':
                self.show_help = True
            elif comm[0] == '-f' or comm[0] == '--file':
                self.in_file = comm[1]
            elif comm[0] == '-p' or comm[0] == '--path':
                self.in_path = comm[1]
            elif comm[0] == '-s' or comm[0] == '--skip':
                self.skip_file.append(comm[1])
            elif comm[0] == '-o' or comm[0] == '--out':
                self.out_file = comm[1]
        # 设置默认参数
        if not self.in_path and not self.in_file:
            self.in_path = os.getcwd()
        if not self.out_file:
            self.out_file = './out.epub'

    def need_print_help(self) -> bool:
        """
        检查是否需要输出帮助文档
        :return:
        """
        if self.show_help:
            return True
        return False

    @staticmethod
    def print_help() -> None:
        """
        输出帮助文档
        """
        print("""
参数如下: 
    -h/--help: 显示帮助文档
    -p/--path: 转换目录(默认当前目录)
                会将当前路径下的所有 md 文件, 按照名称排序后转换
    -s/--skip: 跳过文件, 与 -p 配合使用
    -f/--file: 转换文件
    -o/--out:  转换后的输出文件
        制作者: 靖哥哥
        """)
        exit()


# 实例化, 保证单例
arg = Args()
