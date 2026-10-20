# 从简单开始的选题清单

筛查日期：2026-10-20（Asia/Shanghai）。来源：本次 Playground CLI 返回的 6,926 条目录，以及 10 道候选题的公开题面和元数据。未读取 hidden tests、checker 或官方 solution；未运行解题计算或提交评分。

依据：已确认方向为液晶弹性体 LCE 光致发光；能读一些 Python、需要项目带学，默认 CPU 起步。以下难度与学习用时是根据公开任务要求做的估计，不是实测耗时、平台承诺或已掌握证据。FRET 示例的生物体系只用于学习光物理计算，不能直接当作用户 LCE 的发光机制。

## 建议顺序

| 顺序 | 题目 | 实际任务与交付 | 入门判断 |
|---|---|---|---|
| 1 | [FRET 效率与寿命计算](https://play.bohrium.com/challenge/f-rster-resonance-energy-transfer-efficiency-calcu-4fff2cf6) | 已给距离与寿命，代入公式；输出 efficiencies.json 和逐步推导 efficiency_derivation.txt | 最简单；Python 标准库即可，无数据下载、训练或 GPU。适合先用 20–40 分钟熟悉公式、单位和文件契约 |
| 2 | [距离依赖的荧光猝灭拟合](https://play.bohrium.com/challenge/distance-dependent-fluorescence-quenching-model-fi-536026a1) | 4 组给定实验点，拟合两个参数并预测；输出 fitted_params.json、predicted_quenching.csv | 简单；NumPy/SciPy，本地 CPU。练习非线性最小二乘、残差与模型解释，初次带做约 1–2 小时 |
| 3 | [FRET 相对荧光产率计算](https://play.bohrium.com/challenge/fret-relative-fluorescence-yield-calculation-53a91b6e) | 7 个浓度的公式求值，特征浓度与距离互验；输出 theoretical_yields.csv、c0_validation.json | 简单至中等；误差函数与单位换算，初次带做约 1–2 小时。相对荧光产率不是实验 PLQY |
| 4 | [聚合物溶液旋节温度与 UCST 临界点](https://play.bohrium.com/challenge/compute-spinodal-temperatures-and-ucst-critical-mi-628b34e4) | 给定参数，推导多分散模型的旋节/临界条件，求根与极值；输出含 4 个标量的 JSON | 中等；CPU 足够，但需要热力学导数、分支判断和求解验证，建议在前 3 题后安排半天至一天 |
| 5 | [聚合物单轴黏弹性响应](https://play.bohrium.com/challenge/uniaxial-viscoelastic-polymer-response-simulation-00c4363d) | 标量内部变量 ODE，3 组应力松弛加 20 周期加载；输出两份力–时间 CSV | 中等；学习价值高，需补伸长比、加载历史、力与应力单位。PA6 模型不等于 LCE 本构，建议留 1–2 天 |
| 6 | [胆甾相液晶光场与能量积累](https://play.bohrium.com/challenge/electromagnetic-field-profile-and-energy-accumulat-f506322a) | 波数求解、复振幅边界匹配、空间/波长积分；输出两份 CSV | 进阶；最贴近 CLC 光学，但有偏振、归一化、共振数值稳定性等要求，建议留到线性代数与积分练习之后 |

前 3 道题面已给出所需数值/公式，平台数据集声明均为空。该判断表示题面自包含，不代表已经证明答案或验证了全部环境。后续模拟题的实际耗时取决于精度和实现。

## 首题目标与风险

首选 ID：`f-rster-resonance-energy-transfer-efficiency-calcu-4fff2cf6`。

- 输入：r=41 Å，两个 R0 分别为 47 Å 和 42 Å；供体寿命 1.64 ns，观测短寿命分量 0.44 ns。
- 计算：E=1/(1+(r/R0)^6)；两组效率差乘 100；预期寿命为 1.64×(1−E_EBFP)。
- 输出：efficiencies.json 的 5 个数值字段，以及包含公式、代入值和中间步骤的 efficiency_derivation.txt。
- 单位风险：字段 relative_increase 实际按题面计算**百分点差**，不能改为相对增长百分比；expected_lifetime_shortening 按给定公式写预期缩短后的寿命，不能写寿命差值。
- 来源边界：0.44 ns 是题面提供的观测常数，不能声称由本次计算预测。
- 验证：独立手算/高精度数值复核、0<E<1、寿命关系、JSON 数值类型与字段、文本中间过程完整性。均尚未执行。

题包已下载到 `asc-work/<首题ID>/task/`。当前 CLI 实际生成 `task.md`、challenge.json 和 config.json；**没有 instruction.md**，后续应读取 task.md，不自行假设文件名。

## 暂不作为起步题

- **液晶盒填充时间**：需要各向异性迁移率、二维压力方程和移动自由界面，并重复多组参数扫描；比标题暗示的单个时间公式困难。
- **液晶相位光栅最小周期**：输出虽仅少数标量，前置工作是二维 Frank–Oseen 取向求解和光学积分，另需原始模拟数据作为过程证据。
- **聚合物晶体层片厚度**：三种模型、无穷区间积分、分段积分核和发散处理，需补齐论文中的模型表达式。
- **多溶剂 FRET 距离与各向异性**：涉及多指数寿命、光谱重叠、旋转扩散和 UFF 建模，不能按普通公式代入题估计工作量。

## 评分状态核实

本次查看的 10 道题均显示 open，但 API scoring.strategy 都是 human_review_only，而题面描述了隐藏验证。这是公开信息之间的不一致。选题可按数学与交付复杂度推进；实际提交前重新核对评分契约或向赛事方确认，不能承诺自动评分或满分。open 也不能证明某轮赛事仍在计分期。

后续按项目约定在方案审核和提交前使用 grill-me。当前仅完成筛选与首题建档，学习进度、计算验证、平台成绩均未据此提升。
