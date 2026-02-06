import re

def convert_md_to_html(md_content):
    html_lines = []
    
    # CSS Styles (Inline for WeChat)
    style_container = 'max-width: 100%; margin: 0 auto; background-color: #ffffff; padding: 20px; box-sizing: border-box; font-family: "Courier New", Courier, monospace, sans-serif;'
    
    # 标题样式：黑色方块背景，白色文字，像素风硬阴影
    style_h1 = 'font-size: 22px; font-weight: 900; border: 3px solid #000; padding: 15px; margin-bottom: 30px; text-align: center; background-color: #fff; box-shadow: 6px 6px 0px #000; line-height: 1.4;'
    style_h2 = 'display: inline-block; background-color: #000; color: #fff; padding: 8px 12px; font-size: 18px; font-weight: bold; margin-top: 40px; margin-bottom: 20px; box-shadow: 4px 4px 0px #888; border: 2px solid #000;'
    style_h3 = 'font-size: 16px; font-weight: bold; border-left: 6px solid #000; padding-left: 10px; margin-top: 25px; margin-bottom: 15px; line-height: 1.5; background-color: #f0f0f0; padding-top: 5px; padding-bottom: 5px;'
    style_h4 = 'font-size: 15px; font-weight: bold; text-decoration: underline; text-decoration-thickness: 2px; text-underline-offset: 4px; margin-top: 20px; margin-bottom: 10px;'
    
    # 正文样式
    style_p = 'font-size: 15px; line-height: 1.8; color: #000; margin-bottom: 20px; text-align: justify; letter-spacing: 0.5px;'
    style_strong = 'background-color: #ddd; padding: 0 4px; border: 1px solid #000; font-weight: bold; margin: 0 2px;'
    
    # 列表样式
    style_ul = 'list-style-type: none; padding-left: 10px; margin-bottom: 20px;'
    style_li = 'margin-bottom: 12px; padding-left: 20px; position: relative; line-height: 1.6; font-size: 15px;'
    style_li_marker = 'position: absolute; left: 0; top: 6px; width: 8px; height: 8px; background-color: #000; border: 1px solid #000;' # 方块点
    
    # 表格样式
    style_table = 'width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 13px; border: 2px solid #000;'
    style_th = 'border: 1px solid #000; padding: 8px; background-color: #000; color: #fff; font-weight: bold; text-align: center;'
    style_td = 'border: 1px solid #000; padding: 8px; text-align: left; vertical-align: top;'
    
    # 引用/代码块样式
    style_quote = 'border: 2px solid #000; background-color: #f4f4f4; padding: 15px; margin: 20px 0; font-size: 14px; position: relative;'
    
    html_lines.append(f'<div style="{style_container}">')
    
    # 简单的状态机
    in_table = False
    table_header_processed = False
    
    lines = md_content.split('\n')
    
    for i, line in enumerate(lines):
        line = line.strip()
        
        # 处理粗体 **text** -> <span>...
        line = re.sub(r'\*\*(.*?)\*\*', f'<span style="{style_strong}">\\1</span>', line)
        
        # 处理表格
        if '|' in line and (line.startswith('|') or line.endswith('|')):
            if not in_table:
                html_lines.append(f'<table style="{style_table}">')
                in_table = True
                table_header_processed = False
            
            # 判断是否是分隔行 |---|
            if set(line.replace('|', '').replace('-', '').replace(' ', '')) == set():
                continue
                
            cols = [c.strip() for c in line.split('|') if c.strip() != '']
            
            html_lines.append('<tr>')
            for col in cols:
                if not table_header_processed:
                    html_lines.append(f'<th style="{style_th}">{col}</th>')
                else:
                    html_lines.append(f'<td style="{style_td}">{col}</td>')
            html_lines.append('</tr>')
            
            if not table_header_processed:
                table_header_processed = True
            continue
        else:
            if in_table:
                html_lines.append('</table>')
                in_table = False
        
        if not line:
            continue
            
        # 标题
        if line.startswith('# '):
            content = line[2:]
            html_lines.append(f'<h1 style="{style_h1}">{content}</h1>')
            # 添加一个像素风装饰线
            html_lines.append('<div style="height: 4px; background: repeating-linear-gradient(90deg, #000, #000 4px, #fff 4px, #fff 8px); margin-bottom: 30px;"></div>')
            
        elif line.startswith('## '):
            content = line[3:]
            html_lines.append(f'<h2 style="{style_h2}">{content}</h2>')
        elif line.startswith('### '):
            content = line[4:]
            html_lines.append(f'<h3 style="{style_h3}">{content}</h3>')
        elif line.startswith('#### '):
            content = line[5:]
            html_lines.append(f'<h4 style="{style_h4}">{content}</h4>')
            
        # 列表
        elif line.startswith('- ') or (line[0].isdigit() and line[1] == '.' and line[2] == ' '):
            # 简单处理：如果是列表项，我们手动包装成带自定义marker的div，避免ul/li在不同编辑器里的默认样式干扰
            content = line[2:] if line.startswith('- ') else line[line.find(' ')+1:]
            # 检查是否有数字前缀
            marker_text = "■" if line.startswith('- ') else line.split(' ')[0]
            
            # 使用flex布局模拟列表，更稳定
            html_lines.append(f'<div style="display: flex; margin-bottom: 10px;">')
            html_lines.append(f'<div style="flex-shrink: 0; width: 24px; font-weight: bold;">{marker_text}</div>')
            html_lines.append(f'<div style="{style_p} margin-bottom: 0;">{content}</div>')
            html_lines.append(f'</div>')
            
        # 引用 (>)
        elif line.startswith('> '):
            content = line[2:]
            html_lines.append(f'<div style="{style_quote}">{content}</div>')
            
        # 普通段落
        else:
            html_lines.append(f'<p style="{style_p}">{line}</p>')
            
    html_lines.append('</div>')
    
    # 底部添加个结束符
    html_lines.append('<div style="text-align: center; margin-top: 40px; letter-spacing: 4px;">*** END ***</div>')
    
    return '\n'.join(html_lines)

# Read file
files_path = r"c:\Users\wb.qiujunjie02\Desktop\skills\一文读懂Agent、MCP、Skill：2026年AI自动化核心三剑客_去AI味版-c7b1f656a3.md"
with open(files_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Generate HTML
html_content = convert_md_to_html(content)

# Write to output file
output_path = r"c:\Users\wb.qiujunjie02\Desktop\skills\pixel_style_post.html"
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"HTML generated at {output_path}")
print(html_content[:500]) # Preview
