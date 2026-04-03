# CLAUDE.md — AI-Testing-Benchmark

## Project Overview
云基础设施自动化评测平台 (AI-Testing-Benchmark) — 面向工程师的B2B技术工具，基于 Gradio 构建。

## Tech Stack
- **Frontend:** Gradio 6.x
- **Backend:** Python
- **Charts:** Plotly (with Chinese labels)
- **File Processing:** pandas, openpyxl

## Key Files
- `app.py` — 主应用入口
- `DESIGN.md` — 设计系统文档

## Design System
Always read DESIGN.md before making any visual or UI decisions.
All font choices, colors, spacing, and aesthetic direction are defined there.
Do not deviate without explicit user approval.

## Gradio 6.x Notes
- `file_count="single"` (not `file_count=1`)
- `gr.Progress()` as default parameter, not type annotation
- Theme/CSS via `theme=` or `css=` in `launch()`
- Components must be defined before event handlers (UnboundLocalError fix)

## Chinese Localization
- Phase names mapped via `PHASE_NAME_MAPPING` dict
- Dropdown choices use tuple format: `(value, label)`
- Progress messages in Chinese
