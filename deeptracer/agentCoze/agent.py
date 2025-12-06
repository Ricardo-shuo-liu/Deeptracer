from cozepy import (
    Coze,
    TokenAuth,
    COZE_CN_BASE_URL,
    Message,
    DeviceOAuthApp,
    MessageObjectString
    )
from deeptracer import DEEPTRACER_DEV_ROOT
import os
import sys
from pathlib import Path
from typing import Optional
import re
import time
from deeptracer import print_color
from dotenv import load_dotenv
import shutil
import tempfile
class get_env_messgae():
    """
    
    从环境变量中获取信息用于配置coze智能体

    Args:
        None
    Attributes:
        None
    
    Methods:
        None
    """


    def __init__(self)->None:
        pass
    @classmethod
    def get_coze_api_token(self,
                           workspace_id: Optional[str] = "7579550904685707316")->str:
        """
        获得用户在环境变量中存储的token信息
        如果不存在返回一个连接可以直接登录coze账号登录实现认证自动获取token

        Args:
            None
        Returns:
            coze_token(str): 用户的token
        """
        coze_token = os.getenv("COZE_API_TOKEN")
        if coze_token:
            return coze_token
        #增强代码鲁棒性
        coze_api_base = get_env_messgae.get_coze_api_base()
        device_oauth_app = DeviceOAuthApp(
                            client_id="57294420732781205987760324720643.app.coze", 
                            base_url=coze_api_base
                            )
        #初始化设备授权应用
        #client_id 是固定值
        #base_url 基础域名
        device_code = device_oauth_app.get_device_code(workspace_id)
        #调用设备授权实例的方法，获取设备授权码
        print_color(f"Please Open: {device_code.verification_url} to get the access token",
                    fore_color="red")
        #用户需要打开的验证 URL
        return device_oauth_app.get_access_token(
                                device_code=device_code.device_code, 
                                poll=True
                                ).access_token
        #get_access_token
        #调用设备授权实例的方法，获取最终的 access_token
        #device_code=device_code.device_code
        #传入第一步获取的设备码，告诉服务器 我是哪个设备在请求授权
        #poll=True 开启自动轮询
    @classmethod
    def get_coze_api_base(self):
        """
        获得用户在环境变量中存储的base信息
        如果不存在返回默认的国内的base地址

        Args:
            None
        Returns:
            coze_base_url(str):coze官网的url
        """
        coze_base = os.getenv("COZE_API_BASE")
        if coze_base:
            return coze_base
        return COZE_CN_BASE_URL
    @classmethod
    def get_coze_bot_id(self):
        """
        从环境变量中获得coze_bot_id

        Args:
            None
        Returns:
            coze_bot_id(str):coze的云端的bot_id

        """
        coze_bot_id = os.getenv("COZE_BOT_ID")
        assert coze_bot_id, "Waring!Can't find coze_bot_id from env! Please check and add it!"
        return coze_bot_id
    @classmethod
    def get_coze_user_id(self):
        """
        获得用户id 如果不存在要求用户按照指定规则
        """
        user_id = os.getenv("COZE_USER_ID")
        if user_id:
            return user_id
        else:
            flag = True
            #设置循环单元
            while(flag):            
                user_id = input("请输入用户id(只能以字母,数字和下划线构成):")
                flag = not get_env_messgae.judge_user_id(user_id)
                if flag:
                    print_color("输入错误!请在1s后重新试!",
                                fore_color="red",
                                bold=True)
                    time.sleep(1)
                    #设置等待
            print_color("输入成功!",
                        fore_color="green",
                        bold=True)
            return user_id
    @classmethod
    def judge_user_id(self,
                      user_id:str
                      )->bool:
        """
        判断user_id 输入是不是符合要求如果不符合那么持续要求用户输入直到成功

        Args:
            user_id(str): 用户输入的用户id
        Returns:
            result(bool): 如果符合返回True
        """
        Recompile = re.compile("[a-zA-Z0-9_]*")
        if re.match(Recompile,user_id).group():
            return True
        return False 
    
