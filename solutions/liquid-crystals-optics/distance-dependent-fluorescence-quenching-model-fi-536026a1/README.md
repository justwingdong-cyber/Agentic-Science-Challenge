# 距离依赖的荧光猝灭拟合

状态：本地独立验证通过，已提交（attempt 57967），等待评分。来源：[Playground 公开题目](https://play.bohrium.com/challenge/distance-dependent-fluorescence-quenching-model-fi-536026a1)，核对日期 2026-10-20。数据仅为题面给出的 4 个距离–猝灭百分数对，不含第三方题包、隐藏测试或官方解答。

## 方法与结果

拟合 `Q(d)=100/(1+a*d^n)`，最小化原始百分数尺度上的等权残差平方和。使用 `log(d0), n` 参数化、解析雅可比和 16 组初值，以避免直接优化很小的 a 导致尺度问题；最后换算 `a=exp(-n*log(d0))`。对数线性化不是最终拟合目标。

| 参数/指标 | 结果 |
|---|---:|
| a（nm^(-n)） | 5.149908937704438e-6 |
| n | 3.535987143073265 |
| d0（nm） | 31.299488428487397 |
| SSE（百分点平方） | 19.594415252318374 |
| RMSE（百分点） | 2.21327897317071 |

| d（nm） | 观测（%） | 预测（%） |
|---|---:|---:|
| 9.4 | 94.7 | 98.59835892729573 |
| 18.9 | 85.3 | 85.61522479945567 |
| 27.5 | 62.9 | 61.24476239462269 |
| 35.0 | 39.0 | 40.248212610833974 |

## 复跑

本机验证环境：Windows、Python 3.13.13、NumPy 2.5.4、SciPy 1.18.1。在本题目录执行：

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r scripts/requirements.txt
.venv\Scripts\python.exe scripts/run.py
.venv\Scripts\python.exe scripts/host_independent_check.py
```

`run.py` 两次执行求解器、比较输出哈希，再运行独立核验；唯一为干净目录复跑增加的操作是创建 logs/。最终答案仅为 outputs/fitted_params.json 与 outputs/predicted_quenching.csv，诊断留在忽略的 logs/。

## 验证与局限

- 不导入求解器的独立核验使用另一参数化与 Nelder–Mead、多初值、驻点和 Hessian 检查；同时验证 CSV 从参数复算、正参数、递减性和 Q(d0)=50。
- 外层使用 3 个固定种子的差分进化搜索再精化，在 d0∈[1,100] nm、n∈[0.1,20] 范围内得到相同 SSE；这不是无界全局最优的数学证明。
- 两次重跑输出字节一致，干净目录的公开脚本副本也已实际运行通过。
- n≈3.536 更接近 4 而非 6，但 4 个观测、缺少误差条与重复测量，不能据此确定 NSET 机理。短距离点仍偏差约 3.90 个百分点，不能隐藏该偏差。
- 题面自动验证描述与 API human_review_only 不一致，平台成绩未知。真实原生轨迹在私有题目工作区，格式检查通过，不公开完整会话。

优化接口参考：[SciPy least_squares 官方文档](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.least_squares.html)。本目录原创脚本和说明沿用仓库 MIT 许可；数据事实来自上述公开题面。
