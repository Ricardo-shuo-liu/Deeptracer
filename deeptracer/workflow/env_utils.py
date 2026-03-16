import pathlib

class build_env_local():
    def __init__(self):
        self.config_dir = pathlib.Path.home() / ".deeptracer"
        self.config_path = self.config_dir / ".env.local"
    def creator(self,key):
        self.config_dir.mkdir(exist_ok=True)
        content = []
        content.append("COZE_API_TOKEN="+key+"\n")
        #此处为了适配coze的逻辑 姑且写死 转为langchain后需要修改指定环境变量信息
        content.extend(
            ["COZE_BOT_ID=7583697542664814611\n",
            "COZE_WORKFLOW_ID=7582881054093230122\n",
            "COZE_API_BASE=https://api.coze.cn\n",
            "COZE_USER_ID=Deeptracer_main_application\n",
            "PORT=8000\n"]
        )
        print(self.config_path)
        with open(self.config_path, "w", encoding="utf-8") as f:
            f.writelines(content)
    def get_config_path(self):
        return self.config_path
    
