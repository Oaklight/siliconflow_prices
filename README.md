# siliconflow_prices

fetch siliconflow prices via api

```bash
SILICONFLOW_API_KEY="sk-xxxxx" python get_prices.py
python merge_prices.py
```

各取所需：

- 原件：`siliconflow_models.json` 来自 siliconflow 官方，api 为技术人员提供，后续可能有新的正式 api
- one-hub 适用：`oneapi_prices.json` \
  通过`运营 -> 模型价格 -> 更新价格`，填入 [`https://oaklight.github.io/siliconflow_prices/oneapi_prices.json`](https://oaklight.github.io/siliconflow_prices/oneapi_prices.json)，点击`获取数据`，按需选择`覆盖数据`或`仅添加新增` \
  已经包含MartialBE的价格表，但相左部分以我的为准

## 更新说明

从提交 6bcde110295e7d0a4bca69a0ec6c9381318f1e0d 之后的更新包括：

1. **手工设置的价格表**：新增了一个手工设置的价格表 `manual_prices.yaml`，其中包含多个供应商的手动设置价格。
2. **合并价格表**：新增了 `merge_prices.py` 脚本，用于合并上游的价格表。合并逻辑如下：
   - 以 siliconflow 自动查询的价格为更新
   - 手工价格作为主要价格（出现冲突时以手工表为准）
3. **GitHub Workflow**：配置了 GitHub Action `.github/workflows/run_get_prices.yml`，内容如下：
   - 每天 UTC 时间 00:00 执行，或者在 master 分支有推送时触发。
   - 运行 `get_prices.py` 和 `merge_prices.py` 脚本。
   - 自动提交并推送更新后的价格文件。

### 主要文件说明

- `get_prices.py`：获取 siliconflow 的价格并通过 API 保存到 `siliconflow_prices.json`。
- `merge_prices.py`：合并手工价格和上游价格，生成最终的 `oneapi_prices.json`。
- `manual_prices.yaml`：手工设置的价格表。
- `siliconflow_models.json`：原始的 siliconflow 模型数据。
- `oneapi_prices.json`：适用于 one-hub 的最终价格表。
