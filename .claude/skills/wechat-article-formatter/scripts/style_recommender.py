#!/usr/bin/env python3
"""
微信公众号排版风格推荐脚本
根据文章内容推荐合适的排版风格
"""

import re
from typing import List, Dict

# 风格描述和关键词映射
STYLE_KEYWORDS = {
    "极简时尚": ["简洁", "现代", "时尚", "专业", "商务", "报告", "分析", "科技"],
    "扁平风格": ["设计", "创意", "视觉", "色彩", "品牌", "营销", "推广", "产品"],
    "像素风格": ["游戏", "复古", "怀旧", "科技", "极客", "编程", "技术", "开发"],
    "复古像素风格": ["复古", "怀旧", "游戏", "80年代", "90年代", "经典"],
    "弥散风格": ["柔和", "渐变", "艺术", "设计", "创意", "抽象", "美学"],
    "手绘风格": ["手工", "艺术", "插画", "创意", "儿童", "教育", "轻松"],
    "酸性设计": ["前卫", "潮流", "时尚", "音乐", "艺术", "实验", "创新"],
    "玻璃拟态风格": ["现代", "透明", "科技", "未来", "界面", "设计", "清新"],
    "新粗野风格": ["大胆", "对比", "强烈", "艺术", "设计", "个性", "独特"],
    "黑白像素": ["简约", "单色", "经典", "摄影", "艺术", "黑白", "对比"]
}

# 风格描述
STYLE_DESCRIPTIONS = {
    "极简时尚": "简洁现代的排版，适合专业文章、科技报道、商业分析",
    "扁平风格": "扁平化设计，色彩鲜明，适合产品介绍、营销内容",
    "像素风格": "像素艺术风格，适合游戏、科技、极客文化相关内容",
    "复古像素风格": "怀旧像素风格，适合复古游戏、怀旧主题文章",
    "弥散风格": "柔和渐变风格，适合艺术、设计、创意类内容",
    "手绘风格": "手绘插画风格，适合教育、儿童、创意手工内容",
    "酸性设计": "前卫酸性设计，适合潮流、音乐、艺术实验内容",
    "玻璃拟态风格": "透明玻璃效果，适合科技、未来感、界面设计内容",
    "新粗野风格": "大胆对比风格，适合艺术评论、设计观点、个性表达",
    "黑白像素": "简约黑白像素，适合摄影、艺术、经典主题内容"
}

def analyze_content(content: str) -> Dict[str, int]:
    """
    分析文章内容，统计关键词出现频率
    """
    content_lower = content.lower()
    keyword_scores = {}

    for style, keywords in STYLE_KEYWORDS.items():
        score = 0
        for keyword in keywords:
            # 统计关键词出现次数
            count = len(re.findall(keyword.lower(), content_lower))
            score += count * 2  # 每个出现的关键词加2分
        keyword_scores[style] = score

    return keyword_scores

def recommend_styles(content: str, top_n: int = 3) -> List[Dict]:
    """
    推荐最适合的排版风格
    """
    scores = analyze_content(content)

    # 按分数排序
    sorted_styles = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    recommendations = []
    for style, score in sorted_styles[:top_n]:
        recommendations.append({
            "style": style,
            "score": score,
            "description": STYLE_DESCRIPTIONS.get(style, "暂无描述"),
            "template_file": f"{style}.html" if style != "极简时尚" else "index.html"
        })

    return recommendations

def get_all_styles() -> List[Dict]:
    """
    获取所有可用的风格
    """
    styles = []
    for style_name, description in STYLE_DESCRIPTIONS.items():
        template_file = f"{style_name}.html" if style_name != "极简时尚" else "index.html"
        styles.append({
            "style": style_name,
            "description": description,
            "template_file": template_file,
            "keywords": STYLE_KEYWORDS.get(style_name, [])
        })
    return styles

if __name__ == "__main__":
    import sys

    # 命令行使用示例
    if len(sys.argv) > 1:
        # 从文件读取内容
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        # 使用测试示例
        content = """
        科技公司发布新产品，采用现代设计语言和扁平化界面。
        这款产品注重用户体验，色彩鲜明，适合年轻人群。
        技术创新和视觉设计相结合，带来全新的使用体验。
        """

    print("文章内容分析:")
    print(content[:200], "...")

    print("\n风格推荐:")
    recommendations = recommend_styles(content)
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec['style']} - 分数: {rec['score']}")
        print(f"   描述: {rec['description']}")
        print(f"   模板文件: {rec['template_file']}")

    print("\n所有可用风格:")
    all_styles = get_all_styles()
    for style in all_styles:
        print(f"- {style['style']}: {style['description']}")