#!/usr/bin/env python3
"""下载上游价格表，叠加 custom_models.json，写出价格 JSON 与 sha256。

输出 CHANGED=true|false 与 HASH=<sha256>，供工作流判断是否提交。
"""
import hashlib
import json
import os
import sys
import urllib.request

UPSTREAM_URL = "https://raw.githubusercontent.com/Wei-Shaw/model-price-repo/main/model_prices_and_context_window.json"
OUTPUT_FILE = "model_prices_and_context_window.json"
HASH_FILE = "model_prices_and_context_window.sha256"
CUSTOM_FILE = "custom_models.json"


def main() -> None:
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(root)

    with urllib.request.urlopen(UPSTREAM_URL, timeout=60) as resp:
        upstream = json.loads(resp.read().decode("utf-8"))
    if not isinstance(upstream, dict) or len(upstream) < 100:
        sys.exit(f"upstream looks broken: {type(upstream).__name__} with {len(upstream)} entries")

    with open(CUSTOM_FILE, encoding="utf-8") as f:
        custom = {k: v for k, v in json.load(f).items() if not k.startswith("_")}

    merged = dict(upstream)
    for name, pricing in custom.items():
        if name in upstream:
            print(f"NOTE: {name} 上游已有，使用本仓库定义覆盖")
        merged[name] = pricing

    body = (json.dumps(merged, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")
    digest = hashlib.sha256(body).hexdigest()

    old = ""
    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, encoding="utf-8") as f:
            old = f.read().strip()
    changed = digest != old
    if changed:
        with open(OUTPUT_FILE, "wb") as f:
            f.write(body)
        with open(HASH_FILE, "w", encoding="utf-8", newline="\n") as f:
            f.write(digest + "\n")

    print(f"upstream={len(upstream)} custom={len(custom)} merged={len(merged)}")
    print(f"CHANGED={'true' if changed else 'false'}")
    print(f"HASH={digest}")


if __name__ == "__main__":
    main()
