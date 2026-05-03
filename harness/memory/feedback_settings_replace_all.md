---
name: settings-prefer-replace-all
description: settings.json 编辑偏好：使用 replace_all 避免重复确认
type: feedback
---

## 规则：Edit 工具使用 replace_all 参数

**Why:** Claude Code 的 Edit 工具默认需要每次确认，使用 `replace_all: true` 可批量替换所有匹配项，减少交互次数。

**How to apply:**
- 当需要全局替换某个字符串时，显式设置 `replace_all: true`
- 不要分散的多次 Edit，应该一次 replace_all 搞定

**示例:**
```python
Edit({
    "file_path": "config.json",
    "new_string": "\"debug\": true",
    "old_string": "\"debug\": false",
    "replace_all": true  # 全局替换，不逐个确认
})
```