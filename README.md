# model-price-repo

模型价格表 = 上游 [Wei-Shaw/model-price-repo](https://github.com/Wei-Shaw/model-price-repo) 的价格表 + 本仓库 `custom_models.json` 里的补充模型。

- GitHub Actions 每 15 分钟拉一次上游，叠加补充模型，内容有变化才提交
- 补充模型：编辑 `custom_models.json`（字段同上游表，单位美元/token），推送后工作流会立即重新生成
- 与上游同名时以 `custom_models.json` 为准；上游补上后可从本文件删掉
- 手动运行：`python3 scripts/merge.py`

sub2api 配置：

```yaml
pricing:
  remote_url: "https://raw.githubusercontent.com/ljh1595149587/model-price-repo/main/model_prices_and_context_window.json"
  hash_url: "https://raw.githubusercontent.com/ljh1595149587/model-price-repo/main/model_prices_and_context_window.sha256"
```
