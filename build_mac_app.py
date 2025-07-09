#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
朋友圈HTML生成器 - Mac应用打包脚本

这个脚本使用PyInstaller将Python应用打包成Mac可执行文件
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_pyinstaller():
    """检查PyInstaller是否已安装"""
    try:
        import PyInstaller
        print(f"✅ PyInstaller已安装，版本: {PyInstaller.__version__}")
        return True
    except ImportError:
        print("❌ PyInstaller未安装")
        return False

def install_pyinstaller():
    """安装PyInstaller"""
    print("正在安装PyInstaller...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ PyInstaller安装成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ PyInstaller安装失败: {e}")
        return False

def create_spec_file():
    """创建PyInstaller规格文件"""
    spec_content = '''
# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['run_gui.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='朋友圈HTML生成器',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)

app = BUNDLE(
    exe,
    name='朋友圈HTML生成器.app',
    icon=None,
    bundle_identifier='com.moments.htmlgenerator',
    info_plist={
        'CFBundleName': '朋友圈HTML生成器',
        'CFBundleDisplayName': '朋友圈HTML生成器',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHighResolutionCapable': True,
        'LSMinimumSystemVersion': '10.13.0',
    },
)
'''
    
    with open('moments_app.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    print("✅ 已创建PyInstaller规格文件: moments_app.spec")

def build_app():
    """构建Mac应用"""
    print("开始构建Mac应用...")
    try:
        # 使用spec文件构建
        cmd = [sys.executable, "-m", "PyInstaller", "moments_app.spec", "--clean"]
        subprocess.check_call(cmd)
        print("✅ Mac应用构建成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 构建失败: {e}")
        return False

def create_dmg():
    """创建DMG安装包（可选）"""
    app_path = "dist/朋友圈HTML生成器.app"
    dmg_path = "dist/朋友圈HTML生成器.dmg"
    
    if not os.path.exists(app_path):
        print("❌ 找不到应用文件，无法创建DMG")
        return False
    
    try:
        # 删除已存在的DMG文件
        if os.path.exists(dmg_path):
            os.remove(dmg_path)
        
        # 创建DMG
        cmd = [
            "hdiutil", "create", "-volname", "朋友圈HTML生成器",
            "-srcfolder", app_path, "-ov", "-format", "UDZO", dmg_path
        ]
        subprocess.check_call(cmd)
        print(f"✅ DMG安装包创建成功: {dmg_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"⚠️ DMG创建失败: {e}")
        print("应用文件仍然可用，只是没有DMG安装包")
        return False
    except FileNotFoundError:
        print("⚠️ hdiutil命令未找到，无法创建DMG安装包")
        print("应用文件仍然可用，只是没有DMG安装包")
        return False

def cleanup():
    """清理临时文件"""
    print("清理临时文件...")
    dirs_to_remove = ['build', '__pycache__']
    files_to_remove = ['moments_app.spec']
    
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"✅ 已删除目录: {dir_name}")
    
    for file_name in files_to_remove:
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"✅ 已删除文件: {file_name}")

def main():
    """主函数"""
    print("🚀 朋友圈HTML生成器 - Mac应用打包工具")
    print("=" * 50)
    
    # 检查当前目录
    if not os.path.exists('run_gui.py'):
        print("❌ 错误: 请在包含run_gui.py的目录中运行此脚本")
        return False
    
    # 检查并安装PyInstaller
    if not check_pyinstaller():
        if not install_pyinstaller():
            return False
    
    # 创建规格文件
    create_spec_file()
    
    # 构建应用
    if not build_app():
        return False
    
    # 创建DMG（可选）
    create_dmg()
    
    # 清理临时文件
    cleanup()
    
    print("\n🎉 打包完成！")
    print("=" * 50)
    
    app_path = "dist/朋友圈HTML生成器.app"
    if os.path.exists(app_path):
        print(f"✅ Mac应用位置: {os.path.abspath(app_path)}")
        print("\n使用方法:")
        print("1. 双击应用图标启动")
        print("2. 或者在终端中运行: open 'dist/朋友圈HTML生成器.app'")
        
        dmg_path = "dist/朋友圈HTML生成器.dmg"
        if os.path.exists(dmg_path):
            print(f"✅ DMG安装包: {os.path.abspath(dmg_path)}")
            print("3. 或者双击DMG文件进行安装")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)