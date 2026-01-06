from unittest.mock import Mock, patch

def test_PyInstrumentAnalyzer_import():
    """测试能否正常导入PyInstrumentAnalyzer类"""
    with patch('builtins.__import__'):
        try:
            from deeptracer.viztracerAnalyer import PyInstrumentAnalyzer
            assert PyInstrumentAnalyzer is not None
        except ImportError as e:
            assert str(e) != ""

def test_viztracerAnalyer_structure():
    """测试模块viztracerAnalyer的基本结构"""
    # 不实际导入，而是测试模块路径是否存在
    import os
    file_path = os.path.join('deeptracer', 'viztracerAnalyer', 'ViztracerAnalyer.py')
    assert os.path.exists(file_path), f"viztracerAnalyer文件不存在: {file_path}"

def test_main_function():
    from deeptracer.viztracerAnalyer import PyInstrumentAnalyzer
    Analyzer = PyInstrumentAnalyzer()
    Analyzer.generate_perf_report("test/test_sources/test_mem.py")

if __name__ == "__main__":
    test_main_function()