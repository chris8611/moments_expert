# 朋友圈HTML生成器 - Kivy版本

这是朋友圈HTML生成器的Kivy版本，支持跨平台运行，包括Windows、macOS、Linux和Android设备。

## 功能特点

- 🎯 **跨平台支持**: 支持桌面系统和Android设备
- 📱 **触屏友好**: 针对移动设备优化的界面
- 🎨 **现代化UI**: 使用Kivy框架的现代化界面设计
- 📁 **文件管理**: 可视化的文件和目录选择
- 🔄 **实时反馈**: 实时显示处理进度和日志
- 📊 **状态监控**: 清晰的状态指示和进度条

## 安装依赖

### 桌面环境安装

```bash
# 安装Kivy依赖
pip install -r requirements_kivy.txt
```

### Android打包环境安装

```bash
# 安装buildozer（用于Android打包）
pip install buildozer

# 在Linux/macOS上还需要安装额外依赖
# Ubuntu/Debian:
sudo apt update
sudo apt install -y git zip unzip openjdk-8-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

# macOS (需要安装Xcode命令行工具):
xcode-select --install
brew install autoconf automake libtool pkg-config
```

## 运行应用

### 桌面环境运行

```bash
# 方法1: 直接运行主文件
python main.py

# 方法2: 直接运行Kivy GUI
python kivy_gui.py
```

### 界面使用说明

1. **选择朋友圈目录**: 点击"选择目录"按钮，选择包含朋友圈数据的文件夹
2. **设置输出文件**: 点击"选择文件"按钮，设置HTML输出文件路径
3. **扫描朋友圈**: 点击"扫描朋友圈"按钮，预览将要处理的内容
4. **生成HTML**: 点击"生成HTML"按钮，开始生成HTML文件
5. **查看结果**: 生成完成后可以点击"打开目录"查看结果

## Android打包

### 1. 初始化buildozer

```bash
# 在项目目录下初始化buildozer配置
buildozer init
```

### 2. 编辑配置文件

编辑 `buildozer.spec` 文件（已提供默认配置）:

- `title`: 应用标题
- `package.name`: 包名
- `package.domain`: 域名
- `requirements`: Python依赖包
- `android.permissions`: Android权限

### 3. 构建APK

```bash
# 构建debug版本APK
buildozer android debug

# 构建release版本APK（需要签名）
buildozer android release
```

### 4. 安装到设备

```bash
# 安装debug版本到连接的Android设备
buildozer android deploy

# 运行并查看日志
buildozer android logcat
```

## 文件结构

```
moments/
├── main.py                 # Kivy版本主入口
├── kivy_gui.py            # Kivy GUI界面
├── direct_html_generator.py # HTML生成核心逻辑
├── requirements_kivy.txt   # Kivy依赖包
├── buildozer.spec         # Android打包配置
├── README_KIVY.md         # Kivy版本说明文档
└── bin/                   # 构建输出目录
    └── *.apk             # 生成的APK文件
```

## 注意事项

### Android权限

应用需要以下Android权限:
- `READ_EXTERNAL_STORAGE`: 读取外部存储
- `WRITE_EXTERNAL_STORAGE`: 写入外部存储
- `INTERNET`: 网络访问（如果需要）

### 文件路径

- **桌面环境**: 支持绝对路径和相对路径
- **Android环境**: 建议使用应用内部存储或外部存储的标准路径

### 性能优化

- 大量图片处理时可能需要较长时间
- Android设备上建议处理较小的数据集
- 可以通过进度条监控处理进度

## 故障排除

### 常见问题

1. **Kivy安装失败**
   ```bash
   # 尝试使用conda安装
   conda install kivy -c conda-forge
   ```

2. **Android构建失败**
   ```bash
   # 清理构建缓存
   buildozer android clean
   
   # 重新构建
   buildozer android debug
   ```

3. **权限问题**
   - 确保Android设备开启了"未知来源"安装
   - 检查应用权限设置

4. **文件路径问题**
   - Android上使用 `/sdcard/` 或应用专用目录
   - 避免使用包含中文的路径名

### 调试方法

```bash
# 查看详细构建日志
buildozer android debug -v

# 查看应用运行日志
buildozer android logcat

# 连接设备调试
adb logcat | grep python
```

## 技术支持

如果遇到问题，请检查:
1. Python版本 (推荐3.8+)
2. Kivy版本兼容性
3. Android SDK/NDK配置
4. 设备权限设置

---

**提示**: 首次构建Android APK可能需要下载大量依赖，请确保网络连接稳定。