# 💰 DCF 估值插件（Coze 自建）

> 两阶段自由现金流折现模型 + 3×3 敏感性矩阵。

**公式：** 企业价值 = Σ(FCFt/(1+r)^t) + 终值/(1+r)^n
**建议：** ≥20% 买入 · 10-20% 观望 · 0-10% 持有 · <0% 卖出
**参数：** symbol · years · growth_rate · perpetual_growth_rate · discount_rate · margin_of_safety

**测试（茅台）：** 每股价值 1,682.50 元 · 安全边际 +19.1% · 建议：观望