class _fileChange():
    """
    封装文件转换功能

    Args:
        None
    Attributes:
        None
    
    Methods:
        None
    """
    def __init__(self)->None:
        pass
    def _toTxt(self,
               filePath:str,
               savePath:str="deeptracer/agentCoze/activityFilesTXT"
               )->str:
        """
        实现文件copy成txt文件
        
        Args:
            filePath(str):文件路径
        Returns:
            txtPath(str):copy后文件路径
        """
        if not os.path.exists(os.path.join(DEEPTRACER_DEV_ROOT,savePath)):
            os.mkdir(os.path.join(DEEPTRACER_DEV_ROOT,savePath))
        #检验缓存空间是不是存在
        findally_path = self._change(filePath,
                                    savePath)
        return findally_path
    def _change(self,
                filePath,
                save_path:str)->str:
        """
        实现判别类型并且创建附件对象实现标注

        Args:
            type(str):文件类型
            name(str):文件名称(剔除后缀)
            save_path(str):保存的文件夹路径
        Returns:
            dst_path(str):附件路径
        """
        filePathType = Path(filePath).suffix
        
        filePathName = Path(filePath).stem
        if filePathType!=".py":
            src_path = os.path.join(DEEPTRACER_DEV_ROOT,filePath)
        else:
            src_path = filePath
        dst_path = os.path.join(DEEPTRACER_DEV_ROOT,
                                save_path,
                                filePathName + ".txt")
        match filePathType:
            case ".py":
                FORMAT_MARK = "#PYTHON"
                self._contentChange(src_path=src_path,
                                    dst_path=dst_path,
                                    FORMAT_MARK=FORMAT_MARK
                                    )
            case ".json":
                FORMAT_MARK = "#JSON"
                self._contentChange(src_path=src_path,
                                    dst_path=dst_path,
                                    FORMAT_MARK=FORMAT_MARK
                                    )
            case ".svg":
                FORMAT_MARK = "#XML"
                self._contentChange(src_path=src_path,
                                    dst_path=dst_path,
                                    FORMAT_MARK=FORMAT_MARK
                                    )
            case ".txt":
                FORMAT_MARK = "#TXT"
                self._contentChange(src_path=src_path,
                                    dst_path=dst_path,
                                    FORMAT_MARK=FORMAT_MARK
                                    )
            case _:
                raise "文件传入失败！"
            
        return dst_path
    def _contentChange(self,
                       src_path:str,
                       dst_path:str,
                       FORMAT_MARK:str="#TXT")->None:
        """
        实现对文件的标注
        
        Args:
            src_path(str):原文件路径
            dst_path(str):标注后txt文件路径
            FORMAT_MARK(str):标注信息
        Returns:
            None
        """
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", delete=False) as temp_f:
        # 写入首行标识
            temp_f.write(f"{FORMAT_MARK}\n")
            with open(src_path, "r", encoding="utf-8", newline="") as src_f:
                shutil.copyfileobj(src_f, temp_f)
        #拷贝内容

        shutil.move(temp_f.name, dst_path)
        #实现命名
