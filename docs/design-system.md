# 人格深潜 — 设计系统

> **适用范围**：仅 [`apps/personality/web`](../apps/personality/web) 人格深潜 **immersive** 体验。  
> 档案整页表单等 form 类 UI 不使用本设计系统。  
> 项目总架构见 [person-archive-engine.md](./person-archive-engine.md)。

> UI 不仅是皮肤，而是探索体验本身。

## 品牌

| 项 | 值 |
| --- | --- |
| 产品名 | 人格深潜 |
| 英文名 | Personality Dive / `renge-shenqian` |
| 气质 | 深空探索 — 神秘、沉浸、非评判 |
| 语气 | 第二人称「你」、观察式（「深潜记录显示…」），禁用「正确/错误」「高分/低分」「某某型人格」 |
| 副标题 | 「向意识深处，遇见真实的自己」 |

## 色彩

| Token | 十六进制 | 用途 |
| --- | --- | --- |
| `space-void` | `#050508` | 主背景 |
| `space-deep` | `#0a0e1a` | 卡片/浮层底 |
| `nebula-purple` | `#6b4ce6` @ 12% | 星云晕染 |
| `nebula-cyan` | `#3dd6d0` @ 8% | 次要光晕 |
| `star-dim` | `#8b9dc3` | 次要文案 |
| `star-bright` | `#e8edf7` | 主文案 |
| `accent-glow` | `#a78bfa` | 选中态、进度环 |
| `danger-soft` | `#f59e0b` | 错误提示（非错题） |

## 排版

- **标题**：Noto Serif SC / 思源宋体，`font-serif`
- **正文**：Inter / 系统无衬线，`font-sans`
- **题干**：`text-xl md:text-2xl leading-snug`，限制 2 行
- **选项**：`text-base`，单行优先

## 组件规范

### 圆角与阴影

- 卡片：`rounded-2xl`
- 选项：`rounded-xl`
- 玻璃态：`bg-space-deep/60 backdrop-blur-md border border-white/5`
- 选中阴影：`shadow-[0_0_24px_rgba(167,139,250,0.25)]`

### 布局

```
┌──────────────────────────┐
│ TopBar: 人格深潜 | 进度 | 静音 │ fixed, 透明
├──────────────────────────┤
│    ParticleBackground    │  z-0, 全屏
│  ┌──────────────────┐    │
│  │ PageTransition    │    │  z-10, max-w-lg mx-auto px-5
│  └──────────────────┘    │
└──────────────────────────┘
```

## 动效常量

```ts
pageEnter: { duration: 0.4, ease: [0.22, 1, 0.36, 1] }
optionSelect: { duration: 0.35 }
staggerChild: 0.2
disabledAfterSelectMs: 300
```

## 粒子参数

| 参数 | 桌面 | 移动 |
| --- | --- | --- |
| 数量 | 60 | 30 |
| 颜色 | `#8b9dc3`, `#a78bfa` 混色 | 同 |
| 速度 | 0.3 | 0.3 |
| 交互 | `repulse` 半径 80, 强度 2 | 关闭 |
| 降级 | `prefers-reduced-motion` → 静态星图 CSS | 同 |

## 音频

- 资源：`public/audio/ambient-space.mp3`（免版权氛围音）
- 进入后 2s fadeIn 至 0.25
- localStorage 键：`renge_shenqian_audio_muted`
- `prefers-reduced-motion` → 默认静音
- 切题/提交：无音效
