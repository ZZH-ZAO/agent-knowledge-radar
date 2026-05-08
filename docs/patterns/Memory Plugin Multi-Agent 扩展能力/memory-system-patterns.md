# 通用问题：Memory System

## 1. 问题定义

Memory System 解决的不是“怎样把历史保存下来”，而是“什么信息值得留下、留下多久、什么时候还能信、什么时候应该失效，以及它该不该进入下一轮上下文”。

真正成熟的 Memory，不是存储功能，而是上下文治理协议。

## 2. 为什么普通做法不够

很多 Agent 项目都会很快碰到同一组问题：

- 历史越积越多，prompt 越来越脏
- 旧摘要过期了还在被继续引用
- 每轮都重复 read_file 或重复总结
- 用户当前请求反而被旧上下文淹没

这说明普通做法只解决了“留痕”，没有解决“治理”。

## 3. 典型方案结构

成熟 Memory System 通常至少要分清下面六件事：

```text
Scope
  -> Lifecycle
  -> Storage
  -> Retrieval
  -> Injection
  -> Freshness / Eviction
```

如果这六层不分开，系统很容易把“聊天记录、工作现场、长期知识”全混在一起。

## 4. 成熟系统通常怎么做

### 4.1 先按作用域拆层

真正有用的记忆，不应该全放在一个桶里。成熟系统会至少区分：

- session memory
- working memory
- project memory
- team memory
- durable memory

这一步的本质，是先问清楚“这条信息到底服务哪种未来任务”。

### 4.2 再按生命周期区分临时和长期

很多信息只对当前任务有用，不应该长期保留；另一些信息属于稳定约定，应该被提炼成 durable knowledge。

如果生命周期不明确，结果通常只有两种：

- 该忘的不忘
- 该留的不留

### 4.3 把 freshness 当成一等公民

这是 Memory 里最容易被忽略、但最关键的一层。真正危险的不是“忘记”，而是“自信地引用过期结论”。

成熟系统会给 file summary、task summary、知识条目补 freshness / invalidation 机制。文件变了、上下文变了、环境变了，旧摘要就应该自动失效。

### 4.4 召回不是越多越好，而是越准越好

真正好的 retrieval 不会把所有可能相关内容都塞回去，而是控制：

- 召回数量
- 每条记忆长度
- 任务相关度
- 注入顺序

Memory 的目标不是“模型知道更多”，而是“模型在当前任务里少走弯路”。

### 4.5 注入策略本身也是治理问题

同样一条 memory，不同任务该不该注入、放在 prompt 哪一段、占多少预算，都应该有明确策略。否则存得越多，污染越重。

## 5. 常见错误做法

### 5.1 把 memory 做成无差别追加日志

这会让记忆系统越来越像历史垃圾堆，而不是生产力资产。

### 5.2 只做召回，不做失效

这类系统短期看很“聪明”，长期最容易把旧结论继续当真。

### 5.3 把聊天历史误当长期知识

历史记录是证据，不等于结构化知识。没有提炼、分层和治理，长期看只会放大噪声。

## 6. 证据项目

### 6.1 zzh/pico

这是当前最强的本地证据项目之一。`memory.py` 和 `context_manager.py` 已经把：

- `task_summary`
- `recent_files`
- `file_summaries`
- `episodic_notes`
- `durable memory`
- freshness / invalidation

这些概念明确拆开了。

### 6.2 anthropics/claude-code

公开文档里 Memory 已经是正式产品能力，说明它不是“顺手做一个历史功能”，而是平台主线之一。

### 6.3 现有面经与知识库材料

你自己的材料里也已经反复出现了上下文膨胀、重复读取、长任务保持现场这些问题，这说明它不是单项目困扰，而是行业共性痛点。

## 7. Trade-off 与边界

### 7.1 记忆越结构化，维护成本越高

你需要额外定义 scope、freshness、retrieval、promotion 和 eviction。但如果不做这些，模型会把成本和错误在运行时成倍还回来。

### 7.2 并不是所有场景都需要重型 Memory

短单轮任务可以非常轻；但只要目标是长链路、跨文件、跨会话、可恢复任务，Memory 就必须进入正式结构。

## 8. 我的项目行动项

- [ ] 在平台项目页固定增加 `memory_scope / freshness_rule / retrieval_rule / injection_rule` 视角。
- [ ] 后续自动沉淀时优先抽取 summary invalidation、durable promotion、retrieval ranking 这几类强信号。
- [ ] 把 `pico` 的分层 memory 设计继续回写到痛点页和面试页，形成统一证据链。
- [ ] 让痛点页逐步展示 prompt 压缩率、重复读取次数、任务恢复成功率这类与 memory 直接相关的指标。

## 自动回写补充

<!-- AUTO-WRITEBACK:anthropics-claude-code-memory-system:START -->
### Anthropics/claude-code

- 命中原因：来自项目已有 relatedPatterns
- 来源项目：`anthropics-claude-code`
- 项目地址：https://github.com/anthropics/claude-code
- 草稿文件：`docs/external-projects/Claude Code ???????/anthropics-claude-code.md`

#### 新增证据项目

???????????????????????????????????????????????????????????????????????

#### 项目里的具体做法

Claude Code ?? terminal ??????????? settings?hooks?commands?MCP?subagents?skills ?????????????????????????????????????????????????

#### 对当前平台的直接启发

- ?????????? Tool Runtime?MCP Integration ? Productization ????
<!-- AUTO-WRITEBACK:anthropics-claude-code-memory-system:END -->
