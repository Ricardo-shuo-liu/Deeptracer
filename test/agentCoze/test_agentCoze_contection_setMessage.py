from deeptracer.agentCoze import Agent

def _a_error():
    object = Agent('path1','path2','path3',"path4")
    #这里只负责占位置 没有真实存在 会报错
    msgs = object.setMessage()
    print(msgs)
def _a_successful():
    object = Agent("test_local/agentCoze/agent.txt",
                    "test_local/agentCoze/agent.txt",
                    "test_local/agentCoze/agent.txt",
                    "test_local/agentCoze/agent.txt")
    #这里真实存在 测试能不能正常连接
    msgs = object.setMessage()
    print(msgs)
if __name__ == "__main__":
    _a_successful()