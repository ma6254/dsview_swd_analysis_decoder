import os
import shutil
import ctypes
import sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def main():
    try:
        # 定义目录路径
        source_dir = os.path.join(os.path.dirname(__file__), "src")
        target_dir = r"C:\Program Files\DSView\decoders\swd_analyzer"

        print("正在执行清理和部署操作...")

        # 删除旧目录
        if os.path.exists(target_dir):
            shutil.rmtree(target_dir, ignore_errors=True)
            print(f"➜ 已删除旧目录: {target_dir}")

        # 复制新目录
        shutil.copytree(source_dir, 
                      target_dir, 
                      copy_function=shutil.copy2,  # 保留文件元数据
                      dirs_exist_ok=True)          # 覆盖已存在文件

        print(f"✓ 已成功部署新版本到: {target_dir}")
        input("按回车键退出...")

    except Exception as e:
        print(f"❌ 发生错误: {str(e)}")
        input("按回车键退出...")
        sys.exit(1)

if __name__ == "__main__":
    if not is_admin():
        # 请求管理员权限（显示UAC弹窗）
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, __file__, None, 1)
        sys.exit()
    main()
