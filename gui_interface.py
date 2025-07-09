#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import threading
import webbrowser
from direct_html_generator import generate_html, MOMENTS_DIR, HTML_FILE

class MomentsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("朋友圈HTML生成器")
        self.root.geometry("920x750")
        self.root.resizable(True, True)
        self.root.minsize(800, 600)
        
        # 设置Mac风格样式
        self.setup_modern_style()
        
        # 设置Mac风格窗口背景
        self.root.configure(bg='#F2F2F7')
        
        # 尝试设置Mac原生外观
        try:
            self.root.tk.call('tk', 'scaling', 1.0)
        except:
            pass
        
        # 创建主框架
        self.create_widgets()
        
        # 初始化路径
        self.moments_dir = MOMENTS_DIR
        self.output_file = HTML_FILE
        
        # 更新界面显示
        self.update_display()
    
    def setup_modern_style(self):
        """设置Mac风格样式"""
        style = ttk.Style()
        
        # 使用现代主题
        style.theme_use('clam')
        
        # Mac系统配色方案
        colors = {
            'primary': '#007AFF',      # Mac蓝色
            'primary_hover': '#0051D5', # 深蓝色
            'secondary': '#34C759',    # Mac绿色
            'accent': '#FF9500',       # Mac橙色
            'background': '#F2F2F7',   # Mac背景色
            'surface': '#FFFFFF',      # 表面色
            'card': '#FFFFFF',         # 卡片背景
            'text_primary': '#000000', # 主要文本
            'text_secondary': '#8E8E93', # 次要文本
            'border': '#C6C6C8',       # 边框色
            'hover': '#E5F3FF',        # 悬停色
            'success': '#34C759',      # 成功色
            'warning': '#FF9500',      # 警告色
            'error': '#FF3B30',        # 错误色
            'separator': '#C6C6C8'     # 分隔线色
        }
        
        # Mac风格按钮样式
        style.configure('Modern.TButton',
                       background=colors['primary'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(20, 10),
                       font=('-apple-system', 13, 'normal'),
                       relief='flat')
        
        style.map('Modern.TButton',
                 background=[('active', colors['primary_hover']),
                           ('pressed', colors['primary_hover'])])
        
        # Mac风格成功按钮样式
        style.configure('Success.TButton',
                       background=colors['success'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(20, 10),
                       font=('-apple-system', 13, 'normal'),
                       relief='flat')
        
        # Mac风格警告按钮样式
        style.configure('Warning.TButton',
                       background=colors['warning'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(20, 10),
                       font=('-apple-system', 13, 'normal'),
                       relief='flat')
        
        # Mac风格输入框样式
        style.configure('Modern.TEntry',
                       fieldbackground=colors['surface'],
                       borderwidth=1,
                       relief='solid',
                       bordercolor=colors['border'],
                       padding=(15, 10),
                       font=('-apple-system', 13))
        
        style.map('Modern.TEntry',
                 bordercolor=[('focus', colors['primary'])])
        
        # Mac风格标签样式
        style.configure('Title.TLabel',
                       background=colors['background'],
                       foreground=colors['text_primary'],
                       font=('-apple-system', 20, 'bold'))
        
        style.configure('Modern.TLabel',
                       background=colors['background'],
                       foreground=colors['text_primary'],
                       font=('-apple-system', 13))
        
        # 配置框架样式
        style.configure('Card.TFrame',
                       background=colors['surface'],
                       relief='flat',
                       borderwidth=1,
                       bordercolor=colors['border'])
        
        # 配置进度条样式
        style.configure('Modern.Horizontal.TProgressbar',
                       background=colors['primary'],
                       troughcolor=colors['border'],
                       borderwidth=0,
                       lightcolor=colors['primary'],
                       darkcolor=colors['primary'])
        
        # Mac风格LabelFrame样式
        style.configure('Modern.TLabelframe',
                       background=colors['surface'],
                       relief='flat',
                       borderwidth=1,
                       bordercolor=colors['border'])
        
        style.configure('Modern.TLabelframe.Label',
                       background=colors['surface'],
                       foreground=colors['text_primary'],
                       font=('-apple-system', 15, 'medium'))
    
    def create_widgets(self):
        """创建界面组件"""
        # 创建Mac风格主框架
        main_frame = ttk.Frame(self.root, padding="30", style='Card.TFrame')
        main_frame.grid(row=0, column=0, sticky="nsew", padx=25, pady=25)
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Mac风格标题
        title_label = ttk.Label(main_frame, text="🌟 朋友圈HTML生成器", 
                               style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 30))
        
        # Mac风格路径配置区域
        path_frame = ttk.LabelFrame(main_frame, text="📁 路径配置", padding="25", style='Modern.TLabelframe')
        path_frame.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(0, 20))
        path_frame.columnconfigure(1, weight=1)
        
        # 朋友圈目录选择
        ttk.Label(path_frame, text="朋友圈目录:", style='Modern.TLabel').grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        self.dir_var = tk.StringVar()
        self.dir_entry = ttk.Entry(path_frame, textvariable=self.dir_var, width=50, style='Modern.TEntry')
        self.dir_entry.grid(row=0, column=1, sticky="ew", padx=(10, 10), pady=(0, 10))
        ttk.Button(path_frame, text="📂 浏览", command=self.browse_directory, style='Modern.TButton').grid(row=0, column=2, pady=(0, 10))
        
        # 输出文件选择
        ttk.Label(path_frame, text="输出文件:", style='Modern.TLabel').grid(row=1, column=0, sticky=tk.W)
        self.output_var = tk.StringVar()
        self.output_entry = ttk.Entry(path_frame, textvariable=self.output_var, width=50, style='Modern.TEntry')
        self.output_entry.grid(row=1, column=1, sticky="ew", padx=(10, 10))
        ttk.Button(path_frame, text="💾 选择", command=self.browse_output_file, style='Modern.TButton').grid(row=1, column=2)
        
        # Mac风格操作按钮区域
        action_frame = ttk.LabelFrame(main_frame, text="🚀 操作中心", padding="25", style='Modern.TLabelframe')
        action_frame.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(0, 20))
        
        # 操作按钮网格布局
        self.scan_btn = ttk.Button(action_frame, text="🔍 扫描朋友圈", command=self.scan_moments, style='Modern.TButton')
        self.scan_btn.grid(row=0, column=0, padx=(0, 10), pady=(0, 10), sticky="ew")
        
        self.generate_btn = ttk.Button(action_frame, text="⚡ 生成HTML", command=self.generate_html_file, style='Success.TButton')
        self.generate_btn.grid(row=0, column=1, padx=(0, 10), pady=(0, 10), sticky="ew")
        
        self.preview_btn = ttk.Button(action_frame, text="👀 预览HTML", command=self.preview_html, style='Warning.TButton')
        self.preview_btn.grid(row=1, column=0, padx=(0, 10), sticky="ew")
        
        self.open_dir_btn = ttk.Button(action_frame, text="📁 打开目录", command=self.open_directory, style='Modern.TButton')
        self.open_dir_btn.grid(row=1, column=1, padx=(0, 10), sticky="ew")
        
        # 配置按钮列权重
        action_frame.columnconfigure(0, weight=1)
        action_frame.columnconfigure(1, weight=1)
        
        # Mac风格状态区域
        status_frame = ttk.Frame(main_frame, style='Card.TFrame', padding="20")
        status_frame.grid(row=3, column=0, columnspan=3, sticky="ew", pady=(0, 20))
        status_frame.columnconfigure(0, weight=1)
        
        # 状态标签
        self.status_var = tk.StringVar(value="🟢 就绪")
        self.status_label = ttk.Label(status_frame, textvariable=self.status_var, style='Modern.TLabel', font=('SF Pro Display', 11, 'bold'))
        self.status_label.grid(row=0, column=0, sticky="w", pady=(0, 10))
        
        # 进度条
        self.progress = ttk.Progressbar(status_frame, mode='indeterminate', style='Modern.Horizontal.TProgressbar')
        self.progress.grid(row=1, column=0, sticky="ew")
        
        # Mac风格信息显示区域
        info_frame = ttk.LabelFrame(main_frame, text="📊 运行日志", padding="20", style='Modern.TLabelframe')
        info_frame.grid(row=4, column=0, columnspan=3, sticky="nsew", pady=(0, 20))
        info_frame.columnconfigure(0, weight=1)
        info_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # Mac风格信息文本框
        self.info_text = scrolledtext.ScrolledText(info_frame, height=12, width=70, 
                                                  font=('Monaco', 11), 
                                                  bg='#FFFFFF', 
                                                  fg='#1D1D1F',
                                                  selectbackground='#007AFF',
                                                  selectforeground='white',
                                                  relief='solid',
                                                  borderwidth=1,
                                                  highlightthickness=0,
                                                  insertbackground='#1D1D1F')
        self.info_text.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Mac风格底部按钮框架
        bottom_frame = ttk.Frame(main_frame, style='Card.TFrame', padding="15")
        bottom_frame.grid(row=5, column=0, columnspan=3, sticky="ew", pady=(10, 0))
        
        ttk.Button(bottom_frame, text="🗑️ 清空日志", command=self.clear_log, style='Modern.TButton').pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(bottom_frame, text="ℹ️ 关于", command=self.show_about, style='Modern.TButton').pack(side=tk.RIGHT)
    
    def update_display(self):
        """更新界面显示"""
        self.dir_var.set(self.moments_dir)
        self.output_var.set(self.output_file)
    
    def browse_directory(self):
        """浏览选择朋友圈目录"""
        directory = filedialog.askdirectory(title="选择朋友圈目录", initialdir=self.moments_dir)
        if directory:
            self.moments_dir = directory
            self.dir_var.set(directory)
            self.log_message(f"📁 已选择朋友圈目录: {directory}")
    
    def browse_output_file(self):
        """浏览选择输出文件"""
        file_path = filedialog.asksaveasfilename(
            title="选择输出HTML文件",
            defaultextension=".html",
            filetypes=[("HTML文件", "*.html"), ("所有文件", "*.*")],
            initialdir=os.path.dirname(self.output_file)
        )
        if file_path:
            self.output_file = file_path
            self.output_var.set(file_path)
            self.log_message(f"💾 已选择输出文件: {file_path}")
    
    def scan_moments(self):
        """扫描朋友圈目录"""
        if not os.path.exists(self.moments_dir):
            messagebox.showerror("错误", "朋友圈目录不存在！")
            return
        
        self.log_message("开始扫描朋友圈目录...")
        
        try:
            folders = []
            for item in os.listdir(self.moments_dir):
                item_path = os.path.join(self.moments_dir, item)
                if os.path.isdir(item_path) and '_' in item:
                    folders.append(item)
            
            folders.sort(reverse=True)  # 按时间倒序
            
            self.log_message(f"📊 找到 {len(folders)} 个朋友圈文件夹:")
            for folder in folders[:10]:  # 只显示前10个
                self.log_message(f"  📁 {folder}")
            
            if len(folders) > 10:
                self.log_message(f"  📋 ... 还有 {len(folders) - 10} 个文件夹")
            
            if not folders:
                self.log_message("⚠️ 未找到有效的朋友圈文件夹")
                self.set_status("未找到朋友圈数据", "warning")
            
        except Exception as e:
            self.log_message(f"扫描出错: {str(e)}")
            messagebox.showerror("错误", f"扫描朋友圈目录时出错:\n{str(e)}")
    
    def generate_html_file(self):
        """生成HTML文件"""
        if not os.path.exists(self.moments_dir):
            messagebox.showerror("错误", "朋友圈目录不存在！")
            return
        
        # 在新线程中执行生成操作
        thread = threading.Thread(target=self._generate_html_thread)
        thread.daemon = True
        thread.start()
    
    def _generate_html_thread(self):
        """在线程中生成HTML"""
        try:
            self.root.after(0, lambda: self.set_status("正在生成HTML文件...", "loading"))
            self.root.after(0, lambda: self.progress.start())
            
            # 临时修改全局变量
            import direct_html_generator
            original_dir = direct_html_generator.MOMENTS_DIR
            original_file = direct_html_generator.HTML_FILE
            
            direct_html_generator.MOMENTS_DIR = self.moments_dir
            direct_html_generator.HTML_FILE = self.output_file
            
            # 生成HTML
            output_file = generate_html()
            
            # 恢复全局变量
            direct_html_generator.MOMENTS_DIR = original_dir
            direct_html_generator.HTML_FILE = original_file
            
            self.root.after(0, lambda: self.progress.stop())
            self.root.after(0, lambda: self.set_status("HTML文件生成完成", "success"))
            self.root.after(0, lambda: self.log_message(f"✅ HTML文件已生成: {output_file}"))
            self.root.after(0, lambda: messagebox.showinfo("🎉 生成成功", f"HTML文件已生成:\n{output_file}"))
            
        except Exception as e:
            self.root.after(0, lambda: self.progress.stop())
            self.root.after(0, lambda: self.set_status("生成失败", "error"))
            self.root.after(0, lambda: self.log_message(f"❌ 生成HTML文件时出错: {str(e)}"))
            self.root.after(0, lambda: messagebox.showerror("❌ 生成失败", f"生成HTML文件时出错:\n{str(e)}"))
    
    def preview_html(self):
        """预览HTML文件"""
        if not os.path.exists(self.output_file):
            messagebox.showwarning("警告", "HTML文件不存在，请先生成HTML文件！")
            return
        
        try:
            webbrowser.open(f"file://{os.path.abspath(self.output_file)}")
            self.log_message(f"🌐 已在浏览器中打开: {self.output_file}")
        except Exception as e:
            self.log_message(f"打开HTML文件时出错: {str(e)}")
            messagebox.showerror("错误", f"打开HTML文件时出错:\n{str(e)}")
    
    def open_directory(self):
        """打开朋友圈目录"""
        if not os.path.exists(self.moments_dir):
            messagebox.showerror("错误", "朋友圈目录不存在！")
            return
        
        try:
            if os.name == 'nt':  # Windows
                os.startfile(self.moments_dir)
            elif os.name == 'posix':  # macOS and Linux
                os.system(f'open "{self.moments_dir}"')
            self.log_message(f"📂 已打开目录: {self.moments_dir}")
        except Exception as e:
            self.log_message(f"打开目录时出错: {str(e)}")
            messagebox.showerror("错误", f"打开目录时出错:\n{str(e)}")
    
    def set_status(self, message, status_type="info"):
        """设置状态信息"""
        status_icons = {
            "info": "ℹ️",
            "success": "✅",
            "warning": "⚠️",
            "error": "❌",
            "loading": "⏳",
            "ready": "🟢"
        }
        
        icon = status_icons.get(status_type, "ℹ️")
        self.status_var.set(f"{icon} {message}")
    
    def log_message(self, message):
        """记录日志信息"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.info_text.insert(tk.END, log_entry)
        self.info_text.see(tk.END)
    
    def clear_log(self):
        """清空日志"""
        self.info_text.delete(1.0, tk.END)
        self.log_message("日志已清空")
    
    def show_about(self):
        """显示关于信息"""
        about_text = """
朋友圈HTML生成器 v1.0

功能说明:
• 扫描指定目录下的朋友圈数据
• 生成美观的HTML时间线页面
• 支持文本、图片、视频和链接内容
• 提供可视化操作界面

使用方法:
1. 选择朋友圈数据目录
2. 设置输出HTML文件路径
3. 点击"生成HTML"按钮
4. 使用"预览HTML"查看结果

作者: AI助手
"""
        messagebox.showinfo("关于", about_text)

def main():
    """主函数"""
    root = tk.Tk()
    app = MomentsGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()