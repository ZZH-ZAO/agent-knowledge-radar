# SDK 包装型 Agent Runtime 设计模板

## Summary

- Project name: sdk-wrapped-agent-runtime-template
- Project path: `D:\claude-code-sourcemap\.claude\docs\user`
- Document type: user
- Purpose: provide a reusable design template for teams building an application-level Agent runtime on top of an existing SDK, based on lessons from ArcReel and similar systems

## 一、什么叫“SDK 包装型 Agent runtime”

很多团队做 Agent 产品时，会直接把某个 SDK 接到前端：

- 用户发消息
- SDK 返回流
- 前端直接展示

这种做法在原型期很快，但产品期往往不够。

所谓“SDK 包装型 Agent runtime”，指的是：

> 在底层 Agent SDK 之上，再建立一层应用级运行时，把底层事件、会话和工具语义，转换成产品真正需要的状态系统和交互系统。

这类 runtime 通常会处理：

- session 生命周期
- reconnect
- interrupt
- snapshot
- pending question
- stream event -> UI patch/delta
- turn normalization

ArcReel 就是很典型的案例。

## 二、什么时候你需要这层包装

如果你满足下面几条中的几条，基本就需要：

- 你不是做一次性实验，而是在做产品
- 前端需要支持刷新恢复或断线重连
- 你不能只展示原始流，需要结构化展示
- 你要支持 interrupt、resume、question-answer
- 你要把聊天和项目/任务状态结合
- 你需要统一 turn schema 给前端渲染

反过来说：

- 如果你只是做 demo，直接接 SDK 也可以
- 但只要往产品走，这层包装几乎是迟早要补的

## 三、推荐的核心组件

### 1. Session Service

职责：

- 对外提供 create / send / interrupt / delete / list / snapshot

它是应用层真正的会话入口，不应该让前端直接操作底层 SDK client。

### 2. Session Manager

职责：

- 管理活跃连接
- 管理 running / idle / completed / error 等状态
- 管理 subscriber
- 管理 pending questions
- 管理 reconnect buffer

这是 runtime 的核心调度层。

### 3. Session Meta Store

职责：

- 把 session 元信息落到 DB

典型字段：

- session_id
- project_name
- title
- status
- created_at
- updated_at

### 4. Transcript Adapter

职责：

- 读取 SDK 自己的 transcript 或消息记录
- 转成应用层可继续处理的消息格式

这层很重要，因为 SDK 的 transcript 格式通常不等于产品前端需要的格式。

### 5. Stream Projector

职责：

- 把流式事件映射成：
  - snapshot
  - patch
  - delta
  - question

这是“原始 SDK 流”与“产品 UI 更新模型”之间的桥。

### 6. Turn Schema / Normalizer

职责：

- 把不同类型消息统一成前端可稳定消费的 turn 结构

例如把：

- user
- assistant
- result
- system
- tool_use
- tool_result
- thinking

都整理成统一内容块。

## 四、为什么 turn normalization 这么重要

因为如果没有它，前端会遇到几个问题：

- 不同消息类型格式不一致
- reconnect 后同一条消息可能重复或形态不同
- 流式 draft 和最终 turn 不容易合并
- UI 组件会充满类型分支和补丁逻辑

所以成熟系统通常要定义：

- Turn Contract
- Content Block Contract

这样前后端才有稳定接口。

## 五、一个典型的流式模型

建议把流式输出理解成三层：

### 1. Raw SDK stream

最底层原始事件。

### 2. Runtime event model

应用 runtime 处理后的事件，例如：

- runtime_status
- ask_user_question
- stream_event
- result

### 3. UI projection model

给前端的真正事件，例如：

- snapshot
- patch
- delta
- question
- status

为什么要这样分：

- 原始事件适合程序，不一定适合 UI
- UI 需要的是稳定可渲染模型，不是底层细节

## 六、reconnect / snapshot 应该怎么设计

这是 SDK 包装型 runtime 最重要的能力之一。

### 1. Snapshot

作用：

- 页面重载或重新进入时，前端能一次性拿到当前状态

典型内容：

- session_id
- status
- turns
- draft_turn
- pending_questions

### 2. Reconnect

作用：

- 流中断后可以恢复

关键点：

- 不只是重连 socket 或 SSE
- 还要让前端知道“现在已生成到哪里”

### 3. Buffer + transcript merge

作用：

- 把内存中的流式消息和持久化 transcript 合并
- 避免重复显示

这一步常常最难，但对产品体验至关重要。

## 七、interrupt / pending question 为什么要一开始就想清楚

### interrupt

如果系统支持长任务、复杂技能或需要用户打断，就必须设计 interrupt。

否则：

- 用户体验会很差
- 资源浪费
- 会话状态会变乱

### pending question

如果 Agent 在流程里要向用户追问，就不能只靠“输出一段文本再等用户猜”。

更好的方式是：

- 把问题结构化
- 让前端知道这是一个待回答问题
- 用户回答后再继续会话

这类设计能显著提升产品交互稳定性。

## 八、SDK 包装型 runtime 的常见坑

### 1. 直接把底层事件暴露给前端

坏处：

- UI 强耦合 SDK
- 以后换 SDK 很痛
- 前端逻辑会越来越脏

### 2. 不做 turn 归一化

坏处：

- 前端渲染复杂度失控

### 3. 只做 session，不做 project context

坏处：

- Agent 会话和产品状态脱节

### 4. 不处理 reconnect 与 replay

坏处：

- 一旦刷新页面，体验就断裂

### 5. 不做权限与工具边界控制

坏处：

- 底层 SDK 权限太大
- 产品安全边界模糊

## 九、一个可直接套用的设计清单

### A. 会话模型

- session 状态有哪些
- session 元数据存哪里
- 是否支持 snapshot
- 是否支持 reconnect

### B. 流式模型

- 原始事件有哪些
- 应用 runtime 事件有哪些
- 前端最终消费哪些事件

### C. Turn Contract

- turn 类型有哪些
- content block 类型有哪些
- tool_use / tool_result 怎么统一

### D. 用户交互

- 是否支持 pending question
- 是否支持 interrupt
- 是否支持 resume

### E. 安全与边界

- 工具权限怎么控制
- 文件访问怎么控制
- 运行时 prompt 怎样做 safety append

### F. 状态耦合

- Agent session 和 project state 怎么关联
- 哪些状态属于 chat
- 哪些状态属于 product

## 十、基于 ArcReel 得到的关键启发

最值得记住的是：

- 应用级 runtime 不是 SDK 的重复，而是产品语义层
- snapshot / projector / normalizer 这三件事是产品化关键
- project state 往往比纯 chat state 更重要
- pending question 和 interrupt 不是附加功能，而是工作流型 Agent 的基础设施

## 十一、最后一句话记忆

如果用一句话记住 SDK 包装型 Agent runtime，我建议记成这样：

> 真正的产品化 Agent runtime，不是直接把 SDK 接出去，而是把 SDK 转译成前端、工作流和系统状态都能稳定理解的应用级运行时。
