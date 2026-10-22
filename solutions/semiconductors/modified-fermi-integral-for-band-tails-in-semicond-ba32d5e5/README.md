# 半导体带尾的修正费米积分

原创计算与中文解读；不包含下载题包、隐藏评测材料、原生会话或私人日志。

来源：https://play.bohrium.com/challenge/modified-fermi-integral-for-band-tails-in-semicond-ba32d5e5

## 复跑
Python 3.13.13、SciPy 1.18.1。进入本目录后：

```powershell
python -m venv .venv
.venv/Scripts/python -m pip install -r scripts/requirements.txt
New-Item -ItemType Directory -Force logs
.venv/Scripts/python scripts/solve.py
```

## 方法与结果
计算态密度与费米占据概率的乘积积分。eta=-4至4、间隔0.5；带尾参数0、1、10，共51个唯一组合。零带尾使用独立分支；expit避免指数溢出；无限区间使用自适应积分。

eta=0时，无带尾结果0.7651470246254081，强带尾结果43.46355463452506，比值56.80418695453132。它们是无量纲积分，不是实际载流子浓度。

独立变量变换积分最大绝对差3.4639e-14；解析校验点、两类单调性、有限正值与JSON结构检查均通过。公开目录独立复跑后输出与工作区字节一致。验证适用于给定数学模型，不构成实验材料验证或平台评分。

## 审核及提交
已按项目 grill-me 流程检查交付范围、数值验证、真实轨迹、复现和公开内容；没有新增未决的用户决策。真实原生解题会话片段已通过平台轨迹校验，未放入公开目录。

提交编号：59201；模型 gpt-6.1-sol，harness codex。提交已受理，最终分数未知。待评分不得解读为零分。
