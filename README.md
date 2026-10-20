# Agentic Science Challenge

面向材料科学与 AI for Science 的题解、计算复现和经验总结。维护者：[@justwingdong-cyber](https://github.com/justwingdong-cyber)。

本仓库记录真实执行过程，区分计划、实现、本地验证与平台评分。当前 **2 道题通过本地独立验证，其中 FRET 首题已提交、荧光猝灭拟合尚未提交**；平台最终成绩仍未知。

## 最简 Agent

已提供基于本机 Codex CLI 的可执行入口，详见 [运行说明](docs/MINIMAL-AGENT.md)：

```powershell
python scripts/asc_agent.py run --challenge-id f-rster-resonance-energy-transfer-efficiency-calcu-4fff2cf6
```

它读取公开题面、执行模型和解题脚本、保存真实轨迹与日志并校验输出契约。模型沿用本机 Codex 配置；当前入口不执行平台提交。

## 分类

| 目录 | 内容 |
|---|---|
| [液晶与光学](solutions/liquid-crystals-optics/README.md) | 胆甾相液晶、光传播、液晶器件 |
| [聚合物与力学](solutions/polymers-mechanics/README.md) | 黏弹性、本构模型、相行为 |
| [材料计算](solutions/materials-simulation/README.md) | DFT、MD、材料性质与结构 |
| [机器学习与优化](solutions/ml-optimization/README.md) | 主动学习、逆向设计、多目标优化 |
| [科学证据与文献](solutions/scientific-evidence/README.md) | 文献证据核对、研究问题回答 |

## 首批候选题

以下中文为便于阅读的译名；题目正式标题、ID 与来源保存在 [catalog.json](catalog.json)。排序依据与风险见 [选题清单](docs/CHALLENGE-SHORTLIST.md)，首题真实执行情况见 [Agent 验收记录](docs/MINIMAL-AGENT.md)。

| 题目 | 分类 | 状态 |
|---|---|---|
| FRET 效率与寿命计算 | 液晶与光学 | 已提交，attempt 57926，等待评分 |
| [距离依赖的荧光猝灭拟合](solutions/liquid-crystals-optics/distance-dependent-fluorescence-quenching-model-fi-536026a1/README.md) | 液晶与光学 | 本地独立验证通过，未提交 |
| FRET 相对荧光产率计算 | 液晶与光学 | 待开始 |
| 聚合物溶液旋节温度与 UCST 临界点计算 | 聚合物与力学 | 待开始 |
| 聚合物单轴黏弹性响应模拟 | 聚合物与力学 | 待开始 |
| 胆甾相液晶中的电磁场分布与能量积累 | 液晶与光学 | 待开始 |
| 液晶盒填充时间模拟 | 液晶与光学 | 暂缓 |

## 如何阅读与复现

每个完成的题解放在 `solutions/<category>/<challenge-id>/`，包含题解 README、源代码、固定的依赖版本、运行说明、必要测试与结果摘要。每个题解必须注明数据获取方式、随机种子（如适用）、实际运行环境和局限。

- [题解模板](templates/solution/README.md)
- [结果记录模板](templates/solution/result.json)
- [复现与发布流程](docs/WORKFLOW.md)
- [工具与账号配置](docs/SETUP.md)
- [来源与许可边界](docs/SOURCES.md)

`local-validated` 只表示本地验证通过；只有平台返回最终评分后才记为 `scored`。失败尝试可记录，但不得把估计数值写成计算结果。

## 开源许可

本仓库原创代码与文字采用 [MIT License](LICENSE)。赛事题面、论文、第三方代码及数据保留原许可；未明确允许再分发的材料只提供来源和下载步骤。认证信息、完整私人聊天和原始 session 日志不进入公开仓库。

## 来源

[The Playground](https://play.bohrium.com/) · [Bohrium CLI 与 Skills](https://github.com/dptech-corp/bohrium-skills)

题目目录初筛日期：2026-10-20（Asia/Shanghai）。
