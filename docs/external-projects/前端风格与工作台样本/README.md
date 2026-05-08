# 前端风格与工作台样本

这里放适合当前知识平台借鉴的前端风格项目，重点不是营销官网，而是：

- 工作台布局。
- 后台管理界面。
- 高密度信息展示。
- 组件系统。
- 数据面板。
- UI blocks。
- 轻量动效。

## 当前优先样本

| 项目 | 类型 | 适合借鉴什么 | 对当前平台的价值 |
| --- | --- | --- | --- |
| [shadcn-ui/ui](https://github.com/shadcn-ui/ui) | 组件规范 / 代码分发 | 可复制组件、清晰 token、可访问性、组合式组件 | 适合作为按钮、表单、弹层、列表、命令面板的设计参考 |
| [Kiranism/next-shadcn-dashboard-starter](https://github.com/Kiranism/next-shadcn-dashboard-starter) | Shadcn 后台模板 | 侧栏、面包屑、表格、账号区、后台页面密度 | 适合参考“项目页 / 方案页”的工作台布局 |
| [Qualiora/shadboard](https://github.com/Qualiora/shadboard) | Next.js + Shadcn Dashboard | 可扩展后台模板、清晰页面骨架 | 适合参考路由页、详情页和状态组件 |
| [tremorlabs/tremor](https://github.com/tremorlabs/tremor) | 数据面板组件 | 指标卡、图表、数据展示、dashboard 气质 | 适合增强痛点页、雷达页、项目评分页 |
| [cruip/tailwind-dashboard-template](https://github.com/cruip/tailwind-dashboard-template) | Tailwind Dashboard | Mosaic Lite 后台页面结构、统计卡、列表 | 适合参考整体密度和列表/详情层级 |
| [ephraimduncan/blocks](https://github.com/ephraimduncan/blocks) | Shadcn UI Blocks | 可复用区块、页面组合方式 | 适合后续快速生成视觉方案页和面试官页 |
| [ibelick/motion-primitives](https://github.com/ibelick/motion-primitives) | 轻量动效组件 | 有节制的交互动效、hover/transition | 适合少量用于面试官训练卡片、切换反馈 |

## 选型结论

当前平台不适合照搬营销页，也不适合大面积炫酷动效。最适合的路线是：

```text
shadcn/ui 的组件清晰度
  + Shadcn Dashboard 的后台布局
  + Tremor 的数据面板表达
  + 少量 Motion Primitives 的交互反馈
```

也就是说，平台应该继续保持“中文知识工作台”的克制气质，但在以下位置升级：

- 项目列表：更清晰的状态、评分、类型分组。
- 项目详情：强化来源、证据、行动项。
- 方案页：更像方法库，而不是普通 markdown 预览。
- 痛点页：用数据面板表达严重程度、依据项目、解决动作。
- 雷达页：变成候选项目评分表，而不是普通列表。
- 视觉生成页：承接 `DESIGN.md -> mockup -> 实现 -> 截图对照`。

## 不建议照搬

- 不照搬 landing page hero。
- 不使用大面积渐变、玻璃拟态、装饰性背景。
- 不让动效抢占阅读注意力。
- 不为了组件库而引入复杂依赖，现阶段先借鉴结构和视觉规则。
