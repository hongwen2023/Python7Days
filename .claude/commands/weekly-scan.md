---
description: 手动生成本周 Claude Code 追踪周报（与定时任务共用同一套指令）
---

读取 `tracking/weekly-report-prompt.md` 并严格按其中的步骤执行，生成本周周报。

补充说明：
- 如果本周已存在周报文件，改为增量更新该文件而不是新建。
- $ARGUMENTS 如果非空，作为本次扫描的额外关注点（例如某个刚发布的功能名）。
