import React, { Suspense, lazy, useEffect, useMemo, useState } from 'react';
import { ArrowLeft, ClipboardList } from 'lucide-react';
import type { ReaderDocument } from '../constants';
import { buildAnalyzeReaderDocument, parseGitHubRepo, recommendFolder, slugify } from '../utils';
import { FullReaderView } from '../components/FullReaderView';

type DistillIntent = {
  source: string;
  sourceType: 'github' | 'local' | 'article' | 'legacy';
  goal: 'project' | 'pattern' | 'pain-point' | 'interview' | 'frontend';
  style: 'article' | 'engineering' | 'interview' | 'product';
  outputs: string[];
  extraNotes: string;
  useGitingest: boolean;
  ingestFocus: string;
  autoWriteback: boolean;
};

type DistillHistoryEntry = DistillIntent & {
  id: string;
  createdAt: string;
};

type DistillDeskAction = 'ingest' | 'analyze' | 'distill';

type DistillExecutionState = {
  status: 'idle' | 'running' | 'done' | 'error';
  message: string;
  action: DistillDeskAction;
  result: Record<string, unknown> | null;
};

const distillOutputOptions = [
  '项目沉淀文档',
  '方案 / patterns 回写',
  '痛点页补强',
  '面试题与口语表达',
  '资料源登记',
  '平台行动项',
] as const;

function goalLabel(goal: DistillIntent['goal']) {
  switch (goal) {
    case 'project': return '项目沉淀';
    case 'pattern': return '方案抽象';
    case 'pain-point': return '痛点补强';
    case 'interview': return '面试训练';
    case 'frontend': return '前端风格';
    default: return goal;
  }
}

function styleLabel(style: DistillIntent['style']) {
  switch (style) {
    case 'article': return '文章感深读';
    case 'engineering': return '工程判断';
    case 'interview': return '面试表达';
    case 'product': return '平台产品化';
    default: return style;
  }
}

const distillActionMeta: Record<DistillDeskAction, { title: string; actionLabel: string; description: string; outputHint: string }> = {
  ingest: {
    title: '仓库理解',
    actionLabel: '执行仓库理解',
    description: '先把仓库转成 summary / tree / content，适合先看结构和目录。',
    outputHint: '这一层只做理解，不急着正式写草稿。适合先看项目骨架、关键目录和源码量级。',
  },
  analyze: {
    title: '分析项目',
    actionLabel: '分析并生成结构化结果',
    description: '先落草稿，再把项目一句话、核心场景、通用问题和设计原则整理出来。',
    outputHint: '这一层会把项目沉淀成可继续阅读的结构化结果，适合后续回写方案、痛点和面试题。',
  },
  distill: {
    title: '正式沉淀',
    actionLabel: '执行正式沉淀',
    description: '直接把项目写入目标目录并刷新索引，适合已经明确值得沉淀的样本。',
    outputHint: '这一层会把内容正式落到文档目录里，并同步刷新索引，方便前端立刻可读。',
  },
};

function buildDistillCommands(intent: DistillIntent, repoName: string, action: DistillDeskAction) {
  const commands: string[] = [];
  if ((action === 'ingest' || action === 'analyze' || action === 'distill') && intent.useGitingest && intent.sourceType !== 'article' && intent.sourceType !== 'legacy' && intent.source.trim()) {
    const focusArg = intent.ingestFocus.trim() ? ` --focus "${intent.ingestFocus.trim()}"` : '';
    commands.push(`python scripts\\ingest_repo.py "${intent.source.trim()}"${focusArg}`);
  }
  if ((action === 'analyze' || action === 'distill') && intent.sourceType === 'github' && repoName) {
    const useIngestArg = intent.useGitingest ? ' --use-ingest' : '';
    const ingestFocusArg = intent.useGitingest && intent.ingestFocus.trim() ? ` --ingest-focus "${intent.ingestFocus.trim()}"` : '';
    commands.push(`python scripts\\project_radar.py distill ${repoName}${useIngestArg}${ingestFocusArg}`);
  }
  if (action === 'ingest') {
    commands.push('python scripts\\ingest_repo.py <source> --focus <dir>');
  } else {
    commands.push('python scripts\\build_knowledge_index.py');
  }
  if (action === 'distill') {
    commands.push('python scripts\\knowledge_lint.py');
    commands.push('npm --prefix apps\\knowledge-platform run build');
  }
  return commands;
}

