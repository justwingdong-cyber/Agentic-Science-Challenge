# grill-me 审核集成

来源：[mattpocock/skills](https://github.com/mattpocock/skills)。安装日期：2026-10-20。

固定安装提交：`5beb35b040e3de97e54fa9e386d7e42d15c295c2`。

- 入口：`skills/productivity/grill-me/SKILL.md`
- 实际工作流：`skills/productivity/grilling/SKILL.md`
- 本地安装：`~/.codex/skills/grill-me/` 和 `~/.codex/skills/grilling/`

上游的 grill-me 设置了 `disable-model-invocation: true`，是显式调用入口。本项目用户已明确要求在方案审核与提交前使用；触发依据是项目 AGENTS.md 中这项用户指令，不依赖技能描述的自动匹配。

当前入口要求调用 grilling。Codex 环境没有专用 Skill 工具时，读取对应 SKILL.md 执行工作流。保留上游原文件，不自行删除询问、依赖分析或用户决策步骤。

grilling 将决策组织为依赖树，分轮询问当前可决策的问题，每个问题附建议答案。可调查的事实由 agent 核查；真正未决的判断由用户决定。已有授权和已明确的决定直接作为上下文，不重复要求用户批准。

本项目在两个阶段执行：

1. **方案审核**：明确目标、数据、科学假设、方法、验证和资源需求。
2. **提交前审核**：核对产物与真实证据，再分别检查比赛提交和 GitHub 发布要求。

审核记录使用 [templates/review.md](../templates/review.md)。审查发现的问题必须落实为修复或明确限制；未执行审核不能填写“已通过”。本次仅安装并配置流程，未宣称任何题解已经审核或通过评分。

在其他 Codex 环境复用时，应安装上述两个技能。可用 skill-installer 指定同一仓库、提交与两个路径，保证版本一致。升级后重新检查上游依赖与行为。
