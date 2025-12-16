import platform
import subprocess
import sys
from pathlib import Path
import shutil

class MemrayAnalyzer:
    """Memray 内存分析核心类（适配 1.10+ 版本）"""
    def __init__(self, target_script: str, output_dir: str = "deeptracer_mem_report"):
        # 基础配置
        self.target_script = Path(target_script).absolute()
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # 文件路径（.bin 为中间件，HTML 为最终产物）
        self.trace_bin = self.output_dir / "mem_trace.bin"
        self.html_report = self.output_dir / "mem_report.html"
        self.leak_report = self.output_dir / "leak_summary.txt"  # 泄漏详情文本
        
        # 系统适配
        self.os_type = platform.system()
        self.is_windows = self.os_type == "Windows"
        self.memray_cmd = shutil.which("memray")  # 检查 memray 是否在 PATH 中

        # 前置校验
        self._pre_check()

    def _pre_check(self):
        """前置校验：确保脚本存在 + Memray 安装正常"""
        # 校验目标脚本
        if not self.target_script.exists():
            raise FileNotFoundError(f"目标脚本不存在：{self.target_script}")
        if self.target_script.suffix != ".py":
            raise ValueError(f"仅支持 .py 脚本，当前文件：{self.target_script}")
        
        # 校验 Memray
        if not self.memray_cmd:
            raise RuntimeError(
                "未检测到 Memray，请执行：pip install memray>=1.10.0"
            )

    def _run_memray_trace(self):
        """执行内存追踪：运行 py 脚本，生成 .bin 中间件"""
        cmd = [
            self.memray_cmd, "run",
            "-o", str(self.trace_bin),       # 输出 bin 文件
            "--format", "bin",              # 固定为 bin 格式
            "--no-progress",                # 关闭进度条，避免干扰
        ]
        # Windows 适配：禁用 C 层追踪
        if self.is_windows:
            cmd.append("--no-native-traces")
        # 加入目标 py 脚本（核心：跑的是 py 文件）
        cmd.append(str(self.target_script))

        # 执行命令
        try:
            subprocess.run(
                cmd,
                shell=self.is_windows,      # Windows 需 shell=True
                capture_output=True,
                text=True,
                check=True,
                # Windows 隐藏命令行窗口
                creationflags=subprocess.CREATE_NO_WINDOW if self.is_windows else 0
            )
            print(f"✅ 已追踪 {self.target_script.name}，内存数据写入：{self.trace_bin}")
            return True
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f"追踪失败：{e.stderr[:200]}\n命令：{' '.join(cmd)}"
            )

    def _generate_html_report(self):
        """生成交互式 HTML 火焰图报告（最终产物）"""
        if not self.trace_bin.exists():
            raise FileNotFoundError("无追踪数据，请先执行内存追踪")

        cmd = [
            self.memray_cmd, "flamegraph",
            str(self.trace_bin),            # 读取 bin 文件
            "-o", str(self.html_report),    # 输出 HTML
            "--title", f"DeepTracer - {self.target_script.name} 内存分析"
        ]

        subprocess.run(
            cmd,
            shell=self.is_windows,
            capture_output=True,
            check=True,
            creationflags=subprocess.CREATE_NO_WINDOW if self.is_windows else 0
        )
        print(f"✅ HTML 报告生成完成：{self.html_report}")

    def _generate_leak_report(self):
        """生成泄漏详情文本报告（可选，辅助分析）"""
        cmd = [
            self.memray_cmd, "stats",
            "--leaks",                      # 仅显示泄漏数据
            str(self.trace_bin),
            "-o", str(self.leak_report)     # 输出文本
        ]
        subprocess.run(
            cmd,
            shell=self.is_windows,
            capture_output=True,
            check=True
        )
        print(f"✅ 泄漏详情生成完成：{self.leak_report}")

    def clean_temp_file(self):
        """清理 .bin 临时文件（可选，减少冗余）"""
        if self.trace_bin.exists():
            self.trace_bin.unlink()
            print(f"✅ 已清理临时文件：{self.trace_bin}")

    def run_full_analysis(self, clean_temp: bool = True):
        """
        全流程分析：追踪 → 生成 HTML → 生成泄漏报告 → 清理临时文件
        :param clean_temp: 是否清理 .bin 临时文件
        :return: 报告路径字典
        """
        try:
            # 1. 运行 py 脚本，追踪内存
            self._run_memray_trace()
            # 2. 生成 HTML 报告（核心产物）
            self._generate_html_report()
            # 3. 生成泄漏详情（可选）
            self._generate_leak_report()
            # 4. 清理临时文件
            if clean_temp:
                self.clean_temp_file()
            
            # 返回结果（仅暴露最终产物）
            return {
                "html_report": str(self.html_report),
                "leak_report": str(self.leak_report),
                "success": True
            }
        except Exception as e:
            return {
                "error": str(e),
                "success": False
            }