function buildExecutionMessage(action: DistillDeskAction, result: Record<string, unknown>) {
  const prefix = `${distillActionMeta[action].title}完成`;
  const outputFile = typeof result.outputFile === 'string' ? result.outputFile : typeof result.draftFile === 'string' ? result.draftFile : '';
  const extra = action === 'analyze' && result.analysis && typeof result.analysis === 'object'
    ? `\n结构化输出：${Object.keys(result.analysis as Record<string, unknown>).slice(0, 6).join(' / ')}`
    : '';
  return `${prefix}${outputFile ? `\n输出：${outputFile}` : ''}${extra}`;
}

function buildResultPreview(action: DistillDeskAction, result: Record<string, unknown>) {
  if (action === 'ingest') {
    const preview = result.preview as { summary?: string; tree?: string } | undefined;
    return [
      `source: ${String(result.source ?? '')}`,
      `ingestSource: ${String(result.ingestSource ?? '')}`,
      `outputFile: ${String(result.outputFile ?? '')}`,
      '',
      'summary:',
      preview?.summary ?? '',
      '',
      'tree:',
      preview?.tree ?? '',
    ].join('\n');
  }
  if (action === 'analyze') {
    if (!result.analysis) return JSON.stringify(result, null, 2);
    const analysis = (result.analysis as Record<string, unknown> | undefined) ?? {};
    return JSON.stringify({
      project: result.project,
      analysis: {
        title: analysis.title,
        oneLine: analysis.oneLine,
        oneLineDetail: (analysis as Record<string, unknown>).oneLineDetail,
        whyWorthStudying: analysis.whyWorthStudying,
        whyWorthStudyingDetail: (analysis as Record<string, unknown>).whyWorthStudyingDetail,
        coreScenario: analysis.coreScenario,
        coreScenarioDetail: (analysis as Record<string, unknown>).coreScenarioDetail,
        generalProblems: analysis.generalProblems,
        generalProblemsDetail: (analysis as Record<string, unknown>).generalProblemsDetail,
        technicalFrameworks: analysis.technicalFrameworks,
        technicalFrameworksDetail: (analysis as Record<string, unknown>).technicalFrameworksDetail,
        designPrinciples: analysis.designPrinciples,
        designPrinciplesDetail: (analysis as Record<string, unknown>).designPrinciplesDetail,
        actions: analysis.actions,
      },
    }, null, 2);
  }
  return JSON.stringify(result, null, 2);
}

function buildDistillPrompt(intent: DistillIntent, repoName: string, recommendedFolder: string) {
  const sourceLabel =
    intent.sourceType === 'github' ? 'GitHub 项目'
    : intent.sourceType === 'local' ? '本地项目'
    : intent.sourceType === 'article' ? '博客 / 论文 / 文档'
    : '旧目录补写';
  const outputText = intent.outputs.length ? intent.outputs.join('、') : '项目沉淀文档';
  const repoHint = repoName ? `如果适用，优先参考仓库 ${repoName} 的源码、README、docs、examples 和 changelog。` : '';
  const ingestHint = intent.useGitingest
    ? `这次先用 Gitingest 做仓库理解增强${intent.ingestFocus.trim() ? `，聚焦目录是 ${intent.ingestFocus.trim()}。` : '，默认看全仓。'}请优先利用 summary、directory tree 和 content 来理解结构，而不是只看 README。`
    : '这次先按常规方式阅读 README、docs 和关键源码，不强制使用 Gitingest。';
  const styleHint =
    intent.style === 'article' ? '写法要更像真正有文章感的深读内容，先立题，再讲场景压力、判断、误区、证据和行动项。'
    : intent.style === 'engineering' ? '重点写工程边界、取舍、约束、验证信号和为什么普通做法不够。'
    : intent.style === 'interview' ? '重点补口语版回答、三分钟工程讲法、面试官追问和容易被问爆的点。'
    : '重点补平台化、产品化、阅读体验、信息架构和可持续演化视角。';

  return [
    `请帮我沉淀这个${sourceLabel}：${intent.source || '（待补充来源）'}。`,
    `这次主目标是：${goalLabel(intent.goal)}。`,
    `希望自动产出的内容：${outputText}。`,
    `推荐写入位置：${recommendedFolder}`,
    repoHint,
    ingestHint,
    styleHint,
    '请按当前仓库已经建立的深度沉淀写法来做：不要侃侃而谈，不要只枚举功能，要写成能学习、能复述、能迁移的中文文章。',
    '默认同时检查是否需要回写项目概览字段、方案页、痛点页、面经页和平台行动项。',
    intent.extraNotes ? `额外要求：${intent.extraNotes}` : '',
  ].filter(Boolean).join('\n');
}

