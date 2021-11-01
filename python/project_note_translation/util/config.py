# 初始化配置信息
import configparser
import os

_config = configparser.ConfigParser()
_config.read(os.path.dirname(__file__) + os.path.sep + '..' +
             os.path.sep + 'config' + os.path.sep + 'config.cfg')
# 有道翻译
YOUDAO_APP_KEY = _config.get('youdao', 'app_key')
YOUDAO_APP_SECRET = _config.get('youdao', 'app_secret')
