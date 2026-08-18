#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新 index.html 中的过期时间戳
用法：python update_expire.py <新时间戳>
"""
import sys
import re
import os

INDEX_FILE = os.path.join(os.path.dirname(__file__), "index.html")


def update_expire(new_ts: int):
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # 匹配 var EXPIRE_TIMESTAMP = <数字>;
    pattern = re.compile(r"var EXPIRE_TIMESTAMP\s*=\s*\d+\s*;")
    if not pattern.search(content):
        print(f"❌ 在 {INDEX_FILE} 中找不到 EXPIRE_TIMESTAMP")
        sys.exit(1)

    new_content = pattern.sub(f"var EXPIRE_TIMESTAMP = {new_ts};", content)

    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"✅ 已更新 EXPIRE_TIMESTAMP = {new_ts}")
    print(f"   对应北京时间：{__import__('time').strftime('%Y-%m-%d %H:%M:%S', __import__('time').localtime(new_ts))}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python update_expire.py <新时间戳>")
        sys.exit(1)
    try:
        ts = int(sys.argv[1])
        update_expire(ts)
    except ValueError:
        print(f"❌ 无效时间戳：{sys.argv[1]}")
        sys.exit(1)