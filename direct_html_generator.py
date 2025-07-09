#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import datetime
import html

# 朋友圈根目录
MOMENTS_DIR = '/Users/mac/Desktop/moments'
# 输出文件路径
HTML_FILE = os.path.join(MOMENTS_DIR, 'moments_timeline_direct.html')

def extract_datetime(folder_name):
    """从文件夹名称中提取日期时间信息"""
    match = re.search(r'_([0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{4})$', folder_name)
    if match:
        date_time_str = match.group(1)
        try:
            return datetime.datetime.strptime(date_time_str, '%Y-%m-%d-%H%M')
        except ValueError:
            return None
    return None

def get_user_name(folder_name):
    """从文件夹名称中提取用户名"""
    match = re.match(r'(.+)_[0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{4}$', folder_name)
    if match:
        username = match.group(1)
        # 去掉所有括号内容，只保留用户名
        clean_username = re.sub(r'\([^)]+\)', '', username)
        return clean_username.strip()
    return "未知用户"

def get_moment_content(folder_path):
    """获取朋友圈内容，包括文本、图片和链接"""
    content = {}
    
    # 获取文本内容
    text_file = os.path.join(folder_path, 'text.txt')
    if os.path.exists(text_file):
        try:
            with open(text_file, 'r', encoding='utf-8') as f:
                content['text'] = f.read().strip()
        except Exception as e:
            content['text'] = f"[读取文本出错: {str(e)}]"
    else:
        content['text'] = ""
    
    # 获取链接内容
    url_file = os.path.join(folder_path, 'url.txt')
    if os.path.exists(url_file):
        try:
            with open(url_file, 'r', encoding='utf-8') as f:
                content['url'] = f.read().strip()
        except Exception as e:
            content['url'] = ""
    else:
        content['url'] = ""
    
    # 获取图片列表
    content['images'] = []
    for file in os.listdir(folder_path):
        if file.startswith('img_') and (file.endswith('.jpg') or file.endswith('.png')):
            content['images'].append(os.path.join(folder_path, file))
    
    # 获取视频列表
    content['videos'] = []
    for file in os.listdir(folder_path):
        if file.endswith('.mp4') or file.endswith('.mov') or file.endswith('.avi'):
            content['videos'].append(os.path.join(folder_path, file))

    return content

def generate_html():
    """直接生成HTML文档"""
    moments = []
    
    # 遍历朋友圈文件夹
    for folder in os.listdir(MOMENTS_DIR):
        folder_path = os.path.join(MOMENTS_DIR, folder)
        
        if not os.path.isdir(folder_path) or not re.search(r'_[0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{4}$', folder):
            continue
        
        moment_datetime = extract_datetime(folder)
        if not moment_datetime:
            continue
        
        user_name = get_user_name(folder)
        content = get_moment_content(folder_path)
        
        moments.append({
            'datetime': moment_datetime,
            'user': user_name,
            'content': content,
            'folder': folder
        })
    
    # 按时间排序（从新到旧）
    moments.sort(key=lambda x: x['datetime'], reverse=True)
    
    # 获取用户名用于标题
    user_title = "朋友圈时间线"  # 默认标题
    if moments:
        user_title = f"{moments[0]['user']}朋友圈"
    
    # 生成HTML
    html_content = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(user_title)}</title>
    <style>
        body {{
            font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "WenQuanYi Micro Hei", sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f8f9fa;
        }}
        
        .container {{
            background-color: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        h1 {{
            color: #2c3e50;
            text-align: center;
            border-bottom: 3px solid #3498db;
            padding-bottom: 15px;
            margin-bottom: 30px;
        }}
        
        .moment {{
            margin-bottom: 30px;
            padding: 20px;
            border-left: 4px solid #27ae60;
            background-color: #f8f9fa;
            border-radius: 0 8px 8px 0;
        }}
        
        .moment-header {{
            margin-bottom: 15px;
        }}
        
        .moment-date {{
            font-size: 1.2em;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 5px;
        }}
        
        .moment-user {{
            color: #e74c3c;
            font-weight: bold;
        }}
        
        .moment-content {{
            margin: 15px 0;
            line-height: 1.8;
            white-space: pre-wrap;
        }}
        
        .moment-images {{
            margin-top: 15px;
        }}
        
        .moment-images img {{
            width: 180px;
            height: 180px;
            object-fit: cover;
            margin: 5px;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        
        .moment-videos {{
            margin-top: 15px;
        }}
        
        .moment-videos video {{
            width: 300px;
            height: auto;
            margin: 5px;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        
        .moment-link {{
            margin-top: 15px;
            padding: 12px;
            background-color: #e8f4fd;
            border: 1px solid #3498db;
            border-radius: 6px;
        }}
        
        .moment-link a {{
            color: #3498db;
            text-decoration: none;
            font-weight: 500;
            word-break: break-all;
        }}
        
        .moment-link a:hover {{
            color: #2980b9;
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{html.escape(user_title)}</h1>
"""
    
    # 添加每条朋友圈
    for moment in moments:
        date_time = moment['datetime']
        formatted_date = date_time.strftime('%Y年%m月%d日 %H:%M')
        
        html_content += f"""
        <div class="moment">
            <div class="moment-header">
                <div class="moment-date">{html.escape(formatted_date)}</div>
                <div class="moment-user">{html.escape(moment['user'])}</div>
            </div>
"""
        
        # 添加文本内容
        if moment['content']['text']:
            html_content += f'            <div class="moment-content">{html.escape(moment["content"]["text"])}</div>\n'
        
        # 添加图片
        if moment['content']['images']:
            html_content += '            <div class="moment-images">\n'
            for i, img_path in enumerate(moment['content']['images']):
                rel_path = os.path.relpath(img_path, MOMENTS_DIR)
                html_content += f'                <img src="{html.escape(rel_path)}" alt="图片{i+1}" title="图片{i+1}">\n'
            html_content += '            </div>\n'
        
        # 添加视频
        if moment['content']['videos']:
            html_content += '            <div class="moment-videos">\n'
            for i, video_path in enumerate(moment['content']['videos']):
                rel_path = os.path.relpath(video_path, MOMENTS_DIR)
                html_content += f'                <video controls>\n'
                html_content += f'                    <source src="{html.escape(rel_path)}" type="video/mp4">\n'
                html_content += f'                    您的浏览器不支持视频播放。\n'
                html_content += f'                </video>\n'
            html_content += '            </div>\n'
        
        # 添加链接
        if moment['content']['url']:
            html_content += f'            <div class="moment-link">\n'
            html_content += f'                <a href="{html.escape(moment["content"]["url"])}" target="_blank">{html.escape(moment["content"]["url"])}</a>\n'
            html_content += '            </div>\n'
        
        html_content += '        </div>\n'
    
    html_content += """
    </div>
</body>
</html>
"""
    
    # 写入HTML文件
    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"已生成HTML文件: {HTML_FILE}")
    return HTML_FILE



def main():
    """主函数"""
    generate_html()

if __name__ == "__main__":
    main()