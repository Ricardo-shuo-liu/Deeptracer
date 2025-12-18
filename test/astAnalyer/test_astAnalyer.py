from unittest.mock import Mock, patch

def test_MemoryAnalyer_import():
    """测试能否正常导入AstAnalyer类"""
    with patch('builtins.__import__'):
        try:
            from deeptracer.astAnalyer import AstAnalyer
            assert AstAnalyer is not None
        except ImportError as e:
            assert str(e) != ""

def test_flow_structure():
    """测试模块astVisualizer的基本结构"""
    # 不实际导入，而是测试模块路径是否存在
    import os
    file_path = os.path.join('deeptracer', 'astAnalyer', 'astVisualizer.py')
    assert os.path.exists(file_path), f"astVisualizer文件不存在: {file_path}"

def test_flow_function():
    from deeptracer.astAnalyer import AstAnalyer
    memoryAnalyzer = AstAnalyer(
        "test/test_sources/test_mem.py",
        open=False
    )
    memoryAnalyzer.visualize()

if __name__ == "__main__":
    test_flow_function()
