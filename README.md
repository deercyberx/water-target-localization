# 论文复现: [论文标题]

## 基本信息

- 论文: [标题]
- 作者: [作者]
- 链接: [arXiv / DOI]
- 复现目标: [你要复现的具体指标/图表]

## 环境

- Python: 3.10+
- GPU: [有/无]
- 依赖安装: pip install -r requirements.txt

## 快速开始

```powershell
cd code
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python train.py
```

## 实验

```powershell
cd experiments
powershell -ExecutionPolicy Bypass -File run_experiment.ps1
```

## 已知差异

| 实现点 | 论文描述 | 当前实现 | 原因 |
|--------|----------|----------|------|
| [模块1] | [论文原文] | [你的实现] | [假设/差异原因] |

---

## Prompt 模板

### Round 1: 跑通环境

```
目标: 稳定运行当前仓库。
请完成:
1) 修复 import/runtime error
2) 输出可直接复制的运行命令 (Windows PowerShell)
3) 先跑 train 1 epoch, 确保可正常结束
4) 给出: 已修复点 + 未解决问题 + 下一步优先级
```

### Round 2: 对齐论文

```
目标: 把实现对齐到论文。
请按 paper/notes.md 逐项检查:
- loss function / optimizer / scheduler / model layer
每改一处都说明: 改了什么、对应论文哪节、可能对结果有什么影响
```

### Round 3: 正式实验

```
目标: 建立可复现实验流程。
请完成:
1) 增加实验脚本
2) 固定 seed
3) 训练日志写入 logs/
4) 输出指标 CSV
5) 给一个可重复运行命令
```

### 调试闭环 (通用)

```
请修复当前错误:
1) 根因
2) 最小修复
3) 是否影响论文对齐
4) 如果信息不足, 列出你的假设
```