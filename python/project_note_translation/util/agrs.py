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
        self.show_help = False
        self.in_path = None
        self.out_path = None
        self.suffix = None
        self.encoding = 'utf-8'
        tmp, args = getopt.getopt(sys.argv[1:], 'i:o:s:h', ['suffix=', 'out=', 'in=', 'help'])
        # 读取参数
        for comm in tmp:
            # 帮助文档
            if comm[0] == '-h' or comm[0] == '--help':
                self.show_help = True
            elif comm[0] == '-i' or comm[0] == '--in':
                self.in_path = comm[1]
            elif comm[0] == '-o' or comm[0] == '--out':
                self.out_path = comm[1]
            elif comm[0] == '-s' or comm[0] == '--suffix':
                self.suffix = comm[1]
        # 设置默认参数
        if not self.in_path:
            self.in_path = os.getcwd()
        if not self.out_path:
            self.out_path = '/tmp/' + os.path.basename(self.in_path)

    def need_print_help(self) -> bool:
        """
        检查是否需要输出帮助文档
        :return:
        """
        if self.show_help:
            return True
        # 缺少参数
        if not self.suffix:
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
    -i/--in: 输入项目路径, 默认为当前路径
    -o/--out: 输出项目路径, 默认为 /tmp/workspace_name
    -t/--type: 处理的文件名后缀
        制作者: 靖哥哥
        """)
        exit()

    @staticmethod
    def check_version():
        """
        检查python版本号
        """
        # Python2显示升级提示
        if sys.version < '3':
            print("""
抱歉, 暂不支持Python2
    请升级Python版本后重试
                """)
            exit()


# 实例化, 保证单例
arg = Args()
