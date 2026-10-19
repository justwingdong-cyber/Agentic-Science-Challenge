# Agentic Science Challenge 工作约定

本目录是独立的科研复现仓库，不适用父目录无畏契约网页应用的产品需求。

- 用户已授权将本项目原创题解分类整理并开源到其 GitHub；完成内容审查后可正常提交和推送，无需每题重复询问发布意愿。
- 默认目标仓库：justwingdong-cyber/Agentic-Science-Challenge。首次推送前核实远端确实属于该用户。
- 按 README 分类，一题一目录，目录名用真实 challenge ID。
- 先读题面、数据协议、评分与预期产物，再实现；以真实计算忠实复现，不编造结果、评分、轨迹或已通过的检查。
- catalog.json 的状态使用 planned / in-progress / local-validated / submitted / scored / failed；评分未知时填 null。
- 正式题解包含方法、环境、执行命令、验证、结果、失败与局限。公开摘要可删去私人信息，提交比赛的原生轨迹须真实保存且满足平台要求。
- 私人数据、凭据、原始 session 日志、下载的题包置于仓库忽略目录，不能盲目 git add 整个工作区。
- 公开第三方数据/题面前核对该材料的再分发许可；限制或禁运适用时只公开允许的原创内容与来源链接。
- CLI 参数以当前 --help 为准；Bohr 具体操作先读 bohr skills read <name>。
- 用户授权接入赛事算力环境。实际执行时先核实资源归属、额度和费用；没有选定题目时不启动计算资源。
- 后续完成一道题时，同步分类索引、catalog.json、题解与可复现产物，并记录真实平台 attempt ID/最终分数（如有）。
