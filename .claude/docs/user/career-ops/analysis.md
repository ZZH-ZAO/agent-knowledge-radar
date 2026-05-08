# career-ops 深度分析

## 项目总述

- 项目名：career-ops
- 项目路径：`D:\career-ops`
- 文档类型：user
- 文档用途：给你自己学习和复盘时使用的完整讲解版

## 1. 先说结论：它不是通用 Agent 平台，而是垂直工作流系统

`D:\career-ops` 最值得先看清的一点，是它并不是在自己实现一个 Claude Code 那样的底层 Agent Runtime。

它更像是：

- 站在 Claude Code / OpenCode / 未来 Codex 这类宿主 Agent 之上
- 用一组模式文件、规则文件、本地脚本和数据文件
- 把“求职”这件事组织成一个可重复执行的 Agent 工作流

所以它的重点不是：

- 自己实现底层 query loop
- 自己实现通用 tool runtime
- 自己做平台级 memory runtime

它真正的重点是：

- 职业搜索工作流怎么拆
- 数据怎么落地
- 输出怎么标准化
- 用户个性化和系统升级怎么隔离
- 多 worker 怎么并行处理多个 job offers

换句话说，它不是“Agent 内核项目”，而是“Agent 应用系统项目”。

---

## 2. 它真正的中心是什么

如果用 Agent 架构的眼光看这个项目，很容易误判。

因为你会看到：

- `CLAUDE.md`
- `modes/*`
- `batch/batch-prompt.md`
- `batch-runner.sh`
- 一堆 `.mjs` 脚本

看起来像很多零散部件。

但它真正的中心其实很清楚：

> 它的中心是“职业搜索流水线”。

这条流水线大致是：

1. 用户给一个 JD 或 URL。
2. 系统抽取 JD。
3. 系统判断角色 archetype。
4. 系统做 A-F/G 评估。
5. 系统生成 report。
6. 系统生成定制 PDF。
7. 系统把结果记入 tracker。
8. 如果是 batch / pipeline 模式，就继续并行处理下一批。

也就是说，这不是聊天系统思维，而是业务流水线思维。

这很值得学，因为很多人做 Agent 时太容易只盯着“模型怎么回答”，却不盯着“整个业务流怎么闭环”。

---

## 3. Prompt 是它最强的工程资产之一

这个项目里的 prompt 设计非常成熟，但它的成熟方式和 Claude Code Sourcemap 不太一样。

Sourcemap 更像在教你：

- Prompt 怎样成为 runtime context system

而 `career-ops` 更像在教你：

- Prompt 怎样成为领域作业规范

你看这些文件就很明显：

- `CLAUDE.md`
- `modes/_shared.md`
- `modes/*.md`
- `batch/batch-prompt.md`

这里的 prompt 已经不只是“提示模型”，而是在做：

- 角色作业说明书
- 业务流程分解
- 工具使用规则
- 风险控制规则
- 写作风格约束
- 输出格式约束

尤其 `modes/_shared.md` 很像一个领域控制中枢：

- source of truth 在哪
- 评分维度是什么
- archetype 怎么判
- 哪些事绝对不能做
- 哪些工具该怎么用

这意味着它把 prompt 从“增强输出质量”推进成了“规范工作行为”。

这点非常值得以后做垂直 Agent 产品时学习。

---

## 4. Tool 不是它自己实现的，但工具治理意识很强

`career-ops` 不是底层 Agent runtime，所以它没有自己重新实现 Tool Runtime。

但它对工具的理解是成熟的，不是“反正能调就行”。

最明显的几个例子：

- `Playwright` 用于验证岗位是否真的 active
- `WebFetch` 只是 fallback
- `WebSearch` 用于 comp research、culture、contacts
- 明确规定：
  - 验证岗位状态时不能轻信 WebFetch / WebSearch，优先 Playwright
  - 绝不能 2+ agent 并行使用 Playwright

这说明作者理解了一个非常实际的问题：

> 工具之间不是平权的，它们的可信度、资源占用和场景适用性不同。

这和很多 demo 项目只是“有浏览器工具、有搜索工具”完全不是一个层次。

这个项目真正厉害的地方，是它开始把工具放进具体业务可信度链条里去理解。

---

## 5. Workflow 编排是这个项目最强的地方

如果让我选 `career-ops` 最值得学的一个部分，我会选 workflow orchestration。

因为它不是只做了一个“输入 -> 输出”的单次流程，而是围绕求职这个真实业务，把不同工作流都搭出来了：

- 单 offer evaluation
- auto-pipeline
- portal scan
- pipeline inbox
- batch parallel processing
- tracker merge
- follow-up cadence

这让系统从“一个 AI 助手”变成了“一个职业运营系统”。

尤其这几个文件很有代表性：

