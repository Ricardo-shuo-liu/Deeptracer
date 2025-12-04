import os

def get_deeptracer_root():
    """
    获取deeptracer库的绝对根路径

    Args:
        None
    Returns:
        deeptracer_root(str):绝对路径
    """
    # 1. 获取当前文件（__init__.py）的绝对路径
    current_file = os.path.abspath(__file__)
    # 2. 向上级目录找（__init__.py在deeptracer/下，所以dirname一次就是根）
    deeptracer_root = os.path.dirname(current_file)
    return deeptracer_root

# 定义全局的根路径常量（方便其他模块调用）
DEEPTRACER_ROOT = get_deeptracer_root()
DEEPTRACER_DEV_ROOT = os.path.dirname(DEEPTRACER_ROOT)
#print(DEEPTRACER_DEV_ROOT)
__all__ = [
    "get_deeptracer_root",
    "DEEPTRACER_ROOT",
    "DEEPTRACER_DEV_ROOT"
]