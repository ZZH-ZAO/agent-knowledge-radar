# 重构导向代码审查提示模板

## Summary

- Project name: refactoring-review-prompt-templates
- Project path: `D:\claude-code-sourcemap\.claude\docs\user\shared`
- Document type: user
- Purpose: provide reusable prompt templates for Claude Code, Codex, or similar coding agents to perform code review with a refactoring mindset

## 一、这份模板是拿来干什么的

这份模板不是教模型“怎么聊天更像专家”，而是让它在审代码时：

- 先识别坏味道
- 再解释维护成本
- 再提出小步重构动作
- 最后明确测试和风险

它特别适合下面几类场景：

- 审遗留代码
- 审 AI 生成代码
- 审一个正在改动的 PR
- 让 Agent 给出“先改哪几步”的重构建议

## 二、通用模板

适合：

- 想让 Agent 对一段代码做标准的重构导向审查

```text
请用“重构导向”的方式审查这段代码，不要只给笼统评价。

请按下面规则输出：
1. 先识别可能存在的坏味道，例如：long function、duplicated code、data clumps、feature envy、repeated switches、large class、message chains、data class、primitive obsession。
2. 每个问题都要说明它为什么会增加后续维护或扩展成本。
3. 每个问题优先给 1-3 个“小步、行为保持”的重构动作，不要一上来就建议重写。
4. 如果缺测试或存在高风险改动，请明确指出。
5. 如果某处只是风格问题而不是真正的重构问题，请直接说明，不要硬凑问题。

输出格式固定为：
- Likely smell
- Why it hurts
- Small next moves
- Risk / missing tests

请优先关注：可读性、可修改性、职责边界、重复逻辑、调用耦合、条件分支扩展成本。
```

## 三、遗留代码审查模板

适合：

- 一段老代码看起来能跑，但你想知道值不值得重构

```text
请把下面这段代码当成“遗留代码”来审查。

我不需要你先给大重构方案，而是请先回答：
1. 这段代码最像哪些坏味道？
2. 哪些问题是真正会拖慢未来改动的？
3. 哪些问题只是表面不优雅，但不值得立刻动？
4. 如果只允许做 3 个低风险改动，应该先做什么？

请遵守：
- 优先给小步重构建议
- 不要默认推翻重写
- 明确区分“结构问题”和“功能问题”
- 如果建议改结构，请说明需要补什么测试作为安全网

输出时请分成两部分：
第一部分：值得现在做的重构
第二部分：可以先忍受的问题
```

## 四、AI 生成代码审查模板

适合：

- 你怀疑代码“能跑，但结构虚胖”

```text
请从“AI 生成代码常见结构问题”的角度审查这段代码。

重点检查：
- 是否有重复逻辑但只是换了变量名
- 是否有过长函数把多个阶段混在一起
- 是否有过长参数列表或数据泥团
- 是否有过多临时变量掩盖真实意图
- 是否把业务概念都压成 primitive types
- 是否有 repeated switches / 大量条件分支导致扩展困难

请不要只说“代码可以优化”，而是按下面格式输出：
- Likely smell
- Evidence in code
- Why it hurts later
- Small next moves
- Risk / missing tests

如果你认为这段代码虽然像 AI 生成，但结构其实还行，也请明确说“没有明显重构问题”，不要硬找。
```

## 五、PR 审查模板

适合：

- 你在看一个具体改动，想让 Agent 用更工程化的方式给 review 意见

```text
请把这次改动当成一个 PR 来做重构导向 review。

不要只看“能不能工作”，还要看这次改动是否引入了新的结构债务。

请重点回答：
1. 这次改动有没有引入新的坏味道？
2. 这次改动有没有放大已有坏味道？
3. 哪些地方现在不改，未来会变成更难动的结构债？
4. 有没有一个更小步、更稳的改法？

输出格式：
- Finding
- Likely smell
- Why it matters for future changes
- Suggested small-step refactor
- Test / safety note

请把问题按严重程度排序。
```

## 六、要求 Agent 给“分步重构路线”时的模板

适合：

- 你已经知道代码有问题，但不想直接大改

```text
这段代码我怀疑需要重构，但我不想要“大改造方案”。

请你给我一个“最多 5 步的小步重构路线”，要求：
- 每一步都尽量行为保持
- 每一步都尽量可以单独提交
- 每一步都说明预期收益
- 如果某一步前必须补测试，要明确写出

每一步请写成：
1. Step
2. Why now
3. Expected improvement
4. Safety requirement

如果你判断这段代码不适合小步重构，也请说明为什么。
```

## 七、要求 Agent 区分“重构”与“重写”时的模板

适合：

- 你感觉团队很容易动不动就建议重写

```text
请帮我判断：下面这段代码的问题，更适合“渐进式重构”还是“较大规模重写”？

请不要只给结论，要明确说明：
- 当前行为是否基本可信
- 是否能拆成小步行为保持修改
- 是否存在足够测试或可补的 characterization tests
- 哪些依赖关系会阻碍小步重构

最后请给出：
- Recommended path: Refactor / Rewrite / Mixed
- Why
- Smallest safe next step
```

## 八、如果你想让 Agent 说得更像成熟 reviewer，可以补上的约束

你可以在任何模板末尾追加下面这段：

```text
请避免下面这些低质量表述：
- “代码不优雅”
- “建议优化一下”
- “最好重构”
- “建议重写”

请改为：
- 明确命名坏味道
- 明确说明维护成本
- 明确给出小步动作
- 明确指出测试与风险
```

## 九、推荐搭配方式

最推荐的组合是：

- 方法理解：`refactoring-2nd-edition-notes.md`
- 速查映射：`refactoring-smell-to-action-cheatsheet.md`
- Agent 检索卡：`refactoring-review-playbook.md`
- 直接可用提示：这份 `refactoring-review-prompt-templates.md`

## 十、一句话记忆

如果把这份模板压成一句话，我会这样记：

> 让 Agent 审代码时，别只说“这里不太好”，而是先命名坏味道，再给小步重构动作，再交代测试和风险。  
