import type { EngineeringLogic, PainPoint, Project, SearchItem, Solution, SourceItem } from '../types';
import type { ReaderDocument, ReaderKind, ReaderTarget } from '../constants';

export function buildProjectPressurePrompt(project: Project) {
  return `如果你把 ${project.name} 放进学习样本里，继续追问通常会落到三个问题上：它真正解决了什么工程边界、为什么这个做法值得迁移、以及它对你当前平台的下一步设计到底有什么启发。`;
}

export function buildProjectTakeaway(project: Project) {
  if (project.relatedPatterns.length) {
    return `${project.name} 最值得学的不是功能数量，而是它如何把 ${project.relatedPatterns.slice(0, 2).join(' / ')} 这些问题落成可执行的工程做法。继续往下读时，要重点看它的边界判断、证据链和可迁移动作。`;
  }
  return `${project.name} 最值得学的不是表面功能，而是它到底把哪个真实工程问题做成了可迁移样本。继续看时，优先追问它解决了什么边界问题、留下了什么证据、对当前平台有什么行动启发。`;
}

export function buildProjectMisreadWarning(project: Project) {
  if (project.primaryCategory === 'Agent Runtime') {
    return `最容易把 ${project.name} 误读成"又一个会调模型的工具"。真正该看的是它有没有把运行边界、恢复协议、工具副作用和上下文治理做成正式结构。`;
  }
  if (project.primaryCategory === 'Frontend Design' || project.primaryCategory === 'Workbench UI') {
    return `最容易把 ${project.name} 误读成"风格不错的页面样本"。真正该看的是它如何把设计约束、信息密度和阅读路径固化成可复用规则。`;
  }
  if (project.primaryCategory === 'MCP' || project.primaryCategory === 'Tool Runtime') {
    return `最容易把 ${project.name} 误读成"接了更多工具"。真正该看的是它怎么处理权限、结果治理、可追踪性和失败恢复。`;
  }
  return `最容易的误区是只看功能表面，不看它为什么这样拆、代价是什么、哪些做法其实并不适合直接照搬。`;
}

export function buildProjectOralAnswer(project: Project) {
  return `如果面试里要用一句比较顺的口语去讲 ${project.name}，我会先把它定义成一个${project.primaryCategory}样本，然后重点说它不是表面功能多，而是它把 ${project.businessScenario} 这类场景里的关键边界收进了正式工程结构。`;
}

export function buildProjectEngineeringPitch(project: Project) {
  return `如果用三分钟讲工程，我会先讲 ${project.name} 解决的真实场景，再讲它最值钱的亮点是 ${project.biggestHighlight}，然后落到它怎样把运行边界、证据链和后续行动项组织起来。这样讲不会停留在功能介绍，而会更像真实项目复盘。`;
}

export function escapeRegExp(value: string) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

