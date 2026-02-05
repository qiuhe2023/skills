#!/usr/bin/env python3
"""
为微信公众号排版模板添加表格组件的脚本
"""

import os
import re
import sys

def get_table_for_template(template_name):
    """根据模板名称返回相应的表格组件"""

    # 极简时尚风格
    if template_name == "index.html":
        return '''    <!-- 组件：表格 -->
    <section style="margin: 30px 0;">
        <div style="font-size: 12px; color: #999; margin-bottom: 10px; letter-spacing: 1px;">组件：数据表格</div>

        <!-- 表格容器 -->
        <div style="border: 1px solid #ddd; overflow: hidden; border-radius: 2px;">

            <!-- 表头 -->
            <div style="display: flex; background-color: #f9f9f9; border-bottom: 1px solid #ddd;">
                <div style="flex: 1; padding: 12px 15px; font-size: 14px; font-weight: bold; color: #000; border-right: 1px solid #ddd;">项目名称</div>
                <div style="flex: 1; padding: 12px 15px; font-size: 14px; font-weight: bold; color: #000; border-right: 1px solid #ddd;">负责人</div>
                <div style="flex: 1; padding: 12px 15px; font-size: 14px; font-weight: bold; color: #000;">截止日期</div>
            </div>

            <!-- 表格行 -->
            <div style="display: flex; border-bottom: 1px solid #f0f0f0;">
                <div style="flex: 1; padding: 10px 15px; font-size: 14px; color: #333; border-right: 1px solid #f0f0f0;">季度报表分析</div>
                <div style="flex: 1; padding: 10px 15px; font-size: 14px; color: #333; border-right: 1px solid #f0f0f0;">张三</div>
                <div style="flex: 1; padding: 10px 15px; font-size: 14px; color: #333;">2026-03-31</div>
            </div>

            <!-- 表格行（交替背景） -->
            <div style="display: flex; border-bottom: 1px solid #f0f0f0; background-color: #fcfcfc;">
                <div style="flex: 1; padding: 10px 15px; font-size: 14px; color: #333; border-right: 1px solid #f0f0f0;">市场调研报告</div>
                <div style="flex: 1; padding: 10px 15px; font-size: 14px; color: #333; border-right: 1px solid #f0f0f0;">李四</div>
                <div style="flex: 1; padding: 10px 15px; font-size: 14px; color: #333;">2026-04-15</div>
            </div>

            <!-- 表格行 -->
            <div style="display: flex;">
                <div style="flex: 1; padding: 10px 15px; font-size: 14px; color: #333; border-right: 1px solid #f0f0f0;">产品上线计划</div>
                <div style="flex: 1; padding: 10px 15px; font-size: 14px; color: #333; border-right: 1px solid #f0f0f0;">王五</div>
                <div style="flex: 1; padding: 10px 15px; font-size: 14px; color: #333;">2026-05-20</div>
            </div>
        </div>

        <div style="font-size: 11px; color: #999; margin-top: 8px; text-align: right;">支持多列数据展示，适配移动端</div>
    </section>'''

    # 扁平风格
    elif template_name == "扁平风格.html":
        return '''    <!-- 组件：表格（扁平风格） -->
    <section style="margin: 30px 0;">
        <div style="font-size: 13px; color: #94a3b8; margin-bottom: 12px; font-weight: bold; letter-spacing: 0.5px;">组件：数据表格</div>

        <!-- 表格容器 -->
        <div style="border: 1px solid #e2e8f0; overflow: hidden; border-radius: 12px; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);">

            <!-- 表头 -->
            <div style="display: flex; background-color: #3b82f6; border-bottom: 1px solid #e2e8f0;">
                <div style="flex: 1; padding: 14px 16px; font-size: 14px; font-weight: bold; color: #ffffff; border-right: 1px solid rgba(255, 255, 255, 0.2);">技术指标</div>
                <div style="flex: 1; padding: 14px 16px; font-size: 14px; font-weight: bold; color: #ffffff; border-right: 1px solid rgba(255, 255, 255, 0.2);">当前状态</div>
                <div style="flex: 1; padding: 14px 16px; font-size: 14px; font-weight: bold; color: #ffffff;">优化目标</div>
            </div>

            <!-- 表格行 -->
            <div style="display: flex; border-bottom: 1px solid #f1f5f9;">
                <div style="flex: 1; padding: 12px 16px; font-size: 14px; color: #1e293b; border-right: 1px solid #f1f5f9; background-color: #ffffff;">响应时间</div>
                <div style="flex: 1; padding: 12px 16px; font-size: 14px; color: #10b981; font-weight: bold; border-right: 1px solid #f1f5f9; background-color: #ffffff;">≤1.2秒</div>
                <div style="flex: 1; padding: 12px 16px; font-size: 14px; color: #1e293b; background-color: #ffffff;">≤0.8秒</div>
            </div>

            <!-- 表格行（交替背景） -->
            <div style="display: flex; border-bottom: 1px solid #f1f5f9;">
                <div style="flex: 1; padding: 12px 16px; font-size: 14px; color: #1e293b; border-right: 1px solid #f1f5f9; background-color: #f8fafc;">错误率</div>
                <div style="flex: 1; padding: 12px 16px; font-size: 14px; color: #f97316; font-weight: bold; border-right: 1px solid #f1f5f9; background-color: #f8fafc;">0.8%</div>
                <div style="flex: 1; padding: 12px 16px; font-size: 14px; color: #1e293b; background-color: #f8fafc;">≤0.5%</div>
            </div>

            <!-- 表格行 -->
            <div style="display: flex;">
                <div style="flex: 1; padding: 12px 16px; font-size: 14px; color: #1e293b; border-right: 1px solid #f1f5f9; background-color: #ffffff;">并发处理</div>
                <div style="flex: 1; padding: 12px 16px; font-size: 14px; color: #10b981; font-weight: bold; border-right: 1px solid #f1f5f9; background-color: #ffffff;">500用户</div>
                <div style="flex: 1; padding: 12px 16px; font-size: 14px; color: #1e293b; background-color: #ffffff;">1000用户</div>
            </div>
        </div>

        <div style="font-size: 12px; color: #94a3b8; margin-top: 10px; text-align: right;">扁平化设计，视觉负担低，数据对比清晰</div>
    </section>'''

    # 科技简约像素
    elif template_name == "科技简约像素.html":
        return '''    <!-- 组件：表格 (科技数据表) -->
    <section style="margin-bottom: 30px;">
        <div style="font-size: 11px; color: #999; margin-bottom: 8px; letter-spacing: 1px; font-family: monospace;">COMPONENT: DATA_TABLE</div>

        <!-- 表格容器 -->
        <div style="border: 1px solid #000; padding: 1px;">

            <!-- 表头 -->
            <div style="display: flex; background-color: #000; border-bottom: 1px solid #000;">
                <div style="flex: 1; padding: 10px 12px; font-size: 12px; font-weight: bold; color: #fff; border-right: 1px solid #333; font-family: monospace;">PARAMETER</div>
                <div style="flex: 1; padding: 10px 12px; font-size: 12px; font-weight: bold; color: #fff; border-right: 1px solid #333; font-family: monospace;">VALUE</div>
                <div style="flex: 1; padding: 10px 12px; font-size: 12px; font-weight: bold; color: #fff; font-family: monospace;">STATUS</div>
            </div>

            <!-- 表格行 -->
            <div style="display: flex; border-bottom: 1px solid #eee;">
                <div style="flex: 1; padding: 10px 12px; font-size: 12px; color: #333; border-right: 1px solid #eee; font-family: monospace; background-color: #fff;">CPU_USAGE</div>
                <div style="flex: 1; padding: 10px 12px; font-size: 12px; color: #0066ff; font-weight: bold; border-right: 1px solid #eee; font-family: monospace; background-color: #fff;">42%</div>
                <div style="flex: 1; padding: 10px 12px; font-size: 12px; color: #00aa00; font-family: monospace; background-color: #fff;">
                    <span style="color: #00aa00;">●</span> NORMAL
                </div>
            </div>

            <!-- 表格行 -->
            <div style="display: flex; border-bottom: 1px solid #eee;">
                <div style="flex: 1; padding: 10px 12px; font-size: 12px; color: #333; border-right: 1px solid #eee; font-family: monospace; background-color: #f9f9f9;">MEMORY_ALLOC</div>
                <div style="flex: 1; padding: 10px 12px; font-size: 12px; color: #0066ff; font-weight: bold; border-right: 1px solid #eee; font-family: monospace; background-color: #f9f9f9;">1.8 GB</div>
                <div style="flex: 1; padding: 10px 12px; font-size: 12px; color: #ff9900; font-family: monospace; background-color: #f9f9f9;">
                    <span style="color: #ff9900;">●</span> WARNING
                </div>
            </div>

            <!-- 表格行 -->
            <div style="display: flex;">
                <div style="flex: 1; padding: 10px 12px; font-size: 12px; color: #333; border-right: 1px solid #eee; font-family: monospace; background-color: #fff;">NETWORK_LATENCY</div>
                <div style="flex: 1; padding: 10px 12px; font-size: 12px; color: #0066ff; font-weight: bold; border-right: 1px solid #eee; font-family: monospace; background-color: #fff;">24 ms</div>
                <div style="flex: 1; padding: 10px 12px; font-size: 12px; color: #00aa00; font-family: monospace; background-color: #fff;">
                    <span style="color: #00aa00;">●</span> OPTIMAL
                </div>
            </div>
        </div>

        <div style="font-size: 10px; color: #888; margin-top: 8px; text-align: right; font-family: monospace;">TABLE_REF: SYS_METRICS_2026</div>
    </section>'''

    # 像素风格
    elif template_name == "像素.html":
        return '''    <!-- 组件：表格（像素风格） -->
    <section style="margin: 30px 0;">
        <div style="font-size: 14px; color: #666; margin-bottom: 15px; font-weight: bold; letter-spacing: 1px; border-bottom: 4px dashed #000; padding-bottom: 5px;">组件：像素数据表格</div>

        <!-- 表格容器 -->
        <div style="border: 4px solid #000; padding: 2px; background-color: #fff; box-shadow: 6px 6px 0px #000;">

            <!-- 表头 -->
            <div style="display: flex; background-color: #ffcc00; border-bottom: 4px solid #000;">
                <div style="flex: 1; padding: 12px 15px; font-size: 16px; font-weight: bold; color: #000; border-right: 4px solid #000;">游戏道具</div>
                <div style="flex: 1; padding: 12px 15px; font-size: 16px; font-weight: bold; color: #000; border-right: 4px solid #000;">稀有度</div>
                <div style="flex: 1; padding: 12px 15px; font-size: 16px; font-weight: bold; color: #000;">价格</div>
            </div>

            <!-- 表格行 -->
            <div style="display: flex; border-bottom: 2px solid #000;">
                <div style="flex: 1; padding: 10px 15px; font-size: 14px; color: #000; border-right: 2px solid #000; background-color: #fff; font-weight: bold;">像素剑</div>
                <div style="flex: 1; padding: 10px 15px; font-size: 14px; color: #00f; border-right: 2px solid #000; background-color: #fff; font-weight: bold;">稀有</div>
                <div style="flex: 1; padding: 10px 15px; font-size: 14px; color: #000; background-color: #fff; font-weight: bold;">500金币</div>
            </div>

            <!-- 表格行（交替背景） -->
            <div style="display: flex; border-bottom: 2px solid #000;">
                <div style="flex: 1; padding: 10px 15px; font-size: 14px; color: #000; border-right: 2px solid #000; background-color: #ffcccc; font-weight: bold;">魔法药水</div>
                <div style="flex: 1; padding: 10px 15px; font-size: 14px; color: #f0f; border-right: 2px solid #000; background-color: #ffcccc; font-weight: bold;">史诗</div>
                <div style="flex: 1; padding: 10px 15px; font-size: 14px; color: #000; background-color: #ffcccc; font-weight: bold;">1200金币</div>
            </div>

            <!-- 表格行 -->
            <div style="display: flex;">
                <div style="flex: 1; padding: 10px 15px; font-size: 14px; color: #000; border-right: 2px solid #000; background-color: #fff; font-weight: bold;">盾牌</div>
                <div style="flex: 1; padding: 10px 15px; font-size: 14px; color: #0a0; border-right: 2px solid #000; background-color: #fff; font-weight: bold;">普通</div>
                <div style="flex: 1; padding: 10px 15px; font-size: 14px; color: #000; background-color: #fff; font-weight: bold;">200金币</div>
            </div>
        </div>

        <div style="font-size: 12px; color: #666; margin-top: 10px; text-align: right; font-weight: bold;">像素风格，数据清晰，视觉冲击力强</div>
    </section>'''

    # 其他模板使用通用表格
    else:
        return '''    <!-- 组件：表格（通用风格） -->
    <section style="margin: 30px 0;">
        <div style="font-size: 13px; color: #666; margin-bottom: 10px; font-weight: bold;">组件：数据表格</div>

        <!-- 表格容器 -->
        <div style="border: 1px solid #ddd; overflow: hidden; border-radius: 4px;">

            <!-- 表头 -->
            <div style="display: flex; background-color: #f5f5f5; border-bottom: 1px solid #ddd;">
                <div style="flex: 1; padding: 12px 15px; font-size: 14px; font-weight: bold; color: #333; border-right: 1px solid #ddd;">项目</div>
                <div style="flex: 1; padding: 12px 15px; font-size: 14px; font-weight: bold; color: #333; border-right: 1px solid #ddd;">数值</div>
                <div style="flex: 1; padding: 12px 15px; font-size: 14px; font-weight: bold; color: #333;">状态</div>
            </div>

            <!-- 表格行 -->
            <div style="display: flex; border-bottom: 1px solid #eee;">
                <div style="flex: 1; padding: 10px 15px; font-size: 14px; color: #333; border-right: 1px solid #eee;">数据项A</div>
                <div style="flex: 1; padding: 10px 15px; font-size: 14px; color: #333; border-right: 1px solid #eee;">85%</div>
                <div style="flex: 1; padding: 10px 15px; font-size: 14px; color: #0a0;">良好</div>
            </div>

            <!-- 表格行 -->
            <div style="display: flex; border-bottom: 1px solid #eee;">
                <div style="flex: 1; padding: 10px 15px; font-size: 14px; color: #333; border-right: 1px solid #eee;">数据项B</div>
                <div style="flex: 1; padding: 10px 15px; font-size: 14px; color: #333; border-right: 1px solid #eee;">62%</div>
                <div style="flex: 1; padding: 10px 15px; font-size: 14px; color: #fa0;">一般</div>
            </div>

            <!-- 表格行 -->
            <div style="display: flex;">
                <div style="flex: 1; padding: 10px 15px; font-size: 14px; color: #333; border-right: 1px solid #eee;">数据项C</div>
                <div style="flex: 1; padding: 10px 15px; font-size: 14px; color: #333; border-right: 1px solid #eee;">95%</div>
                <div style="flex: 1; padding: 10px 15px; font-size: 14px; color: #0a0;">优秀</div>
            </div>
        </div>

        <div style="font-size: 12px; color: #999; margin-top: 8px; text-align: right;">数据表格组件，支持多列展示</div>
    </section>'''

