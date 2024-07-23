import os
import sys
import ctypes
import subprocess

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_program(path):
    exit_code = 0
    try:
        result = subprocess.run([path], check=True, capture_output=True, text=True)
        exit_code = result.returncode
        print(f"Exit code: {exit_code}")
        print(f"Output: {result.stdout}")
        print(f"Errors: {result.stderr}")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    return exit_code

def run(program_path):

    if is_admin():
        # 管理员权限下执行代码
        return run_program(program_path)
    else:
        # 提升为管理员权限
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
