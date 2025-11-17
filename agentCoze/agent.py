from cozepy import Coze, TokenAuth, COZE_CN_BASE_URL,Message
import os
from dotenv import load_dotenv


class Agent():
    """
    建立智能体对象,实现支持连接到远端API的功能管理
    
    Args:
        jsonPath(str) : viztracer逻辑生成的活动文件的路径
        svgPath(str) : py-sqy逻辑生成的活动文件的路径
        pyPath(str) : 检测源文件的路径地址
    Attributes:
        None
    
    Methods:
        None
    
    """
    def __init__(self,jsonPath:str,svgPath:str,pyPath:str)->None:
        """
        初始化函数,实现对象的基本参数逻辑的定义

        Args:
           jsonPath(str) : viztracer逻辑生成的活动文件的路径
            svgPath(str) : py-sqy逻辑生成的活动文件的路径
            pyPath(str) : 检测源文件的路径地址 
        
        Returns:
            None
        """
        self.jsonPath = jsonPath
        self.svgPath  = svgPath
        self.pyPath = pyPath
    
    def contection(self,configPath:str = "agentCoze/.env.local")->str:
        """
        连接逻辑，实现与

        Args:
            configPath(str):cozeAPI配置文件地址
        
        Returns:
            None
        """
        load_dotenv(configPath)
        #配置环境变量
        coze_api_token = os.getenv("COZE_API_TOKEN")
        self.bot_id =os.getenv("COZE_BOT_ID")
        self.user_id = os.getenv("COZE_USER_ID")
        #从环境变量中获得基本参数信息

        self.cozeObject = Coze(auth=TokenAuth(coze_api_token), base_url=COZE_CN_BASE_URL)

    
    def setMessage(self)->str:
        """
        智能体的交流

        Args:
            None
        
        Return :
            msgs(str):返回修改后的完成代码以及其相对解释
        """
        chat_poll = self.cozeObject.chat.create_and_poll(
            bot_id=self.bot_id,
            user_id=self.user_id,
            additional_messages=[
                Message.build_user_question_text(
                    "请分析以下文本\n\n"
                )
            ]
        )
        msgs = getattr(chat_poll, "messages", [])

        return self.messageDraw(msgs)
    def messageDraw(self,msgs:list)->str:
        """
        将从环境变量中获得的Message列表转化为python字符串
        
        Args:
            msgs(list):API返回的Message在环境中提取的参数值

        Returns:
            message(str):拼接完毕后的数据信息
        """
        message_texts = []
        for msg in msgs:
            message_texts.append(msg.content)
        
        messgae = "\n".join(message_texts)
        return messgae
        #拼接信息

