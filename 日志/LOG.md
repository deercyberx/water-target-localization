# LOG.md

> 活动记录，追加在文件末尾。

---

## 2026-06-15

- 完成论文深度阅读（11 页全文），提取所有关键细节
- 填写 paper/notes.md：论文信息、技术路线、4 个公式、19 种匹配方法 + 14 种检索方法完整对比、实验配置、失败模式分析、水面场景启示
- 填写 CONTEXT.md：论文信息、技术路线、模型结构、数据集、环境配置、实验结果汇总
- 更新 TASKS.md：标记"阅读论文"完成，下一步搭建环境
- 更新 ACTIVE.md：当前阶段 Round 1 — 搭建环境
- Clone 代码到 code/ 目录: https://github.com/UAV-AVL/Benchmark
- 深度分析代码结构和实验流程：
  - 代码目录结构和模块功能
  - 三步定位Pipeline（检索→匹配→PnP）
  - 关键配置参数说明
  - 时间开销估算（RoMa匹配占98%）
  - 环境依赖分析（Python 3.9, PyTorch 2.2.1+cu121）
  - 确认不需要训练，纯推理代码
- 更新 CONTEXT.md：添加代码结构、实验流程、关键配置、环境配置
- 环境搭建完成：
  - 安装 Python 3.9（winget），创建 code/.venv 虚拟环境
  - 安装 PyTorch 2.2.1+cu121 + 18 个依赖包
  - 修复 CAMP get_CAMP.py 的 argparse 冲突（parse_args → parse_args([], namespace=self)）
  - 下载并部署：CAMP权重(349MB)、RoMa权重(426MB)、DINOv2权重(1.2GB)
  - 解压数据集 Data.rar 到 code/Data/（487张UAV图，3个场景）
- 基线跑通验证：25张图，Topn_opt策略，航空参考图，平均误差3.5m，A@5m≈84%
- Round 1 完成
- 航空图 HIGH 完整实验（487 张，Top N Re-rank）：
  - A@5m=82.3%（论文 74.1%），A@10m=90.3%，A@20m=95.9%
  - QZ_SongCity: A@5m=98.3%，Qingzhou_3_2: A@5m=96.6%
  - QingZhou_2024 表现差: A@5m=44.4%，mean=91.75m
- 卫星图 LOW 实验失败：RTX 3080 (10GB) GPU OOM
  - RoMa dense matching 的 local_correlation 需要 ~1.1GB 额外显存
  - 模型 ~4GB + 分配 ~3.5GB + 额外 ~1.1GB > 10GB
  - 需要换 GPU 或改用轻量匹配方法

## 2026-06-16

- 解决 GPU OOM 问题：降低 RoMa 分辨率
  - coarse_res: 560 → 280, upsample_res: 864 → 512
  - 模型显存从 ~4GB 降到 ~0.4GB
  - 添加 torch.cuda.empty_cache() 每次匹配后清理
  - 设置 PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True（Windows 不支持但无害）
- 卫星图 LOW 完整实验成功（487 张）：
  - A@5m=13.6%（论文 18.5%），A@10m=39.4%（论文 38.7%），A@20m=63.7%（论文 58.5%）
  - A@5m 偏低可能是降分辨率影响精细匹配，但 A@10m/A@20m 反而更好
- 完整实验对比：
  - 航空图 HIGH: A@5m=82.3%, A@10m=90.3%, A@20m=95.9%
  - 卫星图 LOW: A@5m=13.6%, A@10m=39.4%, A@20m=63.7%
  - 结论：卫星图精度远低于航空图，与论文一致
- Round 2 完成
- 定位策略对比实验（航空图 HIGH，CAMP+RoMa）：
  - Top N Re-rank: A@5m=82.3%, A@10m=90.3%, A@20m=95.9%
  - Top1: A@5m=68.8%, A@10m=78.2%, A@20m=81.9%
  - Most Inliers: A@5m=79.5%, A@10m=86.2%, A@20m=87.3%
  - 结论：Top N Re-rank 最优，与论文一致
- 俯仰角影响分析（航空图 HIGH + Top N Re-rank）：
  - 20°-50°（倾斜）: A@5m=79.4%, 平均误差 35.5m
  - 70°-90°（正下视）: A@5m=92.9%, 平均误差 11.7m
  - 结论：正下视精度最高，倾斜视角精度下降，与论文一致
- 匹配方法对比实验（航空图 HIGH + Top N Re-rank + CAMP）：
  - RoMa: A@5m=82.3%, A@10m=90.3%, A@20m=95.9%
  - SIFT: A@5m=32.5%, A@10m=37.5%, A@20m=40.9%
  - 结论：RoMa 大幅优于 SIFT，密集匹配远优于稀疏手工方法
- 收集技术报告素材：
  - 微信公众号文章（CVPR 2026 AnyVisLoc 详细介绍）
  - Gemini 3.1 Pro 参考文本（前四章完整内容，含双光融合、EKF 滤波等）
  - 确认所有章节素材齐全