export function DistillDeskView() {
  const [intent, setIntent] = useState<DistillIntent>({
    source: '',
    sourceType: 'github',
    goal: 'project',
    style: 'article',
    outputs: ['项目沉淀文档', '方案 / patterns 回写', '痛点页补强'],
    extraNotes: '',
    useGitingest: true,
    ingestFocus: '',
    autoWriteback: true,
  });
  const [copied, setCopied] = useState('');
  const [bridgeUrl, setBridgeUrl] = useState('http://127.0.0.1:8765');
  const [selectedAction, setSelectedAction] = useState<DistillDeskAction>('analyze');
  const [analysisReaderDocument, setAnalysisReaderDocument] = useState<ReaderDocument | null>(null);
  const [latestAnalysisResult, setLatestAnalysisResult] = useState<Record<string, unknown> | null>(null);
  const [history, setHistory] = useState<DistillHistoryEntry[]>([]);
  const [executionState, setExecutionState] = useState<DistillExecutionState>({
    status: 'idle',
    message: '',
    action: 'analyze',
    result: null,
  });

  useEffect(() => {
    if (typeof window === 'undefined') return;
    const raw = window.localStorage.getItem('knowledge-distill-history');
    if (!raw) return;
    try {
      const parsed = JSON.parse(raw) as DistillHistoryEntry[];
      setHistory(parsed);
    } catch {
      // ignore
    }
    const savedBridgeUrl = window.localStorage.getItem('knowledge-bridge-url');
    if (savedBridgeUrl) setBridgeUrl(savedBridgeUrl);
  }, []);

  const repoName = useMemo(() => parseGitHubRepo(intent.source), [intent.source]);
  const recommendedFolder = useMemo(() => recommendFolder(intent.goal), [intent.goal]);
  const codexPrompt = useMemo(() => buildDistillPrompt(intent, repoName, recommendedFolder), [intent, repoName, recommendedFolder]);
  const commandHints = useMemo(() => buildDistillCommands(intent, repoName, selectedAction), [intent, repoName, selectedAction]);
  const selectedActionMeta = distillActionMeta[selectedAction];

  async function writebackCurrentAnalysis() {
    if (!latestAnalysisResult) return;
    setExecutionState((current) => ({ ...current, status: 'running', message: '正在把分析结果回写到 patterns / pain-points / interviews ...' }));
    try {
      const response = await fetch(`${bridgeUrl}/api/writeback-analysis`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(latestAnalysisResult),
      });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const result = (await response.json()) as Record<string, unknown>;
      const targets = (result.writebackTargets as { patterns?: string[]; painPoints?: string[]; interviews?: string[] } | undefined) ?? {};
      setExecutionState({
        status: 'done',
        action: 'analyze',
        message: [
          '自动回写完成',
          String(result.writebackSummary ?? ''),
          `patterns：${(targets.patterns ?? []).join('、') || '无'}`,
          `pain-points：${(targets.painPoints ?? []).join('、') || '无'}`,
          `interviews：${(targets.interviews ?? []).join('、') || '无'}`,
        ].filter(Boolean).join('\n'),
        result,
      });
    } catch (error) {
      setExecutionState((current) => ({ ...current, status: 'error', message: error instanceof Error ? error.message : '回写失败' }));
    }
  }

  if (analysisReaderDocument) {
    return (
      <section className="reader-workspace">
        <div className="reader-workspace-toolbar">
          <button type="button" className="ghost-button" onClick={() => setAnalysisReaderDocument(null)}>
            <ArrowLeft size={16} />
            <span>返回沉淀台</span>
          </button>
          <div className="distill-actions">
            <button type="button" className="ghost-button" onClick={() => exportMarkdown(analysisReaderDocument.title, analysisReaderDocument.content)}>
              导出 Markdown
            </button>
            <button type="button" className="primary-button" onClick={writebackCurrentAnalysis}>
              一键回写到知识库
            </button>
          </div>
        </div>
        <FullReaderView document={analysisReaderDocument} onClose={() => setAnalysisReaderDocument(null)} />
      </section>
    );
  }

  async function copyText(value: string, key: string) {
    if (typeof navigator === 'undefined' || !navigator.clipboard) return;
    await navigator.clipboard.writeText(value);
    setCopied(key);
    window.setTimeout(() => setCopied(''), 1400);
  }

  function exportMarkdown(title: string, content: string) {
    if (typeof window === 'undefined') return;
    const blob = new Blob([content], { type: 'text/markdown;charset=utf-8' });
    const url = window.URL.createObjectURL(blob);
    const anchor = document.createElement('a');
    anchor.href = url;
    anchor.download = `${slugify(title) || 'document'}.md`;
    anchor.click();
    window.URL.revokeObjectURL(url);
  }

  function toggleOutput(output: string) {
    setIntent((current) => ({
      ...current,
      outputs: current.outputs.includes(output) ? current.outputs.filter((item) => item !== output) : [...current.outputs, output],
    }));
  }

  function saveCurrentIntent() {
    const entry: DistillHistoryEntry = { ...intent, id: `${Date.now()}`, createdAt: new Date().toLocaleString('zh-CN') };
    const next = [entry, ...history].slice(0, 10);
    setHistory(next);
    if (typeof window !== 'undefined') window.localStorage.setItem('knowledge-distill-history', JSON.stringify(next));
  }

  function buildRequestPayload(action: DistillDeskAction) {
    if (action === 'ingest') return { source: intent.source, sourceType: intent.sourceType, focus: intent.ingestFocus };
    return { ...intent, refresh: true, rebuildIndex: true, autoWriteback: intent.autoWriteback };
  }

  async function executeCurrentIntent(action: DistillDeskAction = selectedAction) {
    const endpoint = action === 'ingest' ? '/api/ingest-repo' : action === 'analyze' ? '/api/analyze-project' : '/api/distill';
    setExecutionState({ status: 'running', action, message: `正在执行：${distillActionMeta[action].title}`, result: null });
    try {
      const response = await fetch(`${bridgeUrl}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(buildRequestPayload(action)),
      });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const result = (await response.json()) as Record<string, unknown>;
      setExecutionState({ status: 'done', action, message: buildExecutionMessage(action, result), result });
      if (action === 'analyze') {
        setLatestAnalysisResult(result);
        const nextDocument = buildAnalyzeReaderDocument(result);
        if (nextDocument) setAnalysisReaderDocument(nextDocument);
      }
      if (action !== 'ingest') saveCurrentIntent();
    } catch (error) {
      setExecutionState({ status: 'error', action, message: error instanceof Error ? error.message : '执行失败', result: null });
    }
  }

  function applyHistory(entry: DistillHistoryEntry) {
    setIntent({
      source: entry.source,
      sourceType: entry.sourceType,
      goal: entry.goal,
      style: entry.style,
      outputs: entry.outputs,
      extraNotes: entry.extraNotes,
      useGitingest: entry.useGitingest ?? true,
      ingestFocus: entry.ingestFocus ?? '',
      autoWriteback: entry.autoWriteback ?? true,
    });
  }

  return (
    <section className="workspace single-column">
      <article className="detail-panel">
        <div className="detail-header">
          <div>
            <div className="eyebrow">沉淀入口</div>
            <h2>直接告诉平台，这次要沉淀什么</h2>
          </div>
          <ClipboardList size={24} />
        </div>
        <p className="lead">
          这里不再把"仓库理解、分析项目、正式沉淀"混成一个动作。你先定义来源，再决定这次要先看结构、先做判断，还是正式落库，平台会按这一层的目标给你不同结果。
        </p>

        <div className="distill-grid">
          <section className="distill-form">
            <div className="form-field">
              <label>桥接服务地址</label>
              <textarea value={bridgeUrl} onChange={(event) => { const next = event.target.value; setBridgeUrl(next); if (typeof window !== 'undefined') window.localStorage.setItem('knowledge-bridge-url', next); }} placeholder="例如：http://127.0.0.1:8765" />
            </div>
            <div className="form-field">
              <label>来源地址或本地路径</label>
              <textarea value={intent.source} onChange={(event) => setIntent((current) => ({ ...current, source: event.target.value }))} placeholder="例如：https://github.com/owner/repo 或 D:\\pico 或 某篇博客 / 论文链接" />
            </div>
            <div className="form-field">
              <label>项目理解增强</label>
              <label className="checkbox-card">
                <input type="checkbox" checked={intent.useGitingest} onChange={(event) => setIntent((current) => ({ ...current, useGitingest: event.target.checked }))} />
                <span>启用 Gitingest 深度理解，把仓库先转成 summary / tree / content 再进入沉淀</span>
              </label>
            </div>
            <div className="form-field">
              <label>自动回写闭环</label>
              <label className="checkbox-card">
                <input type="checkbox" checked={intent.autoWriteback} onChange={(event) => setIntent((current) => ({ ...current, autoWriteback: event.target.checked }))} />
                <span>分析完成后默认自动回写到 patterns / pain-points / interviews，并立即重建索引</span>
              </label>
            </div>
            {intent.useGitingest ? (
              <div className="form-field">
                <label>Gitingest 聚焦目录（可选）</label>
                <textarea value={intent.ingestFocus} onChange={(event) => setIntent((current) => ({ ...current, ingestFocus: event.target.value }))} placeholder="例如：src / packages/core / apps/web；留空表示全仓" />
              </div>
            ) : null}
            <div className="form-field">
              <label>来源类型</label>
              <div className="segmented">
                {([['github', 'GitHub 项目'], ['local', '本地项目'], ['article', '博客 / 论文 / 文档'], ['legacy', '旧目录补写']] as const).map(([value, label]) => (
                  <button key={value} className={intent.sourceType === value ? 'selected' : ''} onClick={() => setIntent((current) => ({ ...current, sourceType: value }))}>{label}</button>
                ))}
              </div>
            </div>
            <div className="form-field">
              <label>这次最主要的沉淀目标</label>
              <div className="segmented">
                {([['project', '项目沉淀'], ['pattern', '方案抽象'], ['pain-point', '痛点补强'], ['interview', '面试训练'], ['frontend', '前端风格']] as const).map(([value, label]) => (
                  <button key={value} className={intent.goal === value ? 'selected' : ''} onClick={() => setIntent((current) => ({ ...current, goal: value }))}>{label}</button>
                ))}
              </div>
            </div>
            <div className="form-field">
              <label>你更希望这次偏哪种写法</label>
              <div className="segmented">
                {([['article', '文章感深读'], ['engineering', '工程判断'], ['interview', '面试表达'], ['product', '平台产品化']] as const).map(([value, label]) => (
                  <button key={value} className={intent.style === value ? 'selected' : ''} onClick={() => setIntent((current) => ({ ...current, style: value }))}>{label}</button>
                ))}
              </div>
            </div>
            <div className="form-field">
              <label>这次希望自动产出哪些东西</label>
              <div className="checkbox-grid">
                {distillOutputOptions.map((option) => (
                  <label key={option} className="checkbox-card">
                    <input type="checkbox" checked={intent.outputs.includes(option)} onChange={() => toggleOutput(option)} />
                    <span>{option}</span>
                  </label>
                ))}
              </div>
            </div>
            <div className="form-field">
              <label>额外要求</label>
              <textarea value={intent.extraNotes} onChange={(event) => setIntent((current) => ({ ...current, extraNotes: event.target.value }))} placeholder="例如：重点看源码、要补面试追问、参考黄同学h写法、顺便回写痛点页" />
            </div>
            <div className="form-field">
              <label>这一步想先做什么</label>
              <div className="distill-action-grid">
                {(Object.entries(distillActionMeta) as Array<[DistillDeskAction, (typeof distillActionMeta)[DistillDeskAction]]>).map(([key, meta]) => (
                  <button key={key} type="button" className={`distill-action-card ${selectedAction === key ? 'selected' : ''}`} onClick={() => setSelectedAction(key)}>
                    <strong>{meta.title}</strong>
                    <span>{meta.description}</span>
                  </button>
                ))}
              </div>
            </div>
            <div className="distill-actions">
              <button type="button" className="primary-button" onClick={() => copyText(codexPrompt, 'prompt')}>
                {copied === 'prompt' ? '已复制指令' : '复制给 Codex 的指令'}
              </button>
              <button type="button" className="primary-button" onClick={() => executeCurrentIntent(selectedAction)}>
                {executionState.status === 'running' ? '执行中...' : selectedActionMeta.actionLabel}
              </button>
              <button type="button" className="ghost-button" onClick={saveCurrentIntent}>保存到本地草稿</button>
            </div>
            {executionState.status !== 'idle' ? (
              <div className={`answer-box execution-state ${executionState.status}`}>
                <h3>执行状态</h3>
                <p>{executionState.message}</p>
              </div>
            ) : null}
          </section>

          <section className="distill-output">
            <div className="answer-box">
              <h3>推荐写入位置</h3>
              <p>{recommendedFolder}</p>
            </div>
            <div className="answer-box">
              <h3>当前动作说明</h3>
              <p>{selectedActionMeta.outputHint}</p>
            </div>
            <div className="answer-box">
              <h3>推荐执行命令</h3>
              <div className="command-stack">
                {commandHints.map((command) => (
                  <button key={command} type="button" className="command-card" onClick={() => copyText(command, command)}>
                    <code>{command}</code>
                    <span>{copied === command ? '已复制' : '点击复制'}</span>
                  </button>
                ))}
              </div>
            </div>
            <div className="answer-box">
              <h3>给 Codex 的沉淀指令</h3>
              <pre className="prompt-preview">{codexPrompt}</pre>
            </div>
            <div className="answer-box">
              <h3>这一轮会怎么做</h3>
              <ul>
                <li>先按来源类型决定是走 Project Radar、源码阅读，还是资料源吸收。</li>
                <li>再按当前动作决定只是理解仓库、做结构化分析，还是正式落草稿。</li>
                <li>最后按当前深度写作规范，把内容写成能学、能说、能迁移的文章，而不是功能枚举。</li>
              </ul>
            </div>
            {executionState.result ? (
              <div className="answer-box">
                <h3>当前返回结果</h3>
                <pre className="result-preview">{buildResultPreview(executionState.action, executionState.result)}</pre>
                {latestAnalysisResult ? (
                  <div className="distill-actions">
                    <button type="button" className="ghost-button" onClick={() => {
                      const nextDocument = buildAnalyzeReaderDocument(latestAnalysisResult!);
                      if (nextDocument) setAnalysisReaderDocument(nextDocument);
                    }}>打开分析阅读器</button>
                    <button type="button" className="ghost-button" onClick={writebackCurrentAnalysis}>一键回写</button>
                  </div>
                ) : null}
              </div>
            ) : null}
          </section>
        </div>

        <section className="history-panel">
          <div className="panel-title">
            <ClipboardList size={18} />
            <span>最近沉淀草稿</span>
          </div>
          {history.length ? (
            <div className="history-grid">
              {history.map((entry) => (
                <button key={entry.id} type="button" className="jump-card" onClick={() => applyHistory(entry)}>
                  <div className="card-row">
                    <strong>{entry.source || '未命名任务'}</strong>
                    <span className="badge">{entry.createdAt}</span>
                  </div>
                  <p>{goalLabel(entry.goal)} / {styleLabel(entry.style)} / {entry.outputs.join('、')}</p>
                </button>
              ))}
            </div>
          ) : (
            <p className="muted">你保存过的沉淀草稿会显示在这里，方便反复补写和继续追任务。</p>
          )}
        </section>
      </article>
    </section>
  );
}
