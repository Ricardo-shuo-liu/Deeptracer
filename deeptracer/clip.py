import argparse
from pathlib import Path
import sys
from server import test
# server 中需要实现fastapi的核心功能 目前test只作为占位


def main()->None:
    """
    deeptracer的api命令行接口实现代码检测的调度    
    Args:
        None
    Returns:
        None
    Examples:
        # 在包含deeptracer包的环境下实现
        >>> deeptracer text.py
        # 检验相对路径为text.py的python文件 AST语法树可视化方案为base
        >>> deeptracer text.py --all
        # 检验相对路径为text.py的python文件 AST语法树可视化方案为all
    """


    argparser = argparse.ArgumentParser(
        prog="DeepTracer",
        description="deeptracer agent tools for your python learning!",
        epilog="Version 1.0.0"
    )
    argparser.add_argument("pypath",
                           help="target python file path")
    argparser.add_argument("-a","--all",
                           action="store_true",
                           dest="full_ast",
                           help="Enable full AST syntax tree visualization. Note: May cause browser crash for large Python files!")
    args = argparser.parse_args()

    def _checkPath(path:str,
                   _checkType:list=['.py',])->str:
        """
        检验指定路径是否存在以及合法
        
        Args:
            path(str): 捕获的python路径
            _checkType(list): 检验的类别种类 方便后面维护
        Returns:
            path(str): 检验完毕的python路径
        """
        pather = Path(path).resolve()
        if not pather.exists():
            raise FileNotFoundError(f"python file not found: {path}")
        if pather.suffix.lower() not in _checkType:
            raise ValueError(f"Invalid file type (only .py files are supported){path}")
        return path
    
    try:
        pypath = _checkPath(path=args.pypath)
        if args.full_ast:
            # TODO:调用主功能函数实现对AST语法树的完全显示
            pass
        else:
            # TODO: 调用主功能函数实现对AST语法树的默认显示
            pass
    except FileNotFoundError as e:
        argparser.error(f"File error: {str(e)}")
        sys.exit(1)
    except ValueError as e:
        argparser.error(f"Parameter error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        argparser.error(f"Conversion failed: {str(e)} (Please check file paths and dependencies)")
        sys.exit(1)