- 实验完成，准备撰写技术报告

## 2026-06-21

- 深度阅读项目全部文件，核对日志记录与实际状态
- 发现素材清单.md严重过时（代码修改"未生效"判断错误，pkl文件实际有2440个，CSV和图表均已存在）
- 读取第五章提纲docx，逐节分析所需素材
- 生成第五章全部图表素材：
  - 图5-3: 完整流程可视化（查询→候选→匹配→PnP），3个代表性样本
  - 图5-4: 航空图vs卫星图对比（误差分布+A@T曲线+分场景）
  - 图5-5: 高度/视角分组分析（俯仰角+高度+场景三维度）
  - 图5-6: 策略/匹配对比柱状图
  - 图5-7: 检测→定位误差传播链路流程图
  - 图5-8: 成功/失败案例可视化（3成功+3失败）
- 生成表格数据汇总（表5-1~5-12完整Markdown版本）
- 修复：PIL替代cv2解决中文路径读取问题、matplotlib字体缓存问题
- 第五章计划审核（3轮）：
  - 一轮：技术有条件通过/学术不通过/数据不通过（图5-4~5-8内容错位、写作口径缺失、俯仰角103vs164）
  - 二轮：技术通过/学术不通过（图5-8第4行应为检测框联动风险、缺表5-12）/数据不通过（表格未更新）
  - 三轮：学术通过/数据通过 — 修正俯仰角164、高度200-300m脚注、噪声来源标注、图5-8四类行、表5-12独立规划
  - 最终结论：计划v2审核通过，可执行
- 执行阶段2完成：A类图表优化
  - 图5-1: 测试区域样例（3场景UAV+参考地图）— 6.5MB，300dpi
  - 图5-4: 航空图vs卫星图对比（误差分布+A@T+分场景+样本量标注）— 414KB
  - 图5-5: 高度/视角分组（样本量标注+50-70°统计有限提示+200-300m无样本说明）— 207KB
  - 图5-6: 策略/匹配/噪声三子图（噪声标注来源AnyVisLoc Table 7）— 267KB
- 执行阶段3完成：B类可视化脚本编写
  - scripts/report/generate_b_type_figures.py — 语法检查通过，导入验证通过
  - 新增函数：process_and_save_all_matches()、draw_pred_on_refmap()
  - 需要GPU环境运行（RTX 3080）
- 阶段4完成：B类脚本运行
  - 修复6个运行时错误：路径解析、JSON name格式、numpy数组bool判断、cv2 flag名称、文件已存在、cv2.imwrite中文路径
  - 全部改用PIL保存/读取图像（兼容中文路径）
  - 启用SHOW_RETRIEVAL_RESULT=True保存检索结果图
  - 生成30个中间文件（6样本×5文件：query/retrieval/match_clean/pnp + 失败案例的match_all/match_inliers）
  - fig5_3_pipeline.png: 13.5MB（真实实验截图）
  - fig5_8_success_failure.png: 11.4MB（真实实验截图）
- 更新素材清单.md：
  - 从"缺失"更新为"齐全"
  - 添加完整的12个数据文件清单
  - 添加完整的7张图+30个中间文件清单
  - 更新任务优先级（16项已完成）
  - 更新素材保存位置目录树
- 撰写第五章初稿：
  - 文件：reports/第五章_实验验证与结果分析_poi-tl_v2.docx
  - 总段落数：66
  - 表格数量：12（表5-1到表5-12）
  - 图片数量：7（图5-1, 5-3, 5-4, 5-5, 5-6, 5-7, 5-8）
  - 内容完整度：100%
- 更新全部日志文件：
  - ACTIVE.md：更新当前阶段、任务、已完成、下一步
  - TASKS.md：标记第五章初稿完成，新增待办任务
  - LOG.md：追加今天活动记录
  - CONTEXT.md：更新报告文件位置和素材状态
  - LEARNINGS.md：添加初稿撰写经验

## 2026-06-23

- 全面文件归类和日志更新：
  - 扫描项目全部文件（排除 .venv/.git/__pycache__），约 200+ 有效文件
  - 归类为 10 大类：日志/论文/代码/报告/脚本/实验数据/图表素材/参考素材/模板/临时文件
  - 发现 `参考素材/` 是早期日志副本，信息过时（GPU 写 RTX 3090 实际 RTX 3080，数据集写"待下载"实际已下载）
  - 发现 `scripts/report/` 有 60+ 一次性脚本，可清理
  - 发现根目录有多个临时分析文件（table_*.txt），可归档
  - 发现 .venv 在项目根目录（非 code/.venv/）
  - 第五章已迭代到 v5 版本（poi-tl 格式化 + 表格优化）
