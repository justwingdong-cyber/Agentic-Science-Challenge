# 最简可执行 Agent 单元

入口：[scripts/asc_agent.py](../scripts/asc_agent.py)。只依赖 Python 标准库和本机 Codex CLI，复用 `codex login` 登录，不需要在代码中写 API key。

## 一次真实执行

在项目根目录运行：

```powershell
python scripts/asc_agent.py run --challenge-id f-rster-resonance-energy-transfer-efficiency-calcu-4fff2cf6
```

工作目录为 `asc-work/<challenge_id>/`。题包需预先下载。入口接受 `task/instruction.md` 或当前 CLI 实际生成的 `task/task.md`，从公开题面提取 outputs JSON 契约。

如果题目依赖 NumPy/SciPy，先为该题准备独立环境，再用该环境的 Python 启动 runner；runner 会把实际解释器路径传给 Agent，避免误用缺少依赖的系统 Python。

最小闭环：读取公开题面 → `codex exec --json` 实际推理和工具执行 → 产出脚本与答案 → 本地契约校验 → 保存轨迹、运行日志和状态。模型沿用当前 Codex 配置；需要固定实际模型时使用 `--model <真实模型标识>`。runner 只记录 requested_model，不将配置继承冒充型号已核实。

| 文件 | 内容 |
|---|---|
| `scripts/` | Agent 编写的可复跑解题与核验脚本 |
| `outputs/` | 题面要求的最终答案 |
| `traces/trace.jsonl` | 实际 Codex JSONL stdout；不生成虚假事件，已知凭据模式会脱敏 |
| `logs/agent_prompt.md` | 实际送给 Agent 的指令 |
| `logs/run.json` | 实际命令、退出状态和轨迹来源 |
| `logs/codex.stderr.log` | CLI 错误日志 |
| `logs/validation.json` | 输出契约、文件哈希与大小检查 |
| `logs/review.md` | Agent 的方案与最终审核记录 |
| `result_summary.md` | 方法、来源、命令、独立核验结果与限制 |
| `status.json` | 本地执行状态与平台提交状态，保留未知分数 null |

存在先前 outputs 或 trace 时 runner 拒绝覆盖；再次运行前手动将整题旧运行归档。超时可用 `--timeout 900` 设置秒数。失败看该题日志，不能盲目重跑。

## 本地检查

不再次调用模型，只验证输出契约：

```powershell
python scripts/asc_agent.py check --challenge-id f-rster-resonance-energy-transfer-efficiency-calcu-4fff2cf6
python -m unittest discover -s scripts -p test_asc_agent.py
```

初版支持 JSON 对象、CSV/TSV 和文本输出，检查所需字段/列、有限数字、文件存在、多余文件、路径越界、部分已知凭据模式与大小。科学正确性必须结合题目独立核验，契约校验不能替代科学验证或平台评分。暂不支持的格式明确报错，扩展校验后再运行新任务。

runner 成功状态为 `contract-validated`，仅表示模型正常结束并通过输出契约。经独立科学核验后再将题目进度标为 `local-validated`；平台最终得分仍须实际提交和查询。

## 审核、轨迹与提交

提示词要求执行项目约定的 grill-me 审核，记录问题与证据；真正需要用户决定的未决项应记录后停止。审核内容需阅读核实，不把文件存在视为审核通过。

在实际提交前继续执行项目的轨迹验证、独立结果检查和 dry-run。runner 本身不上传比赛提交，不消费 Bohrium 算力；它调用的 Codex 使用当前账号的模型额度。还需核实题面的评分契约与实际模型身份。

```powershell
playground trace validate --trace asc-work/<challenge_id>/traces/trace.jsonl
```

原生轨迹会真实反映命令与消息。日志采用已知模式脱敏并剔除若干服务凭据环境变量；这不是完备的数据防泄漏系统。不得向 Agent 提供私密文件或在命令中打印凭据。Codex 的 workspace-write 控制写入，题面读取限制由 runner 的文件白名单和 Agent 指令实施，不应把它误称为完整的操作系统读隔离。

CLI 用法依据本机 `codex exec --help` 和 [OpenAI 官方非交互执行文档](https://developers.openai.com/codex/noninteractive/)。

## 本机验收记录（2026-10-20）

- 已用真实 `codex exec --json` 完成 FRET 首题，产出两份最终文件及三份可复跑脚本；不是 mock 模型运行。
- 求解器执行两次输出字节一致，独立 Fraction 核验、边界/单调性/反解检查通过。
- 主 agent 用 60 位 Decimal 另行复算，最大绝对误差约 1.73e-14；独立记录保存在该题 logs/host-independent-check.json。
- `playground trace validate` 返回 valid=true，23 条 JSONL 事件、14 条 usable events；这仅证明本次轨迹可解析，不保证平台轨迹评分。
- 六项 unittest 通过，包含路径越界、多余文件、非有限/错误数字、凭据模式及公开题面白名单。
- 未提交比赛、未调用 Bohrium 计算资源；评分描述冲突仍记录为限制。
