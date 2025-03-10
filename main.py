import fanbookbotapi
import json
import logging
import coloredlogs
import processing_msg
# 创建日志记录器
logger = logging.getLogger(__name__)
# 配置 coloredlogs
coloredlogs.install(level='DEBUG', logger=logger)

def Rjson(file):
    with open(file, 'r', encoding='utf-8') as f:
        return json.load(f)
def Wjson(file,data):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data,f,ensure_ascii=False,indent=4)
    return True

logger.info('正在启动bot...')

# token从config.json中读取
config = Rjson('config.json')
bot_token = config['bot_token']
# 更新bot_id
bot_info=fanbookbotapi.getme(token=bot_token).text
bot_id=json.loads(bot_info)['result']['last_name']
config['bot_id'] = bot_id
Wjson('config.json',config)
logger.info(f'bot_id: {bot_id}')

def onMessage(ws,message):
    processing_msg.pm(ws,message,bot_token,bot_id)

# 建立ws连接
fanbookbotapi.bot_websocket(token=bot_token,onOpen=lambda:logger.info('连接成功'),onClose=lambda:logger.info('连接关闭'),onError=lambda e:logger.error(f'发生错误: {e}'),onMessage=onMessage)