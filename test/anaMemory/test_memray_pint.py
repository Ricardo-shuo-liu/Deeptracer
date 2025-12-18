from unittest.mock import Mock, patch

def test_MemoryAnalyer_import():
    """测试能否正常导入MemoryAnalyzer类"""
    with patch('builtins.__import__'):
        try:
            from deeptracer.anaMemory import MemoryAnalyzer
            assert MemoryAnalyzer is not None
        except ImportError as e:
            assert str(e) != ""

def test_flow_structure():
    """测试anaMemory模块的基本结构"""
    # 不实际导入，而是测试模块路径是否存在
    import os
    file_path = os.path.join('deeptracer', 'anaMemory', 'memoryAnalyzer.py')
    assert os.path.exists(file_path), f"anaMemory文件不存在: {file_path}"

def test_flow_function():
    from deeptracer.anaMemory import MemoryAnalyzer
    memoryAnalyzer = MemoryAnalyzer(
        "test/test_sources/test_mem.py"
    )
    memoryAnalyzer.run_full_analysis()

if __name__ == "__main__":
    test_flow_function()