def find_insert_position(content):
    """
    在内容中查找合适的插入位置
    策略：在分栏布局（display: flex）之后，图片组件之前插入
    """
    lines = content.split('\n')

    # 查找分栏布局的结束位置
    for i, line in enumerate(lines):
        if 'display: flex' in line and 'justify-content:' in line:
            # 找到分栏布局的开始，需要找到对应的结束标签
            for j in range(i, min(i+20, len(lines))):
                if '</section>' in lines[j] and 'margin-bottom:' in lines[j-1]:
                    return j + 1  # 在</section>之后插入

    # 如果没找到分栏布局，查找双栏布局的典型模式
    for i, line in enumerate(lines):
        if 'width: 48%' in line or 'flex: 1' in line:
            for j in range(i, min(i+15, len(lines))):
                if '</section>' in lines[j]:
                    return j + 1

    # 如果还是没找到，在图片组件之前插入
    for i, line in enumerate(lines):
        if 'margin-bottom:' in line and 'img src=' in '\n'.join(lines[i:i+5]):
            return i - 1 if i > 0 else 50  # 在图片组件之前插入

    # 默认位置：大约在文件中间
    return len(lines) // 2

def add_table_to_template(filepath):
    """为模板文件添加表格组件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 检查是否已经包含表格组件
    if '组件：表格' in content or '数据表格' in content:
        print(f"  {os.path.basename(filepath)}: 已包含表格组件，跳过")
        return False

    # 获取模板名称
    template_name = os.path.basename(filepath)

    # 获取表格组件
    table_component = get_table_for_template(template_name)

    # 查找插入位置
    insert_pos = find_insert_position(content)

    # 插入表格组件
    lines = content.split('\n')
    lines.insert(insert_pos, '\n' + table_component + '\n')

    # 保存文件
    new_content = '\n'.join(lines)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"  {template_name}: 已添加表格组件")
    return True

def main():
    """主函数"""
    templates_dir = "/Users/qiuhe/Documents/skills/.claude/skills/wechat-article-formatter/assets/templates"

    if not os.path.exists(templates_dir):
        print(f"错误：模板目录不存在 {templates_dir}")
        return

    # 获取所有HTML模板文件
    template_files = [f for f in os.listdir(templates_dir) if f.endswith('.html')]

    print(f"找到 {len(template_files)} 个模板文件")

    # 为每个模板添加表格组件
    count = 0
    for template_file in template_files:
        filepath = os.path.join(templates_dir, template_file)
        try:
            if add_table_to_template(filepath):
                count += 1
        except Exception as e:
            print(f"  {template_file}: 错误 - {e}")

    print(f"\n完成！已为 {count}/{len(template_files)} 个模板添加表格组件")

if __name__ == "__main__":
    main()