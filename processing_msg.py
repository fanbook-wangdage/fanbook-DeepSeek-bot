import json
import logging
import coloredlogs
import requests
import re

# 创建日志记录器
logger = logging.getLogger(__name__)
# 配置 coloredlogs
coloredlogs.install(level='DEBUG', logger=logger)

def pm(ws, message:str, bot_token:str, bot_id:str):
    """处理消息
    Args:
        ws : ws对象
        message (str): ws收到的消息
        bot_token (str): bot token
        bot_id (str): bot id
    """
    message = json.loads(message)
    try:
        if message["action"] == "push":
            if message["data"]["author"]["bot"] == False:
                content = json.loads(message["data"]["content"])
                logger.info(f'收到消息: {content}')
                logger.info(f'纯文本内容: {content["text"]}')
                try:
                    # 提取并删除文本内容中的@ID
                    text = content["text"]
                    at_ids = re.findall(r'\${@!(\d+)}', text)
                    text = re.sub(r'\${@!\d+}', '', text)
                    
                    logger.info(f'提取的@ID: {at_ids}')
                    logger.info(f'处理后的文本内容: {text}')
                    if at_ids[0]==bot_id:
                        logger.info('是@机器人的消息')
                    else:
                        logger.info('不是@机器人的消息')
                except Exception as e:
                    logger.warning('消息中没有@任何人')
                
    except KeyError as e:
        try:
            if content['type'] == 'richText':
                logger.warning('不支持富文本消息')
            else:
                logger.warning(f'不支持解析的消息，原始消息: {message}')
        except Exception as e:
            logger.warning(f'不支持解析的消息，原始消息: {message}')
    except Exception as e:
        # 获取详细的错误信息
        import traceback
        logger.error(traceback.format_exc())