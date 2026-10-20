# Agentic Science Challenge

面向材料科学与 AI for Science 的题解、计算复现和经验总结。维护者：[@justwingdong-cyber](https://github.com/justwingdong-cyber)。

本仓库记录真实执行过程，区分计划、实现、本地验证与平台评分。当前为项目初始化阶段，**已完成题解：0**；下列条目是待开始的候选题，不代表已复现或已提交。

## 分类

| 目录 | 内容 |
|---|---|
| [液晶与光学](solutions/liquid-crystals-optics/README.md) | 胆甾相液晶、光传播、液晶器件 |
| [聚合物与力学](solutions/polymers-mechanics/README.md) | 黏弹性、本构模型、相行为 |
| [材料计算](solutions/materials-simulation/README.md) | DFT、MD、材料性质与结构 |
| [机器学习与优化](solutions/ml-optimization/README.md) | 主动学习、逆向设计、多目标优化 |
| [科学证据与文献](solutions/scientific-evidence/README.md) | 文献证据核对、研究问题回答 |

## 首批候选题

以下中文为便于阅读的译名；题目正式标题、ID 与来源保存在 [catalog.json](catalog.json)。已根据公开题面重新按入门难度排序，详见 [选题清单与首题风险](docs/CHALLENGE-SHORTLIST.md)。这是选题审核，尚未完成计算或提交。

| 题目 | 分类 | 状态 |
|---|---|---|
| FRET 效率与寿命计算 | 液晶与光学 | 题包已下载，待开始 |
| 距离依赖的荧光猝灭拟合 | 液晶与光学 | 待开始 |
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
