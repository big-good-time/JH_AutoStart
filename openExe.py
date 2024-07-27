import subprocess
import sys
import os
import time

def process_path(path):
    # 规范化路径
    return os.path.normpath(path)

def start_process(path):
    try:
        # 启动子进程
        proc = subprocess.Popen(path, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"Process launched with PID: {proc.pid}")
        return proc
    except Exception as e:
        print(f"Failed to start process: {e}")
        return None

def check_process(proc, timeout=5):
    start_time = time.time()
    while True:
        # 检查进程是否已经完成
        retcode = proc.poll()
        if retcode is not None:
            # 进程已经完成
            stdout, stderr = proc.communicate()
            # print("Process completed.")
            # print("Standard Output:")
            # print(stdout)
            # print("Standard Error:")
            # print(stderr)
            if stderr:
                print(f'openEXE: 执行命令失败: {stderr}')
                return False
            return retcode
        elif time.time() - start_time > timeout:
            # 超时
            print("Process is still running.")
            # 不结束进程，只是通知超时
            return True
        else:
            # 继续等待
            time.sleep(1)

def run(input_path):
    processed_path = process_path(input_path)

    proc = start_process(processed_path)
    if proc:
        retcode = check_process(proc)
        if retcode:
            return True
        else:
            return False