- 更新 ACTIVE.md：Round 3 → Round 4，当前聚焦表格优化
- 更新 TASKS.md：新增 v5 迭代为已完成，新增清理/归档待办
- 更新 CONTEXT.md：修正代码结构、报告文件位置、环境配置（venv路径）
- 更新 LOG.md：追加今天活动记录

- 根目录文件整理：
  - 创建 tmp/ 目录，归档 6 个临时文件（会话记录、字体测试图、4个 table_*.txt/json）
  - 移动 analyze_tables.py → tmp/（未 tracked 的中间产物）
  - 移动 check_format.py → scripts/report/check_format_comprehensive.py（与已有 check_format.py 内容不同，重命名避免冲突）
  - 移动 提示词 → 参考素材/
  - 更新 .gitignore 添加 tmp/
  - 根目录现在只剩 .gitignore + README.md

- 第五章版本更新：确认 v1 为最新版（非之前记录的 v5）
  - 更新表格数据
  - 补充素材到 5all素材/
  - 最新版: reports/第五章_实验验证与结果分析_v1.docx

- Nature Skills 安装与使用：
  - 克隆 nature-skills 仓库到 clone库/
  - 安装 8 个技能到 .claude/skills/（nature-reader/paper2ppt/polishing/figure/writing/citation/reviewer/response）
  - 阅读并理解各技能功能（nature-polishing: 学术文本润色；nature-figure: 投稿级科研图）

- 第五章 Nature 风格润色（使用 nature-polishing 技能）：
  - 轴值检测：paper_type=research, section=results+conclusion, language=zh-to-en, journal=generic
  - 一次润色：中文保留，优化段落逻辑、句式、术语一致性
  - 二次润色：优化句式结构（10-30词）、段落聚焦（一段一意）、精确对冲
  - 输出完整润色版本（中文版）

- 对齐检查（与提纲 v1 逐节对比）：
  - 11节全部对齐（标题、图表编号、写作口径）
  - 发现3处细节差异：
    - 5.3 位姿求解器：提纲写EPnP+RANSAC，实际P3P+RANSAC（润色正确）
    - 5.5 篇幅：提纲建议2-3页，润色约1.5页（合理）
    - 5.9 检测框类型：未逐一命名（已修正）
  - 确认数据一致性：SIFT A@5m=31.2%（PKL）、俯仰角70-90°=164张（PKL）

- 修正 5.9 节检测框类型描述：
  - 明确列出四类：人工标注框、模型预测框、扰动框、多目标框
  - 与表5-11完全对齐

- 生成 v2_polished.docx：
  - 使用 python-docx 替换正文段落
  - 保留原文档的12个表格、图片、格式、字体
  - 输出文件：reports/第五章_实验验证与结果分析_v2_polished.docx

- Nature Reviewer 评审（使用 nature-reviewer 技能）：
  - 生成3份审稿报告 + 1份综合意见
  - 评审轴：originality, scientific importance, interdisciplinary readership, technical soundness, readability
  - 主要问题：公式显示、样本选择标准、图表引用
  - 总体评价：技术扎实，多维度分析全面，任务边界明确

- Nature Response 回复（使用 nature-response 技能）：
  - 制定回复策略，修复3个主要问题：
    1. 公式显示问题：公式整合到段落中，完整显示
    2. 样本选择标准：补充到5.5节最后一个段落
    3. 技术细节解释：增加PDM@K、重投影误差、内点数量、推理时间的解释
  - 生成修改后的文档

- 子代理审核：
  - 启动独立子代理审核修改内容
  - 6项检查全部通过：公式显示、样本选择标准、技术细节、段落完整性、表格完整性、格式保留
  - 发现2个可选改进：公式排版格式、样本选择标准位置
  - 完成可选改进

- 最终状态：
  - 文件：reports/第五章_实验验证与结果分析_v2_polished.docx
  - 段落数量：75
  - 表格数量：12（全部保留）
  - 修改内容：公式显示、样本选择标准、技术细节解释
  - 审核状态：通过

## 2026-06-23（续）

- GitHub仓库清理：
  - 扫描云端仓库文件（261个文件）
  - 分析垃圾文件和重复文件
  - 删除临时文件：tmp/目录（2个文件）
  - 删除重复文件：5all素材/图表/、5all素材/实验数据/、5all素材/参考文献/、5all素材/参考文献补充/（46个文件）
  - 删除过时文件：参考素材/目录（12个文件）
  - 删除重复脚本：5all素材/脚本/（6个文件）
  - 删除重复素材：code/素材/目录（9个文件）
  - 总计删除75个文件，保留185个核心文件
  - 仓库状态：干净整洁，无垃圾文件

- 更新日志系统：
  - 更新ACTIVE.md：当前阶段更新为Round 6，添加GitHub仓库状态
  - 更新TASKS.md：标记GitHub仓库清理完成，更新待办事项
  - 更新LOG.md：追加今天活动记录
  - 更新CONTEXT.md：更新仓库状态和文件统计