class Agent():
    """
    建立智能体对象,实现支持连接到远端API的功能管理
    
    Args:
        jsonPath(str) : viztracer逻辑生成的活动文件的路径
        svgPath(str) : py-sqy逻辑生成的活动文件的路径
        pyPath(str) : 检测源文件的路径地址
        txtPath(str) : Ast树的存储文件位置
    Attributes:
        None
    
    Methods:
        None
    
    """
    def __init__(self,
                 jsonPath:str,
                 svgPath:str,
                 pyPath:str,
                 txtPath:str,
                 configPath:str = "deeptracer/agentCoze/.env.local",
                 cachePath:str = "deeptracer/agentCoze/activityFilesTXT"
                 )->None:
        """
        初始化函数,实现对象的基本参数逻辑的定义

        Args:
           jsonPath(str) : viztracer逻辑生成的活动文件的路径
            svgPath(str) : py-sqy逻辑生成的活动文件的路径
            pyPath(str) : 检测源文件的路径地址 
            txtPath(str) : Ast树的存储文件位置
        Returns:
            None
        """
        config_Path = os.path.join(DEEPTRACER_DEV_ROOT,configPath)
        load_dotenv(config_Path)#配置环境变量

        fileF = _fileChange()
        self.files_paths = {
            "json":fileF._toTxt(jsonPath,cachePath),
            "xml":fileF._toTxt(svgPath,cachePath),
            "python": fileF._toTxt(pyPath,cachePath),
            "txt":fileF._toTxt(txtPath,cachePath)
        }
        for pathtype,path in self.files_paths.items():
            print(path)
        self.cachePath = cachePath
        #配置基础文件路径 用于智能体读取
    def _validate_file(self):
        """
        检测传输的文件的路径是不是存在
        如果不存在会报错
        Args:
            None
        Returns:
            None
        
        """
        error_type = []
        for file_type,file_path in self.files_paths.items():
            if not os.path.exists(file_path):
                error_type.append(f"{file_type}类型的路径{file_path}")
        
        if not error_type:
            newline = '\n'
            raise FileNotFoundError(
                f"以下文件不存在：{newline}{newline.join(error_type)}"
                )
        
   
    def contection(self
                   )->Coze:
        """
        连接逻辑，实现与云端对象连接返回连接对象

        Args:
            None
        
        Returns:
            cozeobject(Coze): Coze对象用于操作
        """
        coze_api_token = get_env_messgae.get_coze_api_token()
        self.bot_id = get_env_messgae.get_coze_bot_id()
        self.user_id = get_env_messgae.get_coze_user_id()
        base_url = get_env_messgae.get_coze_api_base()
        #从环境变量中获得基本参数信息

        return Coze(auth=TokenAuth(coze_api_token),
                               base_url=base_url)
        #返回建立的coze对象 相当于登录coze
    def _get_content_type(self,
                          file_path:str)->str:
        """
        获得文件类型即获得txt,py等类型
        
        Args:
            file_path(str):文件路径
        Returns:
            file_type(str):文件类型
        """
        suffix = os.path.splitext(file_path)[1].lower()
        #切割路径获得后缀
        content_types = {
                        ".json": "application/json",
                        ".svg": "image/svg+xml",
                        ".py": "text/x-python",
                        ".txt": "text/plain",
                        ".md": "text/markdown"
                        }
        #建立映射表
        file_type = content_types.get(suffix,
                                      "application/octet-stream")
        #如果在映射表里面查找不到 就标定为数据流二进制形式直接报错
        return file_type
    def upload_file(self,
                    file_path:str,
                    cozeObj:Coze)->str:
        """
        上传一个文件给coze云端服务并返回对应的文件id
        
        Args:
            file_path(str):上传的文件路径

        Returns:
            file_id(str):上传文件的id
        """
        try:
            print_color(f"开始上传{file_path}文件","blue")  
            with open(file_path,"rb") as fb:
                uploadObj = cozeObj.files.upload(
                    file=fb
                )
                #上传文件实现逻辑
                return uploadObj.id
        except Exception as e:
            raise RuntimeError(f"文件 {file_path} 上传失败：{str(e)}")
    def upload_batch_file(self,
                          cozeObj:Coze)->list[str]:
        """
        批量上传所有文件
        Args:
            cozeObj(Coze):Coze对象
        Returns:
            ids(list):上传文件的id列表
        """
        ids = []
        for file_type,file_path in self.files_paths.items():
            id = self.upload_file(file_path,
                             cozeObj=cozeObj)
            ids.append(id)
            print_color(f"{file_type} 文件上传成功,ID:{id}", fore_color="green")
        return ids
    def setMessage(self,
                   prompt:str=None,
                   prompt_path:str="deeptracer/agentCoze/prompt/ default_prompt.txt",
                   )->str:
        """
        智能体的交流

        Args:
            None
        
        Return :
            msgs(str):返回修改后的完成代码以及其相对解释
        """
        
        cozeobject = self.contection()
        file_ids = self.upload_batch_file(cozeobject)
        MessageObjList = self._ids_to_Messgae(ids=file_ids)
        default_prompt_path = os.path.join(DEEPTRACER_DEV_ROOT,prompt_path)
        #得到coze对象实现一次调用函数直接发送信息
        with open(default_prompt_path,"r") as fb:
            default_prompt = fb.read()
        final_prompt = prompt if prompt else default_prompt
        
        user_message = Message.build_user_question_objects(
            [
                MessageObjectString.build_text(final_prompt),
            ] + MessageObjList
        )
        # 关联上传的文件 ID
        try:
            print_color("开始连接云端智能体请求分析",fore_color="blue")
            result = cozeobject.chat.create_and_poll(
                bot_id=self.bot_id,
                user_id=self.user_id,
                additional_messages=[user_message],
                poll_timeout=600
            )
            msgs = getattr(result,"messages",[])
            self._remove_cache(os.path.join(DEEPTRACER_DEV_ROOT,
                                            self.cachePath))
            #清理传递过程中产生的缓存文件
            return self.messageDraw(msgs)
        except Exception as e:
            raise RuntimeError(f"发送分析请求失败：{str(e)}")
        
    def _ids_to_Messgae(self,
                        ids:list[str])->list[MessageObjectString]:
        """
        将上传的文件的id列表转化为可使用对象
        
        Args:
            ids(list):上传文件的id列表
        Returns:
            MessageObjList(list):可使用对象列表
        """
        MessageObjList = []
        for id in ids:
            MessageObj = MessageObjectString.build_file(file_id=id)
            MessageObjList.append(MessageObj)
        return MessageObjList
    def _remove_cache(self,
                      cachePath:str)->None:
        """
        清理存放txt文件的文件夹

        Args:
            cachePath(str):存放地址
        Returns:
            None
        """
        print_color("开始清理缓存",fore_color="blue")
        if os.path.exists(cachePath):
            try:
                # 直接删除非空文件夹（核心函数）
                shutil.rmtree(cachePath)
                print_color(f"程序缓存清理成功"
                            ,fore_color="green")
            except Exception as e:
                print_color(f"程序缓存清理失败",
                            fore_color="red")
        else:
            print_color("状态良好无需清理!",
                        fore_color="green")
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
            if msg.role == "assistant":  # 只取智能体的回复
                message_texts.append(msg.content)
        
        messgae = "\n".join(message_texts)
        return messgae
        #拼接信息