import subprocess
from deeptracer import (
    DEEPTRACER_DEV_ROOT,
    print_color
    )
import os
from pathlib import Path
import platform
import shutil

class  MemoryAnalyzer:
    """
    memray内存分析入口
    
    """
    def __init__(self,
                 input_path:str,
                 output_dir:str="deeptracer/tools_report"
                 )->None:    
        """
        内存分析器初始化函数
    
        Args:
            input_path(str):输入文件路径
            output_fir(str):存储报告路径
        
        Returns:
            None
        """
        
        root = Path(DEEPTRACER_DEV_ROOT)
        self.target_script = Path(input_path).absolute()
        self.output_dir = root / output_dir
        #存储到目标文件夹下
        self.trace_bin = self.output_dir / "mem_trace.bin"
        self.html_report = self.output_dir / "mem_report.html"

        self.os_type = platform.system()
        #获得操作系统的版本
        self.memray_cmd = shutil.which('memray')
        #检测memray是不是在系统变量中

        self._pre_check()
    def _pre_check(self):
        """
        检验函数确保配置信息正常

        Args:
            None
        Returns:
            None
        """ 
        
        if not self.target_script.exists():
            raise FileNotFoundError(f"目标脚本不存在：{self.target_script}")
        #检测目标文件是不是存在
        if self.target_script.suffix != ".py":
            raise ValueError(f"仅支持 .py 脚本，当前文件：{self.target_script}")
        #检测目标文件是不是python文件
        if not self.memray_cmd:
            raise RuntimeError(
                "未检测到 Memray,请执行:pip install memray>=1.10.0"
            )
        #检测memray是不是正常安装
    def _run_memray_tracer(self):
        """
        运行memray命令拼接以及调用
        
        Args:
            None
        Returns:
            None
        """
        cmd = [
            self.memray_cmd,
            "run",
            "-o",
            str(self.trace_bin),
        ]
        #建立命令组建
        
        if self.os_type == "Windows":
            cmd.append("--no-native-traces")
            #如果是windows系统禁用c追踪
        cmd.append(str(self.target_script))
        try:
            subprocess.run(
                cmd,
                shell=(self.os_type == "Windows"), 
                capture_output=True,
                text=True,
                check=True,
                # Windows 隐藏命令行窗口
                creationflags=subprocess.CREATE_NO_WINDOW if ((self.os_type == "Windows")) else 0
            )
        
            """
            params:shell 决定是不是通过shell.exe来执行
                Windows 下 Memray 的可执行文件(memray.exe)依赖 cmd.exe 解析执行上下文
                类 Unix 下 memray 是可直接执行的二进制文件(/usr/bin/memray),无需 shell 中转
            Arritubs:
                shell=True 会先启动 cmd.exe,由 cmd 解析并调用 memray.exe,参数解析更稳定(这是 Windows 下调用命令行工具的通用适配方案)
                (类unix)shell=True 会多启动一个 /bin/sh 进程，虽然开销小,但高频调用时会累积;shell=False 直接调用 memray 二进制文件，少一层中转，效率更高
            
            params:capture_output
                错时能通过 e.stderr 获取 Memray 的错误信息，方便定位问题
            params:text
                底层逻辑:默认情况下,subprocess 捕获的输出是 bytes 类型(如 b"追踪成功"),text=True 会自动用 utf-8 解码为字符串("追踪成功")
            params:check
                Memray 执行出错(如 memray run 传错参数、目标脚本权限不足)时，不会 “假装成功”，而是触发 except CalledProcessError,返回包含错误信息的字典
            params:creationflags
                subprocess.CREATE_NO_WINDOW:Windows 下用 subprocess 执行命令时，默认会弹出一个黑色的 cmd 窗口，这个参数能隐藏它
                类 Unix 系统(Linux/macOS)没有 “命令行窗口” 的概念，因此设为 0 即可(无任何效果)

            """
            print_color(f"已追踪 {self.target_script.name}的内存信息",
                        fore_color="green")
        except Exception as e:
            raise RuntimeError(
                f"追踪失败"
            )
    def _generate_html_report(self):
        """
        运行memray生成html文件实现可视化
        
        Args:
            None
        Returns:
            None
        """
        if not self.trace_bin.exists():
            raise FileNotFoundError("无追踪数据，请先执行内存追踪")
        #检验是不是已经分析产生分析文件
        cmd = [
            self.memray_cmd,
            "flamegraph",
            str(self.trace_bin),#指定读取bin文件路径
            "-o",
            str(self.html_report),# 指定输出HTML路径
        ]
        #拼接命令
        if self.html_report.exists():
            self.html_report.unlink()
        subprocess.run(
                cmd,
                shell=(self.os_type == "Windows"), 
                capture_output=True,
                text=True,
                check=True,
                # Windows 隐藏命令行窗口
                creationflags=subprocess.CREATE_NO_WINDOW if ((self.os_type == "Windows")) else 0
            )
        #运行
        print_color("HTML 报告生成完成",
                    fore_color="green")
    def _clean_temp_file(self):
        """
        清除中间文件
        
        Args:
            None
        Returns:
            None
        """
        if self.trace_bin.exists():
            self.trace_bin.unlink()
            print_color(f"已清理临时文件",
                        fore_color="green")
    def run_full_analysis(self, 
                          clean_temp: bool = True):
        try:
            # 1. 运行 py 脚本，追踪内存
            self._run_memray_tracer()
            # 2. 生成 HTML 报告（核心产物）
            self._generate_html_report()
            # 3. 清理临时文件
            if clean_temp:
                self._clean_temp_file()
            
            # 返回结果（仅暴露最终产物）
            return {
                "html_report": str(self.html_report),
                "success": True
            }
        except Exception as e:
            print(e)
            return {
                "error": str(e),
                "success": False
            }
