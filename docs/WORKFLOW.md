# 题解与发布流程

1. 获取题目：每题单独建立 `asc-work/<challenge_id>/`，进入后用 `playground task download --challenge-id <challenge_id> --out task` 下载真实题包至 `task/`。核对任务说明、评分方式、预期产物与数据许可。不要依据标题猜测交付要求。
2. 建档：在分类目录创建题解，复制 templates/solution 内容，填入真实题目 ID，并将 catalog 状态改为 in-progress。
   方案审核：调用 `grill-me`（当前转交 `grilling`），按依赖梳理任务与方法决定；先核查事实，解决真正未决的取舍，再开展依赖这些决定的实现。记录见 [审核模板](../templates/review.md)。
3. 实现：建立最小基线、固定依赖版本与随机种子，再做必要的精度/收敛/守恒等检查。保留实际失败和修复记录。
4. 验证：从独立环境按公开说明复现；记录数值误差、单位、硬件和耗时。通过后标为 local-validated。
5. 提交：保存真实原生 agent session，在本地验证并对比赛提交做 dry-run。上传真实产物和符合平台要求的轨迹。原始日志留在仓库之外。
   上传前必须调用 `grill-me`：对照题面和评分契约审查产物、真实运行证据、误差与复现命令、轨迹有效性。解决影响交付的未决项后再执行实际提交；不得把 dry-run 成功当作最终评分。
6. 评分：记录 attempt ID 和状态；provisional 分数不是最终评分。服务器最终返回 scored 后才更新最终分数。
7. 整理：在题解中总结有效方法、失败原因、适用条件；同步 catalog 和分类索引。
8. 发布：核对跟踪文件、第三方许可和适用赛事公开要求，排除凭据、私人聊天与隐藏测试数据，提交原创代码及总结到用户仓库。
   GitHub 发布前同样执行 `grill-me` 审核，针对公开文件和题解结论核验；可引用同一版本已完成的事实检查，但对新增或变更内容补审。

平台要求原生轨迹，不得事后伪造轨迹。公开的解题过程摘要不替代正式提交轨迹。

本地下载示例（在项目根目录的 Bash 中执行，将实际题目 ID 赋给变量）：

```bash
challenge_id="实际题目ID"
mkdir -p "asc-work/$challenge_id"/{task,scripts,outputs,traces,logs,bohr-result}
cd "asc-work/$challenge_id"
playground task download --challenge-id "$challenge_id" --out task
```

每题标准工作目录：

```text
asc-work/<challenge_id>/
  task/
  scripts/
  outputs/
  traces/
  logs/
  bohr-result/
  result_summary.md
  submission.json
  status.json
```

| 路径 | 用途 |
|---|---|
| `task/` | CLI 下载的原始题包、题面与资源 |
| `scripts/` | 解题、数据处理、计算与验证脚本 |
| `outputs/` | 按题目要求准备的提交产物；不要把整套工作目录作为提交输出 |
| `traces/` | 真实原生 agent 轨迹；记录来源，不伪造或用普通日志替代 |
| `logs/` | 下载、计算、验证、审核与提交操作日志 |
| `bohr-result/` | 从 Bohrium 下载的计算结果，核验后再整理到 outputs |
| `result_summary.md` | 方法、运行环境、实际结果、验证与局限摘要 |
| `submission.json` | 本地提交记录：初始化为未提交，实际提交后记录真实 attempt ID 和响应；其自身不替代平台要求的提交清单 |
| `status.json` | 本地任务进度与最新查询到的平台状态，包含查询时间；最终分数未知时为 null |

建档时创建上述文件和目录。未执行步骤明确标记未运行，未提交时 attempt ID 和最终分数为 null；后续依据真实命令响应更新。题目对 outputs 内文件的具体格式和命名有要求时，以题面为准。

Agent 身份运行前，将 `PLAYGROUND_CREDENTIALS_PATH` 指向本机私有凭据文件。`asc-work/` 是忽略的本地工作区；经核验并适合公开的原创代码、题解和复现说明整理到 `solutions/<category>/<challenge_id>/`。

参考：Playground `GET /api/docs/compete-and-submit`，核对日期 2026-10-20。具体比赛是否仍在进行以比赛页为准，题目 open 状态不等于赛事报名仍开放。
