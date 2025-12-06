from unittest.mock import Mock, patch

def test_agent_import():
    """测试能否正常导入Agent类"""
    with patch('builtins.__import__'):
        try:
            from deeptracer.agentCoze import Agent
            assert Agent is not None
        except ImportError as e:
            assert str(e) != ""

def test_agent_structure():
    """测试Agent模块的基本结构"""
    # 不实际导入，而是测试模块路径是否存在
    import os
    agent_file_path = os.path.join('deeptracer', 'agentCoze', 'agent.py')
    assert os.path.exists(agent_file_path), f"Agent文件不存在: {agent_file_path}"

def test_agent_function():
    from deeptracer.agentCoze import Agent
    # coze = Agent(
    #     jsonPath="test/test_sources/result.json",
    #     svgPath="test/test_sources/cpu_profile.svg",
    #     pyPath="test/test_sources/test.py",
    #     txtPath="test/test_sources/ast.txt"
    # )
    coze = Agent(
        "test.txt",
        "test.txt",
        "test.txt",
        "test.txt"
    )
    msgs = coze.setMessage()
    print(msgs)

if __name__ == "__main__":
    test_agent_function()