- `docs/ARCHITECTURE.md`
- `modes/pipeline.md`
- `batch/batch-runner.sh`
- `merge-tracker.mjs`
- `verify-pipeline.mjs`

它们一起说明了一件事：

> 真正有价值的 Agent 产品，很多时候不是靠底层模型花活，而是靠 workflow 是否把业务链条接住。

这对你以后看别的垂直 Agent 项目会很有帮助。

---

## 6. 它的“memory”更像文件型长期职业上下文

这个项目没有 Claude Code 那种正式的多层 memory runtime。

它没有明显的：

- extractMemories
- autoDream
- 多层 recall 机制

但它也不是没有 memory。

它采用的是一种更朴素、但对这个场景很合适的做法：

- `cv.md`
- `article-digest.md`
- `config/profile.yml`
- `modes/_profile.md`
- `interview-prep/story-bank.md`
- `data/applications.md`
- `data/follow-ups.md`

这些文件共同组成了一个稳定的长期职业上下文。

这类 memory 的好处是：

- 可读
- 可改
- 可检查
- 对高敏感个人数据更稳

在求职场景下，这种“文件型长期上下文”反而比太自动化的 memory 更可信。

所以这个项目在 memory 上最值得学的是：

> 不一定非要做 fancy memory runtime，先把长期业务上下文组织成稳定资产也很重要。

---

## 7. Multi-Agent 是务实的并行 worker，不是炫技型多 Agent

`career-ops` 有 multi-agent，但它的多 Agent 不是那种 coordinator/swarm/social agents 的方向。

它更像：

- 一个 batch orchestrator
- 多个 headless worker
- 每个 worker 用 self-contained prompt 干完整子任务

这在 `batch/batch-prompt.md` 和 `docs/ARCHITECTURE.md` 里非常明显。

它的多 Agent 设计是非常业务导向的：

- 一个 job offer 就是一份天然独立任务
- 所以最合理的拆法就是 worker 并行
- 不需要复杂 agent 社会结构
- 也不需要很重的 coordinator 心智模型

这点非常值得学，因为很多项目上 multi-agent 是为了看起来高级，而这里是因为业务天然适合并行。

这是“恰到好处的多 Agent”，不是“过度设计的多 Agent”。

---

## 8. 数据契约是它最工业化、最容易被忽略的亮点

如果说这个项目里哪一点最像成熟产品工程，而不是 prompt 工程，我会选 `DATA_CONTRACT.md`。

这个文件的价值非常高，因为它明确区分了：

- User Layer
- System Layer

也就是说，它把这些问题提前设计清楚了：

- 哪些文件是用户资产
- 哪些文件是系统逻辑
- 更新时哪些绝不能碰
- 个性化该写到哪一层

这点对 Agent 产品太重要了。

因为一旦系统会：

- 自动升级
- 自动改文件
- 持续沉淀用户资料

如果没有数据契约，很快就会出现：

- 用户自定义被系统更新覆盖
- 系统逻辑被个人偏好污染
- 可升级性和个性化互相冲突

`career-ops` 在这点上是非常成熟的。

这也是我认为它最值得其他垂直 Agent 产品复制的一点之一。

---

## 9. 它真正教会我们的，不是“怎么做通用 Agent”，而是“怎么做垂直 Agent 产品”

如果把这个项目的最大教学价值压缩成一句话，我会说：

> 它最值得学的，不是怎么做一个通用 Agent 平台，而是怎么站在现成 Agent 宿主上，把一个高价值垂直场景做成真正可执行的业务系统。

这背后有几条很重要的方法论：

- 不一定要自己造底层 runtime
- 先借宿主 Agent 的通用能力
- 把领域规则做深
- 把 workflow 做实
- 把数据契约做清楚
- 把个性化和可升级性分层
- 把人类在环写进系统边界

这套思路对很多未来垂直 Agent 产品都非常有参考价值。

---

## 10. 最后总结：这个项目最该学什么

如果你以后回头看这份分析，最值得记住的是下面这几点。

- `career-ops` 不是 Agent 内核，而是垂直 Agent 工作流系统。
- 它的中心不是通用 query loop，而是职业搜索流水线。
- 它把 prompt 做成了领域作业规范，这一点非常强。
- 它对工具可信度和并发约束有真实工程意识。
- 它的 workflow 编排是整套系统最强的地方。
- 它的 memory 虽然不 fancy，但非常适合求职场景。
- 它的多 Agent 设计务实、克制、非常贴业务。
- 它的数据契约设计非常成熟，尤其值得学。

一句话压缩就是：

> `career-ops` 证明了很多高价值 Agent 产品，并不需要先成为“通用 AI 平台”，而是可以先成为“借助宿主 Agent 执行能力的垂直业务操作系统”。
