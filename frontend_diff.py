from deeptracer.server.app import start
from deeptracer.astAnalyer import AstAnalyer
from deeptracer.speedAnalyer import SpeedAnalyzer
# 生成原始代码
with open("codes.py","r", encoding="utf-8") as fp:
    original_code = fp.read()

# 生成修改后的代码
modified_code = """def calculate_sum(n):
    return sum(range(n+1))

def multiply(a, b):
    result = a * b
    return result

# 基础变量
a = 10
b = 20
c = a + b

# 新功能
print("Hello, World!")
print("Welcome to DeepTracer!")

# 新增的工具函数
def helper_function():
    return "This is a helper"

def another_helper():
    return "Another helper" """


initial_code = original_code  # 初始代码应该是原始代码
aster = AstAnalyer(pythonScript="codes.py")
# 生成 AST 和 Pyinstrument 的 HTML 数据（模拟）
ast_html = aster.visualize()
speeder = SpeedAnalyzer()

pyinstrument_html = speeder.generate_perf_report(py_file_path="codes.py")

workflow_data = {
    "py_file_code": initial_code,
    "original_code": original_code,
    "modified_code": modified_code,
    "modify_reason": "优化了 calculate_sum 函数使用内置 sum 函数；改进了 multiply 函数增加中间变量；更新了变量值；新增了欢迎信息和工具函数；删除了旧功能"
}

if __name__ == "__main__":
    start(
        astAnalyer_html=ast_html,
        speedAnalyer_html=pyinstrument_html,
        workflowJson=workflow_data,
        originCode=initial_code
    )
