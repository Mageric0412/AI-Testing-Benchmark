# Design System — AI-Testing-Benchmark

## Product Context
- **What this is:** 云基础设施自动化评测平台，面向工程师的B2B技术工具
- **Who it's for:** 云架构师、DevOps工程师、SRE团队
- **Space/industry:** 云评估 / MLOps / DevOps 仪表板
- **Project type:** Web App (Gradio)

## Aesthetic Direction
- **Direction:** Brutally Minimal + Warm Neutrals
- **Decoration level:** Intentional — every decorative element earns its place
- **Mood:** 严谨、精确、有判断力 — 区别于冰冷企业蓝，传达"人为洞察"而非"机器生成"
- **Reference sites:** Datadog (冷静表面层次), Weights & Biases (结构化数据)

## Typography
- **Display/Hero:** Instrument Sans Bold — 几何无衬线，传达技术严谨感
- **Body:** DM Sans Regular — 高可读性，人文感
- **UI/Labels:** Same as body (DM Sans)
- **Data/Tables:** JetBrains Mono — 等宽字体，tabular-nums 确保数字对齐
- **Loading:** CDN — Google Fonts (Instrument Sans, DM Sans, JetBrains Mono)
- **Scale:**
  - Hero: 48px / 700 / letter-spacing -0.02em
  - H1: 32px / 700
  - H2: 24px / 600
  - H3: 18px / 600
  - Body: 16px / 400 / line-height 1.7
  - Caption: 12px / 400 / uppercase / letter-spacing 0.1em

## Color
- **Approach:** Warm Neutrals + Single Accent — 区别于竞品的企业蓝系
- **Primary:** #1a1a1a — 主文字、深色标题
- **Background:** #FAFAF8 — 暖白主背景
- **Surface:** #F0EFEB — 米灰卡片/容器背景
- **Surface Hover:** #E8E7E2 — 交互态
- **Border:** #D4D3CF — 分割线
- **Accent:** #E85D04 — 暖橙唯一强调色（CTA、关键数据）
- **Accent Hover:** #D45403 — 按钮悬停
- **Muted:** #6B6B6B — 次要文字
- **Semantic:**
  - Success: #2D6A4F (深绿)
  - Warning: #BC6C25 (赭色)
  - Error: #9B2226 (深红)
- **Dark mode:** 降低亮度，保持暖色调 — 文字 #E8E7E2，背景 #1a1a1a，Surface #2a2a2a

## Spacing
- **Base unit:** 4px
- **Density:** Comfortable — 评估工具需要可读性
- **Scale:** 2xs(2) xs(4) sm(8) md(16) lg(24) xl(32) 2xl(48) 3xl(64)

## Layout
- **Approach:** Grid-disciplined — 严格网格，数据驱动产品需要清晰节奏
- **Grid:** 12-column, max-width 1200px
- **Max content width:** 1200px (主内容), 680px (正文阅读宽度)
- **Border radius:** 分层 — sm:4px, md:8px, lg:12px (非统一泡泡半径)

## Motion
- **Approach:** Minimal-functional — 仅功能性过渡，评估工具不需要花哨动画
- **Easing:** ease-out (进入), ease-in (退出)
- **Duration:** fast(100ms), base(200ms) — 状态切换反馈
- **Rules:** 仅 transform/opacity 动画，避免 layout 属性

## Decisions Log
| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-04-03 | Initial design system created | Created by /design-consultation — Brutally Minimal + Warm Neutrals approach |
| 2026-04-03 | Single accent color (warm orange) | Differentiation from enterprise blue competitors |
| 2026-04-03 | Instrument Sans + JetBrains Mono | Technical precision without being generic |
