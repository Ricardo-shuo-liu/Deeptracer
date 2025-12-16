# test_mem.py
import time

def create_large_list():
    # 分配大列表（占用内存）
    large_data = [i for i in range(10_000_000)]  # 约 80MB 内存
    return large_data

def leak_memory():
    # 模拟内存泄漏：全局变量持有对象，不释放
    global leaked_data
    leaked_data = []
    for i in range(5_000_000):
        leaked_data.append({"key": i, "value": str(i)})  # 约 400MB 内存

def main():
    print("开始运行测试脚本...")
    # 正常分配 + 释放
    normal_data = create_large_list()
    del normal_data  # 释放内存
    time.sleep(1)
    
    # 模拟泄漏
    leak_memory()
    time.sleep(2)
    print("脚本运行完成（内存泄漏未释放）")

if __name__ == "__main__":
    main()
