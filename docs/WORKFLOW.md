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
| `outputs/` | 只放题目要求的最终答案和必要说明；禁止缓存、依赖包、密钥文件及无关大文件 |
| `traces/` | 真实原生 agent 轨迹，统一路径 `traces/trace.jsonl`；记录来源，不伪造或用普通日志替代 |
| `logs/` | 下载、计算、验证、审核与提交操作日志 |
| `bohr-result/` | 从 Bohrium 下载的计算结果，核验后再整理到 outputs |
| `result_summary.md` | 方法、运行环境、实际结果、验证与局限摘要 |
| `submission.json` | 本地提交记录：初始化为未提交，实际提交后记录真实 attempt ID 和响应；其自身不替代平台要求的提交清单 |
| `status.json` | 本地任务进度与最新查询到的平台状态，包含查询时间；最终分数未知时为 null |

建档时创建上述文件和目录。未执行步骤明确标记未运行，未提交时 attempt ID 和最终分数为 null；后续依据真实命令响应更新。题目对 outputs 内文件的具体格式和命名有要求时，以题面为准。

提交前逐项核对 `outputs/` 的文件清单和大小，确保每个文件都对应题目要求或必要说明；不要将整套工作区、依赖环境、缓存、凭据或无关计算结果作为输出打包。

Agent 身份运行前，将 `PLAYGROUND_CREDENTIALS_PATH` 指向本机私有凭据文件。`asc-work/` 是忽略的本地工作区；经核验并适合公开的原创代码、题解和复现说明整理到 `solutions/<category>/<challenge_id>/`。

## 平台数据与远程资源

依赖平台数据、计算或模型服务时先检查：

```bash
bohr version
bohr doctor --output json
playground data list --limit 20 --json
```

查看命令的实际响应与诊断字段，不能只根据退出码判断所有服务可用。题目声明数据集后，在该题工作目录运行（替换真实 ID 和版本）：

```bash
playground data pull --dataset <dataset_id> --version <version> --out data/
```

`data/` 为按需创建的本地输入目录，不属于最终提交输出。记录数据 ID、固定版本、来源和必要的完整性校验；不读取 hidden tests、checker 或官方 solution。

- 小数据先本地运行，快速验证输入与输出格式。
- 长时间计算使用 Bohrium 作业或沙盒；运行前核实资源、额度和计费渠道，并读取对应 Bohr skill。
- 大模型、领域模型和内部推理服务按题目说明使用 Trisol；不凭工具名称猜测调用协议。
- 所有远程 job ID、实际命令、stdout/stderr 记录到 `logs/`，在 `result_summary.md` 汇总运行与结果下载位置。需要返回敏感信息的认证命令不得直接重定向整段输出，日志先过滤凭据。
- 轨迹统一使用真实原生 `traces/trace.jsonl`。不打印环境变量全集，不将 token、access key、密码、cookie 写入轨迹、日志或提交文件。

## 提交命令与身份记录

在对应题目工作目录运行，将变量替换为真实信息。`--model` 使用实际解题模型标识，`--harness` 使用实际运行方式（如 codex、bohrium-agent、harbor-lbg、manual、custom-agent）。只有确实人工完成时才填写 manual；不能照抄示例模型，也不能将未知型号当作已知。

推荐显式提供真实轨迹：

```bash
set -o pipefail
challenge_id="实际题目ID"
model_name="实际模型标识"
harness_name="实际运行方式"

playground trace validate --trace traces/trace.jsonl \
  > logs/trace-validation.json 2> logs/trace-validation.stderr.log
```

轨迹验证通过、grill-me 审核完成且 outputs 内容就绪后，再构建并检查提交预演；任一步失败都先处理，不能直接继续实际提交：

```bash
playground submit \
  --challenge-id "$challenge_id" \
  --outputs outputs \
  --trace traces/trace.jsonl \
  --model "$model_name" \
  --harness "$harness_name" \
  --dry-run \
  > logs/submission-dry-run.json 2> logs/submission-dry-run.stderr.log
```

核对预演产物和结果后，实际提交：

```bash
playground submit \
  --challenge-id "$challenge_id" \
  --outputs outputs \
  --trace traces/trace.jsonl \
  --model "$model_name" \
  --harness "$harness_name" \
  2> logs/submission.stderr.log | tee submission.json
```

`set -o pipefail` 防止 tee 掩盖提交失败。保留提交退出状态，核对 submission.json 的实际响应并记录 attempt ID；不要仅凭文件存在判断成功。重试失败上传时遵循 CLI 返回的同一 attempt ID 重试指令，保留之前的响应与日志。

不显式提供 trace 的简写形式为：

```bash
playground submit \
  --challenge-id "$challenge_id" \
  --outputs outputs \
  --model "$model_name" \
  --harness "$harness_name" \
  2> logs/submission.stderr.log | tee submission.json
```

**当前版本限制（0.1.40）**：省略 `--trace` 时 CLI 尝试自动发现原生轨迹；找不到真实有效轨迹则拒绝创建新提交。这种简写并非无轨迹提交。没有真实轨迹时不伪造，也不宣称可以先提交 outputs 后补轨迹；保留已有产物，后续通过真实执行生成轨迹。升级后以当前帮助与实际验证为准。

## 查询评分与分层排错

从 `submission.json` 的实际成功响应找到 `attempt_id`；若响应结构不同，先核对字段，不猜测 ID。没有成功提交或有效 ID 时不执行占位符查询。在对应题目目录运行：

```bash
set -o pipefail
attempt_id="submission.json 中的实际 attempt_id"
playground status --attempt-id "$attempt_id" \
  2> logs/status.stderr.log | tee status.json
playground status --attempt-id "$attempt_id" --bundle \
  > logs/status-bundle.json 2> logs/status-bundle.stderr.log
```

每次查询记录查询时间、attempt ID、退出状态和原始平台状态；覆盖最新 status.json 前保留有用的历史响应。`--bundle` 是只读详情查询，不代表自动下载提交包。CLI 的状态查询不会自动下载或分享生成的 skill。

| 平台状态 | 解释与处理 |
|---|---|
| `queued` / `running` | 排队或评测中，稍后查询，不重复提交 |
| `scoring` | 后端评分中；已有细节也不视为最终得分 |
| `scored` | 已产生终态得分，核对详情后同步 catalog 和 result_summary |
| `failed` | 查看具体错误、日志和失败层，修复原因后再决定如何重试 |

平台可能返回其他状态或分离的 attempt/bundle 状态，保留实际值并依据响应解释；不要将 unknown、provisional 或中间分数写成最终成绩。catalog 的任务进度与平台原始状态分别记录；最终分数未知时保留 null。

失败时逐层定位：安装 → 认证 → 题目下载 → 输出格式 → 依赖 → 计算 → 提交包 → 评分器 → trace → 平台。顺序用于排查，不表示每种失败必须重跑所有阶段。记录错误消息、关键日志、request ID（如有）、修复措施和复核结果，禁止打印凭据或环境变量全集。确认是评分器或平台失败时保留证据，不把它解释为答案错误；上传重试沿用 CLI 指定的原 attempt ID，避免创建重复提交。

参考：本机 Playground 0.1.40 的 `submit --help`、`status --help`、轨迹校验和提交实现，以及 Playground `GET /api/docs/compete-and-submit`，核对日期 2026-10-20。具体比赛是否仍在进行以比赛页为准，题目 open 状态不等于赛事报名仍开放。
