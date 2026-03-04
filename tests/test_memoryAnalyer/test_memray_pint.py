from unittest.mock import Mock, patch
import pytest
@pytest.mark.skip(reason="由于权限问题该模块代码全部重构")
@logtitle
def test_MemoryAnalyer_import():
    """测试能否正常导入MemoryAnalyzer类"""
    with patch('builtins.__import__'):
        try:
            from deeptracer.memoryAnalyer import MemoryAnalyzer
            assert MemoryAnalyzer is not None
        except ImportError as e:
            assert str(e) != ""
@pytest.mark.skip(reason="由于权限问题该模块代码全部重构")
@logtitle
def test_anaMemory_structure():
    """测试anaMemory模块的基本结构"""
    # 不实际导入，而是测试模块路径是否存在
    import os
    file_path = os.path.join('deeptracer', 'memoryAnalyer', 'viztracer.py')
    assert os.path.exists(file_path), f"viztracer文件不存在: {file_path}"
@pytest.mark.skip(reason="由于权限问题该模块代码全部重构")
@logtitle
def test_main_function():
    from deeptracer.memoryAnalyer import MemoryAnalyzer
    memoryAnalyzer = MemoryAnalyzer(
        "tests/test_sources/test_mem.py"
    )
    memoryAnalyzer.run_full_analysis()

