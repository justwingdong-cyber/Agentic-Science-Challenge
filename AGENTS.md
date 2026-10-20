# Agentic Science Challenge 工作约定

本目录是独立的科研复现仓库，不适用父目录无畏契约网页应用的产品需求。

- 用户已授权将本项目原创题解分类整理并开源到其 GitHub；完成内容审查后可正常提交和推送，无需每题重复询问发布意愿。
- 默认目标仓库：justwingdong-cyber/Agentic-Science-Challenge。首次推送前核实远端确实属于该用户。
- 按 README 分类，一题一目录，目录名用真实 challenge ID。
- 每题本地工作目录固定为 `asc-work/<challenge_id>/`，进入该目录后运行 `playground task download --challenge-id <challenge_id> --out task`。题包位于 `task/`；使用真实 ID，不创建字面占位符目录。整个 asc-work 工作区忽略提交，核验后的原创题解整理到 solutions 分类目录。
- 每题工作区统一包含 `task/`、`scripts/`、`outputs/`、`traces/`、`logs/`、`bohr-result/` 以及 `result_summary.md`、`submission.json`、`status.json`，含义与初始化规则见 docs/WORKFLOW.md。初始化时明确未运行、未提交和未知字段，不预填虚构的任务 ID、评分或成功状态。
- 先读题面、数据协议、评分与预期产物，再实现；以真实计算忠实复现，不编造结果、评分、轨迹或已通过的检查。
- catalog.json 的状态使用 planned / in-progress / local-validated / submitted / scored / failed；评分未知时填 null。
- 正式题解包含方法、环境、执行命令、验证、结果、失败与局限。公开摘要可删去私人信息，提交比赛的原生轨迹须真实保存且满足平台要求。
- 私人数据、凭据、原始 session 日志、下载的题包置于仓库忽略目录，不能盲目 git add 整个工作区。
- 公开第三方数据/题面前核对该材料的再分发许可；限制或禁运适用时只公开允许的原创内容与来源链接。
- CLI 参数以当前 --help 为准；Bohr 具体操作先读 bohr skills read <name>。
- 用户授权接入赛事算力环境。实际执行时先核实资源归属、额度和费用；没有选定题目时不启动计算资源。
- 后续完成一道题时，同步分类索引、catalog.json、题解与可复现产物，并记录真实平台 attempt ID/最终分数（如有）。

## grill-me 审核与提交前调用

- 用户已明确要求：在本项目任务的审核层以及提交前调用 `grill-me`。这是持续生效的项目工作流要求。
- 每次实际调用时读取本机 `~/.codex/skills/grill-me/SKILL.md`；当前上游版本是入口，转交 `~/.codex/skills/grilling/SKILL.md`。没有 Skill 工具时直接读取并遵循这两个文件，不声称调用了不存在的工具。
- 方案审核：读完题面和评分契约、形成方案后，实施主要计算前调用。检查交付范围、假设、数据可用性、方法选择、验证标准、资源需求与未决依赖。
- 提交前审核：产物和必要验证准备完成后，上传 Playground 或发布 GitHub 题解前调用。检查逐项需求覆盖、真实运行证据、指标与评分口径、依赖和命令可复现性、原生轨迹、产物完整性、数据许可及公开内容。
- 使用已有用户决定和验证证据解决已定事项，不重复询问已有授权；可调查的事实先调查，不能把事实核查转嫁给用户。按照 grilling 的依赖分轮提出真正未决的问题，并附建议答案；等待回答后处理依赖这些决定的工作。
- 审核不是自动测试或外部评分的替代。仅在实际执行后记录已审核；保存问题、证据、决策、修复与未解决项。存在影响正确性或交付的未决项时，不标记审核通过、不提交相关产物。
- 审核记录采用 `templates/review.md`。私人问答放在忽略目录 `.private/reviews/`；公开题解只保留必要且已脱敏的审核摘要。产物有实质变化后重审受影响项。
- 来源与安装版本见 `docs/GRILL-ME.md`。
