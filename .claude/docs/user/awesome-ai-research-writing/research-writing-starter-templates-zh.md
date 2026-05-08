# 科研写作调用话术模板库

## Summary

- Project name: research writing starter templates
- Source case: `D:\awesome-ai-research-writing`
- Document type: user
- Purpose: provide copyable starter wording so research-writing tasks can move from “know the route” to “start the task immediately”

## 这页解决什么问题

前面的速查表和路由器已经能回答：

- 这是什么类型的写作任务
- 更适合用 prompt 还是 skill
- 先准备哪些输入

但很多时候，真正卡住你的不是“知道该用什么”，而是：

- 第一条消息到底怎么说
- 要一次性交代哪些信息
- 怎么写才不会太空

这页就是为了解决这个问题。

## 最推荐先记住的 5 个模板

### 1. 英文摘要润色

适合：

- 已经有英文摘要
- 想更像顶会风格

```text
请帮我润色下面这段英文摘要，让它更像顶会论文风格。

目标会议：
当前最担心的问题：
希望保留的核心贡献句：

英文摘要：
<把你的摘要贴在这里>
```

### 2. 中文草稿转英文论文段落

适合：

- 先用中文想清楚了
- 现在要正式转成英文论文表达

```text
请把下面这段中文草稿改写成适合论文正文的英文段落。

目标会议：
是否保留 LaTeX 公式：是 / 否
语气要求：更学术 / 更简洁 / 更像 introduction / 更像 methods

中文草稿：
<把你的中文草稿贴在这里>
```

### 3. 从 repo 起草论文

适合：

- 已经有代码仓库和实验结果
- 想直接拉出论文骨架

```text
请基于这个 repo 帮我起草一篇论文。

repo 路径：
实验结果目录：
目标会议：
一句话核心贡献：
我希望先产出：论文骨架 / abstract / introduction / 全文初稿
```

### 4. Reviewer 视角挑刺

适合：

- 你想在投稿前先让系统“先打你一遍”

```text
请从 reviewer 视角审视下面这篇论文内容，并指出最关键的问题。

目标会议：
你要重点关注：贡献是否清楚 / 实验是否充分 / 逻辑是否成立 / 表达是否严谨

内容：
<贴摘要、章节或整篇 PDF 的文字内容>
```

### 5. 去 AI 味

适合：

- 逻辑已基本成型
- 但语言腔调太像模型生成

```text
请帮我去掉下面这段文字的 AI 味，让它更自然，但不要改变原意。

当前文本类型：LaTeX 英文 / Word 中文
我希望保留的语气：

文本：
<把内容贴在这里>
```

## 全量模板索引

你也可以直接通过脚本输出：

```powershell
python .\scripts\research_writing_starter.py
python .\scripts\research_writing_starter.py --scenario english-abstract-polish
```

当前支持这些场景：

- `english-abstract-polish`
- `zh-to-en-paper-paragraph`
- `logic-check`
- `reviewer-pass`
- `paper-from-repo`
- `template-setup`
- `related-work`
- `doc-coauthoring`
- `humanize`
- `word-docx`
- `figure-caption`

## 推荐使用顺序

如果你现在要真正开始一个科研写作任务，我建议这样用：

1. 先跑路由器，确认路线
2. 再从这页或脚本里复制最接近的模板
3. 最后把你已有材料填进去直接开工

对应命令：

```powershell
python .\scripts\research_writing_router.py --task "我要改英文摘要，让它更像顶会论文"
python .\scripts\research_writing_starter.py --scenario english-abstract-polish
```

## 对当前工作台的意义

这一步很重要，因为它把知识资产又往前推进了一层：

- 不是只有案例
- 不是只有分析
- 不是只有速查
- 而是已经能直接给出可复制调用入口

这会让这类知识仓库从“值得参考”变成“可以直接拿来用”。
