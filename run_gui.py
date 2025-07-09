#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
朋友圈HTML生成器 - GUI启动脚本

这个脚本提供了一个简单的启动入口，用于运行朋友圈HTML生成器的图形界面。
"""

import sys
import os

# 确保当前目录在Python路径中
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    from gui_interface import main
    
    if __name__ == "__main__":
        print("启动朋友圈HTML生成器GUI界面...")
        main()
except ImportError as e:
    print(f"导入错误: {e}")
    print("请确保所有必要的文件都在当前目录中。")
    input("按回车键退出...")
except Exception as e:
    print(f"运行错误: {e}")
    input("按回车键退出...")