export function extractMarkdownSection(content: string, headings: string[]) {
  for (const heading of headings) {
    const pattern = new RegExp(`^##\\s+\\d*\\.?\\s*${escapeRegExp(heading)}\\s*$`, 'm');
    const match = content.match(pattern);
    if (!match || match.index === undefined) continue;
    const start = match.index + match[0].length;
    const rest = content.slice(start);
    const nextMatch = rest.match(/^##\s+/m);
    const end = nextMatch && nextMatch.index !== undefined ? start + nextMatch.index : content.length;
    const value = content.slice(start, end).trim();
    if (value) return value;
  }
  return '';
}

export function buildProjectDeepDiveMarkdown(project: Project) {
  const scenario = project.scenarioSection || extractMarkdownSection(project.content, ['核心场景', '核心使用场景']);
  const problems = project.problemSection || extractMarkdownSection(project.content, ['它解决的通用问题', '通用问题']);
  const solutions = project.solutionSection || extractMarkdownSection(project.content, ['这个项目具体怎么做', '优秀技术和框架', '技术和框架']);
  const frameworks = project.frameworkSection || extractMarkdownSection(project.content, ['优秀技术和框架', '技术和框架']);
  const principles = project.principleSection || extractMarkdownSection(project.content, ['可迁移设计原则', '设计原则']);
  const actions = project.actionSection || extractMarkdownSection(project.content, ['对我当前项目的行动项', '对当前知识平台的行动项', '当前项目行动项']);
  const tradeoffs = project.tradeoffSection || extractMarkdownSection(project.content, ['Trade-off 与边界', 'Trade-off', '代价和边界', '边界']);

  const blocks = [
    scenario ? `## 1. 核心场景\n\n${scenario}` : '',
    problems ? `## 2. 它解决的通用问题\n\n${problems}` : '',
    solutions ? `## 3. 这个项目具体怎么做\n\n${solutions}` : '',
    frameworks ? `## 4. 优秀技术和框架\n\n${frameworks}` : '',
    tradeoffs ? `## 5. Trade-off 与边界\n\n${tradeoffs}` : '',
    principles ? `## 6. 可迁移设计原则\n\n${principles}` : '',
    actions ? `## 7. 对当前项目的行动项\n\n${actions}` : '',
  ].filter(Boolean);

  return blocks.join('\n\n') || `## 深度拆解待补充\n\n当前项目的正文结构还没有被完整沉淀，后续需要补齐"通用问题、具体做法、步骤和行动项"。`;
}

export function buildSolutionDeepDiveMarkdown(solution: Solution) {
  const structure = solution.structureSection || extractMarkdownSection(solution.content, ['典型方案结构', '方案结构']);
  const practice = solution.practiceSection || extractMarkdownSection(solution.content, ['成熟系统通常怎么做', '常见步骤', '成熟做法']);
  const mistakes = solution.mistakeSection || extractMarkdownSection(solution.content, ['常见错误做法', '常见误区']);
  const actions = solution.actionSection || extractMarkdownSection(solution.content, ['我的项目行动项', '当前项目行动项', '当前行动项', '我应该怎么做']);

  const blocks = [
    solution.problemDefinition ? `## 1. 问题定义\n\n${solution.problemDefinition}` : '',
    solution.whyImportant.length ? `## 2. 为什么重要\n\n${solution.whyImportant.map((item) => `- ${item}`).join('\n')}` : '',
    structure ? `## 3. 典型方案结构\n\n${structure}` : '',
    practice ? `## 4. 成熟系统通常怎么做\n\n${practice}` : '',
    mistakes ? `## 5. 常见误区\n\n${mistakes}` : '',
    actions ? `## 6. 当前行动项\n\n${actions}` : '',
  ].filter(Boolean);

  return (
    blocks.join('\n\n') ||
    `## 深度拆解待补充\n\n当前方案还缺少"典型结构、成熟做法、误区和行动项"的完整正文，后续需要优先补齐。`
  );
}

export function buildSolutionPressurePrompt(_solution: Solution) {
  return `继续追问时，真正的问题通常不是"这个方案是什么"，而是"为什么普通做法不够、它适合什么边界、代价又是什么"。`;
}

export function buildSolutionTakeaway(solution: Solution) {
  if (solution.maturePractices.length) {
    return `${solution.title} 这页最该带走的不是术语，而是成熟系统通常会用哪些固定机制来稳定解决这类问题。`;
  }
  return `${solution.title} 这页最该带走的是：先定义通用问题，再决定方案，而不是先堆实现名词。`;
}

export function buildPainPointPressurePrompt(painPoint: PainPoint) {
  return `继续追问 ${painPoint.title} 时，真正的问题通常不是"这个痛点是什么"，而是"为什么反复发生、优质项目怎么处理、共性做法是什么"。`;
}

export function buildPainPointTakeaway(painPoint: PainPoint) {
  return `${painPoint.title} 最该带走的是：先定义行业共性问题，再看证据项目怎么解决，最后落到可执行行动项。`;
}

export function buildPainPointDeepDiveMarkdown(painPoint: PainPoint, projects: Project[]) {
  return painPoint.content?.trim() || buildPainPointDocument(painPoint, projects);
}

export function buildPainPointDocument(painPoint: PainPoint, projects: Project[]) {
  const projectMap = new Map(projects.map((project) => [project.id, project]));
  const evidenceProjects = painPoint.evidenceProjects.map((id) => projectMap.get(id)).filter((project): project is Project => Boolean(project));
  const relatedProjects = projects.filter((project) => project.types.some((type) => type.toLowerCase().includes(painPoint.topic.toLowerCase().split(' ')[0] || '')));
  const practices = evidenceProjects.length ? evidenceProjects : relatedProjects.slice(0, 3);
  const commonPractices = painPoint.commonPractices ?? painPoint.maturePractices ?? [];
  const evidenceCount = painPoint.evidenceProjectCount ?? evidenceProjects.length;
  const lastUpdatedFromProjects = (painPoint.lastUpdatedFromProjects ?? []).map((id) => projectMap.get(id)?.name || id).filter(Boolean);
  const lineBreak = String.fromCharCode(10);
  const doubleLineBreak = lineBreak + lineBreak;
  const metricLines = [
    `总项目数：${projects.length} 个`,
    `证据项目：${evidenceCount} 个`,
    `相关项目：${relatedProjects.length} 个`,
    `来源类型：${(painPoint.evidenceSources ?? []).join(' / ') || '待补充'}`,
    `成熟做法：${commonPractices.length} 条`,
    `常见误区：${painPoint.commonMistakes.length} 条`,
    `行动项：${painPoint.actions.length} 条`,
    `最近更新项目：${lastUpdatedFromProjects.join(' / ') || '待更新'}`,
    `最近更新时间：${painPoint.lastUpdatedAt || '待更新'}`,
  ];

  return `# 行业痛点：${painPoint.title}

> 本页从多个优质项目、博客、论文和旧文档中提炼出该痛点的行业现象、证据项目、成熟做法与当前行动项。

## 1. 行业共性问题定义

${painPoint.industryPain || painPoint.solutionMethod}

这个痛点不是单个项目的功能缺口，而是从多个来源里反复出现的结构性问题。平台的目标是搜索优质资料，研究它们如何解决这些问题，再提炼共性做法，反哺当前项目。

## 2. 当前知识库证据统计

${metricLines.map((item) => `- ${item}`).join(lineBreak)}

## 3. 为什么这个问题重要

${painPoint.solutionMethod}

## 4. 证据项目与优秀做法

${practices.length ? practices.map((project) => `### ${project.name}

- 主分类：${project.primaryCategory}
- 类型标签：${project.types.join(' / ')}
- 沉淀状态：${project.status}
- 评分：${project.score ?? '暂无'}
- 一句话总结：${project.summary || '该项目正在沉淀中，后续补充核心判断。'}
- 关联方案：${project.relatedPatterns.length ? project.relatedPatterns.join('、') : '暂无'}
- 该项目之所以成为本痛点的证据，是因为它在 ${painPoint.topic} 领域提供了可验证的工程做法。`).join(doubleLineBreak) : '暂无直接证据项目，后续需要补充 GitHub、博客或论文来源。'}

## 5. 共性成熟做法

${commonPractices.length ? commonPractices.map((item) => `- ${item}`).join(lineBreak) : '- 暂无成熟做法，后续需要从 GitHub 项目、博客和论文中提取。'}

## 6. 数据支撑与判断信号

${(painPoint.dataSignals ?? []).length ? painPoint.dataSignals!.map((item) => `- ${item}`).join(lineBreak) : '- 暂无数据信号，后续需要补充可量化的判断指标。'}

## 7. 常见错误做法

${painPoint.commonMistakes.length ? painPoint.commonMistakes.map((item) => `- ${item}`).join(lineBreak) : '- 暂无常见误区'}

## 8. 对当前平台的启发

- 这个痛点应该反哺当前知识平台的项目页、方案页和痛点页。
- 后续新增相关资料时，应自动检查是否能补强本痛点的证据链。
- 平台应该让每个痛点都能回答"为什么反复发生"和"优质项目怎么处理"。

## 9. 演化规律

${painPoint.evolutionRule || '本痛点的演化规律待补充，后续需要观察行业趋势和新项目做法。'}

## 10. 当前项目行动项

${painPoint.actions.length ? painPoint.actions.map((item) => `- [ ] ${item}`).join(lineBreak) : '- [ ] 待补充行动项'}
`;
}

export function buildReaderDocument(
  target: ReaderTarget | null,
  projects: Project[],
  solutions: Solution[],
  painPoints: PainPoint[],
  sources: SourceItem[],
  engineeringLogic: EngineeringLogic,
): ReaderDocument | null {
  if (!target) return null;
  switch (target.kind) {
    case 'project': {
      const project = projects.find((item) => item.id === target.id);
      if (!project) return null;
      return {
        kind: 'project',
        id: project.id,
        title: project.name,
        eyebrow: '项目全文阅读',
        summary: project.oneLineVerdict || project.summary,
        sourceFile: project.sourceFile,
        content: project.content,
        badges: [project.primaryCategory, project.status, ...(project.types.slice(0, 3) || [])],
        quickFacts: [
          { label: '主分类', value: project.primaryCategory },
          { label: '业务场景', value: project.businessScenario },
          { label: '最大亮点', value: project.biggestHighlight },
          { label: '评分', value: project.score ? String(project.score) : '暂无' },
        ],
        guideCards: [
          { title: '为什么现在读', body: project.whyReadNow || buildProjectTakeaway(project) },
          { title: '最容易误读什么', body: buildProjectMisreadWarning(project) },
          { title: '最容易追问什么', body: buildProjectPressurePrompt(project) },
          { title: '口语版回答', body: project.oralAnswer || buildProjectOralAnswer(project) },
        ],
        actionItems: project.nextActions,
      };
    }
    case 'solution': {
      const solution = solutions.find((item) => item.id === target.id);
      if (!solution) return null;
      return {
        kind: 'solution',
        id: solution.id,
        title: solution.title,
        eyebrow: '方案全文阅读',
        summary: solution.problemDefinition,
        sourceFile: solution.sourceFile,
        content: buildSolutionDeepDiveMarkdown(solution),
        badges: ['方案方法库', ...(solution.maturePractices.slice(0, 3) || [])],
        quickFacts: [
          { label: '问题定义', value: solution.problemDefinition || '暂无' },
          { label: '成熟做法', value: String(solution.maturePractices.length) },
          { label: '常见误区', value: String(solution.commonMistakes.length) },
          { label: '行动项', value: String(solution.actions.length) },
        ],
        guideCards: [
          { title: '为什么重要', body: solution.whyImportant.join('；') || '暂无' },
          { title: '常见误区', body: solution.commonMistakes.join('；') || '暂无' },
          { title: '成熟做法', body: solution.maturePractices.join('；') || '暂无' },
          { title: '继续追问', body: buildSolutionPressurePrompt(solution) },
        ],
        actionItems: solution.actions,
      };
    }
    case 'pain-point': {
      const painPoint = painPoints.find((item) => item.id === target.id);
      if (!painPoint) return null;
      const commonPractices = painPoint.commonPractices ?? painPoint.maturePractices ?? [];
      return {
        kind: 'pain-point',
        id: painPoint.id,
        title: painPoint.title,
        eyebrow: '痛点全文阅读',
        summary: painPoint.industryPain || painPoint.solutionMethod,
        sourceFile: painPoint.sourceFile ?? painPoint.id,
        content: buildPainPointDeepDiveMarkdown(painPoint, projects),
        badges: [painPoint.topic, painPoint.severity, ...(painPoint.evidenceSources ?? [])],
        quickFacts: [
          { label: '主题', value: painPoint.topic },
          { label: '严重度', value: severityLabel(painPoint.severity) },
          { label: '证据项目', value: String(painPoint.evidenceProjectCount ?? painPoint.evidenceProjects.length) },
          { label: '行动项', value: String(painPoint.actions.length) },
        ],
        guideCards: [
          { title: '行业共性问题', body: painPoint.industryPain || '暂无' },
          { title: '为什么反复发生', body: painPoint.solutionMethod },
          { title: '成熟做法', body: commonPractices.join('、') || '暂无' },
          { title: '数据信号', body: (painPoint.dataSignals ?? []).join('、') || '暂无' },
        ],
        actionItems: painPoint.actions,
      };
    }
    case 'source': {
      const source = sources.find((item) => item.id === target.id);
      if (!source) return null;
      return {
        kind: 'source',
        id: source.id,
        title: source.title,
        eyebrow: '资料源全文阅读',
        summary: source.summary,
        sourceFile: source.sourceFile,
        content: source.content,
        badges: [source.sourceType, source.evidenceStrength, ...(source.relatedPainPoints.slice(0, 2) || [])],
        quickFacts: [
          { label: '资料类型', value: source.sourceType },
          { label: '证据强度', value: strengthLabel(source.evidenceStrength) },
          { label: '关联痛点', value: String(source.relatedPainPoints.length) },
          { label: '关联方案', value: String(source.relatedPatterns.length) },
        ],
        guideCards: [
          { title: '推荐用途', body: source.recommendedUse || '暂无' },
          { title: '关联痛点', body: source.relatedPainPoints.join('；') || '暂无' },
          { title: '关联方案', body: source.relatedPatterns.join('；') || '暂无' },
          { title: '为什么值得信', body: source.summary || '暂无' },
        ],
        actionItems: source.actions,
      };
    }
    case 'engineering-logic':
      return {
        kind: 'engineering-logic',
        id: 'engineering-logic',
        title: engineeringLogic.title,
        eyebrow: '工程逻辑全文阅读',
        summary: engineeringLogic.summary,
        sourceFile: engineeringLogic.sourceFile,
        content: engineeringLogic.content,
        badges: ['工程主线', ...(engineeringLogic.currentFocus.slice(0, 3) || [])],
        quickFacts: [
          { label: '阶段数', value: String(engineeringLogic.stages.length) },
          { label: '当前焦点', value: String(engineeringLogic.currentFocus.length) },
          { label: '风险边界', value: String(engineeringLogic.riskBoundaries?.length ?? 0) },
          { label: '验证清单', value: String(engineeringLogic.validationChecklist?.length ?? 0) },
        ],
        guideCards: [
          { title: '当前焦点', body: engineeringLogic.currentFocus.join('；') || '暂无' },
          { title: '推荐顺序', body: engineeringLogic.recommendedOrder?.join('；') || '暂无' },
          { title: '风险边界', body: engineeringLogic.riskBoundaries?.join('；') || '暂无' },
          { title: '验证清单', body: engineeringLogic.validationChecklist?.join('；') || '暂无' },
        ],
        actionItems: engineeringLogic.actions,
      };
    default:
      return null;
  }
}

export function parseReaderHash(hash: string): ReaderTarget | null {
  const trimmed = hash.replace(/^#/, '');
  const match = trimmed.match(/^reader\/(project|solution|pain-point|source|engineering-logic)\/(.+)$/);
  if (!match) return null;
  return { kind: match[1] as ReaderKind, id: decodeURIComponent(match[2]) };
}

export function scrollToElement(id: string) {
  document.getElementById(id)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

export function slugify(value: string) {
  return value
    .toLowerCase()
    .replace(/[^\w一-龥]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

export function extractReaderHeadings(content: string) {
  return content
    .split('\n')
    .map((line) => line.trim())
    .filter((line) => /^#{1,4}\s+/.test(line))
    .map((line) => {
      const match = line.match(/^(#{1,4})\s+(.+)$/);
      const level = match?.[1].length ?? 1;
      const text = (match?.[2] ?? line).replace(/^\d+\.\s*/, '').trim();
      return { id: slugify(text), text, level };
    });
}

export function kindLabel(kind: SearchItem['kind']) {
  switch (kind) {
    case 'project': return '项目';
    case 'solution': return '方案';
    case 'painPoint': return '痛点';
    case 'source': return '资料源';
    case 'interview': return '面经';
    default: return '内容';
  }
}

export function severityLabel(severity: PainPoint['severity']) {
  switch (severity) {
    case 'high': return '高';
    case 'medium': return '中';
    case 'low': return '低';
    default: return severity;
  }
}

export function strengthLabel(strength: SourceItem['evidenceStrength']) {
  switch (strength) {
    case 'high': return '高';
    case 'medium': return '中';
    case 'low': return '低';
    default: return strength;
  }
}

export function parseGitHubRepo(source: string) {
  const match = source.match(/github\.com\/([^/\s]+)\/([^/\s?#]+)/i);
  if (!match) return '';
  return `${match[1]}/${match[2].replace(/\.git$/i, '')}`;
}

export function buildAnalyzeReaderDocument(result: Record<string, unknown>): ReaderDocument | null {
  const project = (result.project as Record<string, unknown> | undefined) ?? {};
  const analysis = (result.analysis as Record<string, unknown> | undefined) ?? {};
  const source = String(project.source ?? 'unknown');
  const title = String(analysis.title ?? '项目分析结果');
  const oneLine = String(analysis.oneLine ?? '');
  const whyWorthStudying = String(analysis.whyWorthStudying ?? '');
  const coreScenario = String(analysis.coreScenario ?? '');
  const generalProblems = String(analysis.generalProblems ?? '');
  const technicalFrameworks = String(analysis.technicalFrameworks ?? '');
  const designPrinciples = String(analysis.designPrinciples ?? '');
  const oneLineDetail = String(analysis.oneLineDetail ?? oneLine);
  const whyWorthStudyingDetail = String(analysis.whyWorthStudyingDetail ?? whyWorthStudying);
  const coreScenarioDetail = String(analysis.coreScenarioDetail ?? coreScenario);
  const generalProblemsDetail = String(analysis.generalProblemsDetail ?? generalProblems);
  const technicalFrameworksDetail = String(analysis.technicalFrameworksDetail ?? technicalFrameworks);
  const designPrinciplesDetail = String(analysis.designPrinciplesDetail ?? designPrinciples);
  const actions = Array.isArray(analysis.actions) ? analysis.actions.map((item: unknown) => String(item)) : [];
  const markdown = String((result.raw as Record<string, unknown> | undefined)?.markdown ?? '').trim();
  const content =
    markdown ||
    `# ${title}

## 1. 项目一句话

${oneLineDetail}

## 2. 为什么值得学

${whyWorthStudyingDetail}

## 3. 核心场景

${coreScenarioDetail}

## 4. 它解决的通用问题

${generalProblemsDetail}

## 5. 优秀技术和框架

${technicalFrameworksDetail}

## 6. 可迁移设计原则

${designPrinciplesDetail}

## 7. 对我当前项目的行动项

${actions.map((item: string) => `- ${item}`).join('\n')}
`;

  return {
    kind: 'project',
    id: `analysis-${slugify(title || source)}`,
    title,
    eyebrow: '项目分析阅读器',
    summary: oneLine || whyWorthStudying || coreScenario,
    sourceFile: String(project.draftFile ?? source),
    content,
    badges: ['分析结果', String(project.repo ?? source).trim()].filter(Boolean),
    quickFacts: [
      { label: '来源', value: source || 'unknown' },
      { label: '草稿文件', value: String(project.draftFile ?? '暂无') },
      { label: '当前状态', value: '结构化分析' },
      { label: '行动项', value: String(actions.length) },
    ],
    guideCards: [
      { title: '项目一句话', body: oneLine || '暂无' },
      { title: '为什么值得学', body: whyWorthStudying || '暂无' },
      { title: '核心场景', body: coreScenario || '暂无' },
      { title: '通用问题', body: generalProblems || '暂无' },
    ],
    actionItems: actions,
  };
}

export function recommendFolder(goal: string) {
  switch (goal) {
    case 'project':
      return '优先写入 docs/external-projects/ 对应分类目录，并同步更新项目概览字段。';
    case 'pattern':
      return '优先写入 docs/patterns/ 对应主题目录，并反链相关项目。';
    case 'pain-point':
      return '优先写入 docs/pain-points/，把行业共性问题、证据项目和行动项一起补齐。';
    case 'interview':
      return '优先写入 docs/interviews/，并把题目、口语版回答、追问链和关联项目一起补进去。';
    case 'frontend':
      return '优先写入 docs/external-projects/前端风格与工作台样本 或 docs/patterns/前端设计控制，再同步回写 DESIGN.md / 平台页面。';
    default:
      return '优先写入 docs/external-projects/ 或 docs/patterns/。';
  }
}

export function buildGraphData(
  projects: import('../types').Project[],
  solutions: import('../types').Solution[],
  painPoints: import('../types').PainPoint[],
  sources: import('../types').SourceItem[],
  interviews: import('../types').InterviewItem[],
): import('../types').GraphData {
  const nodes: import('../types').GraphNode[] = [];
  const relations: import('../types').Relation[] = [];
  const seen = new Set<string>();

  function addNode(id: string, label: string, kind: import('../types').GraphNode['kind'], score?: number) {
    if (seen.has(id)) return;
    seen.add(id);
    nodes.push({ id, label, kind, score });
  }

  for (const p of projects) {
    addNode(p.id, p.name, 'project', p.score);
    for (const patternId of p.relatedPatterns) {
      addNode(patternId, patternId, 'solution');
      relations.push({ from: p.id, to: patternId, type: 'implements', weight: 2 });
    }
    if (p.writebackTargets) {
      for (const ppId of p.writebackTargets.painPoints) {
        addNode(ppId, ppId, 'painPoint');
        relations.push({ from: p.id, to: ppId, type: 'evidence-for', weight: 1 });
      }
      for (const intId of p.writebackTargets.interviews) {
        addNode(intId, intId, 'interview');
        relations.push({ from: p.id, to: intId, type: 'supports', weight: 1 });
      }
    }
  }

  for (const s of solutions) {
    addNode(s.id, s.title, 'solution');
  }

  for (const pp of painPoints) {
    addNode(pp.id, pp.title, 'painPoint');
    if (pp.relatedSolution) {
      addNode(pp.relatedSolution, pp.relatedSolution, 'solution');
      relations.push({ from: pp.id, to: pp.relatedSolution, type: 'solves', weight: 2 });
    }
    for (const projId of pp.evidenceProjects) {
      addNode(projId, projId, 'project');
      relations.push({ from: projId, to: pp.id, type: 'evidence-for', weight: 2 });
    }
  }

  for (const src of sources) {
    addNode(src.id, src.title, 'source');
    for (const ppId of src.relatedPainPoints) {
      addNode(ppId, ppId, 'painPoint');
      relations.push({ from: src.id, to: ppId, type: 'evidence-for', weight: 1 });
    }
    for (const patId of src.relatedPatterns) {
      addNode(patId, patId, 'solution');
      relations.push({ from: src.id, to: patId, type: 'related', weight: 1 });
    }
  }

  for (const item of interviews) {
    addNode(item.id, item.rawQuestion, 'interview');
    for (const projId of item.relatedProjects) {
      addNode(projId, projId, 'project');
      relations.push({ from: item.id, to: projId, type: 'related', weight: 1 });
    }
    for (const patId of item.relatedPatterns) {
      addNode(patId, patId, 'solution');
      relations.push({ from: item.id, to: patId, type: 'related', weight: 1 });
    }
  }

  return { nodes, relations };
}
