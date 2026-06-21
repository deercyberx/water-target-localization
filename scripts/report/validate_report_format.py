# -*- coding: utf-8 -*-
"""
报告格式验证脚本
检查 generate_report.py 中的格式规范
"""

import re

def validate_report_format():
    """验证报告格式规范"""
    issues = []

    with open('generate_report.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # 检查1: 正文字体字号
    # 规范: 宋体/小四/1.5倍行距
    if "font.size = Pt(12)" in content:
        # 小四 = 12pt，字号正确
        pass
    else:
        issues.append({
            "severity": "critical",
            "location": "全局设置",
            "description": "正文字号未设置为小四(12pt)",
            "suggestion": "在 style.font.size = Pt(12) 设置正文字号"
        })

    # 检查行距
    if "line_spacing" not in content and "WD_LINE_SPACING" not in content:
        issues.append({
            "severity": "major",
            "location": "全局设置",
            "description": "未设置1.5倍行距",
            "suggestion": "添加 paragraph_format.line_spacing = 1.5 或 WD_LINE_SPACING.ONE_POINT_FIVE"
        })

    # 检查2: 一级标题格式
    # 规范: 黑体三号 (16pt)
    if "doc.add_heading(" in content:
        # 使用默认Heading样式，未设置黑体三号
        issues.append({
            "severity": "critical",
            "location": "一级标题",
            "description": "一级标题使用默认Heading样式，未设置为黑体三号(16pt)",
            "suggestion": "修改Heading 1样式: font.name='黑体', font.size=Pt(16)"
        })

    # 检查3: 页边距
    # 规范: 上下2.54cm，左右3.17cm
    if "top_margin" not in content and "bottom_margin" not in content:
        issues.append({
            "severity": "critical",
            "location": "页面设置",
            "description": "未设置页边距（规范: 上下2.54cm，左右3.17cm）",
            "suggestion": "添加 section.top_margin = Cm(2.54), section.bottom_margin = Cm(2.54), section.left_margin = Cm(3.17), section.right_margin = Cm(3.17)"
        })

    # 检查4: 公式格式
    # 规范: 居中，加粗
    formula_count = content.count("p.alignment = WD_ALIGN_PARAGRAPH.CENTER")
    bold_count = content.count("run.bold = True")
    if formula_count > 0 and bold_count > 0:
        # 公式居中和加粗已设置
        pass
    else:
        issues.append({
            "severity": "major",
            "location": "公式",
            "description": "公式未设置居中或加粗",
            "suggestion": "确保公式段落居中对齐且run.bold=True"
        })

    # 检查公式字号
    formula_font_size = re.findall(r'run\.font\.size = Pt\((\d+)\)', content)
    if formula_font_size:
        sizes = [int(s) for s in formula_font_size]
        if 11 in sizes:
            issues.append({
                "severity": "minor",
                "location": "公式",
                "description": "公式字号设置为11pt，不是标准小四(12pt)",
                "suggestion": "统一公式字号为Pt(12)或按规范设置"
            })

    # 检查5: 表格格式
    # 规范: 居中，表头加粗，蓝色背景
    if "table.alignment = WD_TABLE_ALIGNMENT.CENTER" in content:
        pass
    else:
        issues.append({
            "severity": "major",
            "location": "表格",
            "description": "表格未设置居中",
            "suggestion": "添加 table.alignment = WD_TABLE_ALIGNMENT.CENTER"
        })

    if "set_cell_shading(cell, 'D9E2F3')" in content:
        # 蓝色背景已设置
        pass
    else:
        issues.append({
            "severity": "major",
            "location": "表格",
            "description": "表头未设置蓝色背景",
            "suggestion": "添加 set_cell_shading(cell, 'D9E2F3') 设置表头蓝色背景"
        })

    # 检查6: 字体设置
    if "'宋体'" in content:
        pass
    else:
        issues.append({
            "severity": "critical",
            "location": "全局设置",
            "description": "未设置宋体字体",
            "suggestion": "设置 font.name='宋体' 和 eastAsia='宋体'"
        })

    # 检查黑体
    if "'黑体'" not in content:
        issues.append({
            "severity": "critical",
            "location": "标题设置",
            "description": "标题未设置黑体字体",
            "suggestion": "修改Heading样式使用黑体字体"
        })

    # 统计问题数量
    critical_count = sum(1 for i in issues if i['severity'] == 'critical')
    major_count = sum(1 for i in issues if i['severity'] == 'major')
    minor_count = sum(1 for i in issues if i['severity'] == 'minor')

    # 确定状态
    if critical_count > 0:
        status = "FAIL"
    elif major_count > 0:
        status = "FAIL"
    else:
        status = "PASS"

    # 生成总结
    if status == "PASS":
        summary = "报告格式验证通过，所有规范均已满足"
    else:
        summary = f"报告格式验证失败：{critical_count}个严重问题，{major_count}个主要问题，{minor_count}个次要问题"

    return {
        "agent": "格式验证",
        "status": status,
        "issues": issues,
        "summary": summary
    }

if __name__ == "__main__":
    import json
    result = validate_report_format()
    print(json.dumps(result, ensure_ascii=False, indent=2))
