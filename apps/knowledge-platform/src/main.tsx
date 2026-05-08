import React, { Suspense, lazy, useEffect, useMemo, useState } from 'react';
import { createRoot } from 'react-dom/client';
import {
  AlertTriangle,
  ArrowLeft,
  BrainCircuit,
  ClipboardList,
  ExternalLink,
  FileQuestion,
  FileSearch,
  FolderKanban,
  GitBranch,
  Layers3,
  MessageSquareText,
  Radar,
  Search,
  Sparkles,
} from 'lucide-react';
import rawData from './data/knowledge-index.json';
import type { EngineeringLogic, InterviewItem, KnowledgeIndex, PainPoint, Project, SearchItem, Solution, SourceItem } from './types';
import './styles.css';

const data = rawData as KnowledgeIndex;
const MarkdownPreview = lazy(() => import('./MarkdownPreview'));

type View =
  | 'distill-desk'
  | 'projects'
  | 'solutions'
  | 'pain-points'
  | 'engineering-logic'
  | 'sources'
  | 'interviews'
  | 'interviewer'
  | 'radar'
  | 'feedback'
  | 'visual-generation';

type ReaderKind = 'project' | 'solution' | 'pain-point' | 'source' | 'engineering-logic';

type ReaderTarget = {
  kind: ReaderKind;
  id: string;
};

const navItems: Array<{ id: View; label: string; icon: React.ComponentType<{ size?: number }> }> = [
  { id: 'distill-desk', label: '沉淀台', icon: ClipboardList },
  { id: 'projects', label: '项目', icon: FolderKanban },
  { id: 'solutions', label: '方案', icon: Layers3 },
  { id: 'pain-points', label: '痛点', icon: AlertTriangle },
  { id: 'engineering-logic', label: '工程逻辑', icon: GitBranch },
  { id: 'sources', label: '资料源', icon: FileSearch },
  { id: 'interviews', label: '面经', icon: FileQuestion },
  { id: 'interviewer', label: 'AI 面试官', icon: BrainCircuit },
  { id: 'radar', label: '雷达', icon: Radar },
  { id: 'feedback', label: '反馈', icon: MessageSquareText },
  { id: 'visual-generation', label: '视觉生成', icon: Sparkles },
];

const viewMeta: Record<View, { title: string; subtitle: string }> = {
  'distill-desk': {
    title: '沉淀工作台',
    subtitle: '直接录入要沉淀的项目、资料或本地仓库，自动生成给 Codex 的沉淀指令、推荐命令与输出落点。',
  },
  projects: {
    title: '项目样本库',
    subtitle: '按项目类型、状态、评分和沉淀深度查看外部样本与自研项目，直接进入真正值得学习的内容。',
  },
  solutions: {
    title: '方案方法库',
    subtitle: '把多个项目背后的共性问题抽象成可迁移的工程框架、实践套路与当前行动项。',
  },
  'pain-points': {
    title: '行业痛点库',
    subtitle: '围绕 Agent 与大模型行业的普遍难题，持续沉淀证据项目、成熟做法、数据信号与平台启发。',
  },
  'engineering-logic': {
    title: '工程逻辑总纲',
    subtitle: '把项目、方案、痛点与资料源收束成真实项目的设计顺序、验证方法与迭代主线。',
  },
  sources: {
    title: '外部资料源',
    subtitle: '统一管理 GitHub、博客、论文和用户文档，让外部资料进入可沉淀、可学习、可反哺的平台流水线。',
  },
  interviews: {
    title: '面经与答案',
    subtitle: '把问题、答题骨架、追问方向与关联项目串起来，形成真正能练习和复盘的题库。',
  },
  interviewer: {
    title: 'AI 面试官',
    subtitle: '围绕当前项目、平台沉淀与外部高质量样本，训练项目表达、取舍判断与工程解释能力。',
  },
  radar: {
    title: 'Project Radar',
    subtitle: '跟踪项目发现、评分、候选池和沉淀状态，让知识库具备持续主动学习能力。',
  },
  feedback: {
    title: '阅读反馈',
    subtitle: '把你在阅读文档过程中的“有帮助 / 需补强 / 备注”沉淀成后续改写与追问输入。',
  },
  'visual-generation': {
    title: '视觉生成工作流',
    subtitle: '把 DESIGN.md、页面风格样本、生成图与真实前端实现串成稳定的中文页面设计流程。',
  },
};

function App() {
  const [view, setView] = useState<View>('projects');
  const [query, setQuery] = useState('');
  const [selectedType, setSelectedType] = useState('全部');
  const [projectViewMode, setProjectViewMode] = useState<'overview' | 'detail'>('overview');
  const [selectedProjectId, setSelectedProjectId] = useState(data.projects[0]?.id ?? '');
  const [selectedSolutionId, setSelectedSolutionId] = useState(data.solutions[0]?.id ?? '');
  const [selectedPainPointId, setSelectedPainPointId] = useState(data.painPoints[0]?.id ?? '');
  const [selectedSourceId, setSelectedSourceId] = useState(data.sources[0]?.id ?? '');
  const [selectedInterviewId, setSelectedInterviewId] = useState(data.interviews.items[0]?.id ?? '');
  const [readerTarget, setReaderTarget] = useState<ReaderTarget | null>(null);

  const projectTypes = useMemo(() => {
    const set = new Set<string>();
    data.projects.forEach((project) => project.types.forEach((type) => set.add(type)));
    return ['全部', ...Array.from(set).sort((a, b) => a.localeCompare(b, 'zh-CN'))];
  }, []);

  const filteredProjects = useMemo(() => {
    const keyword = query.trim().toLowerCase();
    return data.projects.filter((project) => {
      const text = `${project.name} ${project.summary} ${project.types.join(' ')} ${project.status}`.toLowerCase();
      const typeMatch = selectedType === '全部' || project.types.includes(selectedType);
      return typeMatch && (!keyword || text.includes(keyword));
    });
  }, [query, selectedType]);

  const searchResults = useMemo(() => {
    const keyword = query.trim().toLowerCase();
    if (!keyword) return [];
    return (data.searchIndex ?? [])
      .map((item) => {
        const text = `${item.title} ${item.summary} ${item.context} ${item.tags.join(' ')} ${item.searchableText}`.toLowerCase();
        const score =
          (item.title.toLowerCase().includes(keyword) ? 6 : 0) +
          (item.tags.join(' ').toLowerCase().includes(keyword) ? 3 : 0) +
          (item.summary.toLowerCase().includes(keyword) ? 2 : 0) +
          (text.includes(keyword) ? 1 : 0);
        return { item, score };
      })
      .filter((entry) => entry.score > 0)
      .sort((a, b) => b.score - a.score)
      .slice(0, 12)
      .map((entry) => entry.item);
  }, [query]);

  useEffect(() => {
    if (!filteredProjects.some((project) => project.id === selectedProjectId)) {
      setSelectedProjectId(filteredProjects[0]?.id ?? data.projects[0]?.id ?? '');
    }
  }, [filteredProjects, selectedProjectId]);

  useEffect(() => {
    if (typeof window === 'undefined') return;
    const applyHash = () => {
      const target = parseReaderHash(window.location.hash);
      setReaderTarget(target);
    };
    applyHash();
    window.addEventListener('hashchange', applyHash);
    return () => window.removeEventListener('hashchange', applyHash);
  }, []);

  const selectedProject = data.projects.find((project) => project.id === selectedProjectId) ?? filteredProjects[0] ?? data.projects[0];
  const selectedSolution = data.solutions.find((item) => item.id === selectedSolutionId) ?? data.solutions[0];
  const selectedPainPoint = data.painPoints.find((item) => item.id === selectedPainPointId) ?? data.painPoints[0];
  const selectedSource = data.sources.find((item) => item.id === selectedSourceId) ?? data.sources[0];
  const selectedInterview = data.interviews.items.find((item) => item.id === selectedInterviewId) ?? data.interviews.items[0];
  const activeReader = useMemo(
    () => buildReaderDocument(readerTarget, data.projects, data.solutions, data.painPoints, data.sources, data.engineeringLogic),
    [readerTarget],
  );

  const metrics = [
    { label: '项目', value: data.projects.length, tone: 'blue' },
    { label: '方案', value: data.solutions.length, tone: 'green' },
    { label: '痛点', value: data.painPoints.length, tone: 'amber' },
    { label: '资料源', value: data.sources.length, tone: 'blue' },
    { label: '面经', value: data.interviews.questionCount, tone: 'green' },
    { label: '搜索项', value: data.searchIndex.length, tone: 'amber' },
  ];

  function openSearchItem(item: SearchItem) {
    switch (item.kind) {
      case 'project':
        setView('projects');
        setSelectedProjectId(item.entityId);
        setProjectViewMode('detail');
        break;
      case 'solution':
        setView('solutions');
        setSelectedSolutionId(item.entityId);
        break;
      case 'painPoint':
        setView('pain-points');
        setSelectedPainPointId(item.entityId);
        break;
      case 'source':
        setView('sources');
        setSelectedSourceId(item.entityId);
        break;
      case 'interview':
        setView('interviews');
        setSelectedInterviewId(item.entityId);
        break;
      default:
        break;
    }
  }

  function openReader(kind: ReaderKind, id: string) {
    setReaderTarget({ kind, id });
    if (typeof window !== 'undefined') {
      window.location.hash = `reader/${kind}/${encodeURIComponent(id)}`;
    }
  }

  function closeReader() {
    setReaderTarget(null);
    if (typeof window !== 'undefined') {
      const url = new URL(window.location.href);
      url.hash = '';
      window.history.replaceState({}, '', url);
    }
  }

  const meta = viewMeta[view];

  return (
    <div className={`app-shell ${activeReader ? 'reader-mode' : ''}`}>
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">K</div>
          <div>
            <div className="brand-title">Knowledge Platform</div>
            <div className="brand-subtitle">自动发现 + 自动筛选 + 自动沉淀</div>
          </div>
        </div>

        <div className="nav-list">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <button
                key={item.id}
                type="button"
                className={`nav-item ${view === item.id ? 'active' : ''}`}
                onClick={() => {
                  closeReader();
                  setView(item.id);
                  if (item.id === 'projects') {
                    setProjectViewMode('overview');
                  }
                }}
              >
                <Icon size={18} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </div>

        <div className="design-note">
          <Sparkles size={16} />
          <div>
            <strong>平台目标</strong>
            <span>把优质项目、资料与经验沉淀成真正可学习、可迁移、可反哺项目的工程资产。</span>
          </div>
        </div>
      </aside>

      <main className="main">
        {activeReader ? (
          <Suspense fallback={<div className="detail-panel">正在加载阅读组件...</div>}>
            <FullReaderView document={activeReader} onClose={closeReader} />
          </Suspense>
        ) : (
          <>
        <header className="topbar">
          <div className="title-group">
            <div className="eyebrow">{meta.title}</div>
            <h1>{meta.title}</h1>
            <p>{meta.subtitle}</p>
          </div>
          <label className="search-box">
            <Search size={16} />
            <input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="搜索项目、方案、痛点、资料源、面经" />
          </label>
        </header>

        <section className="metrics-strip">
          {metrics.map((metric) => (
            <div key={metric.label} className={`metric metric-${metric.tone}`}>
              <span>{metric.label}</span>
              <strong>{metric.value}</strong>
            </div>
          ))}
        </section>

        {searchResults.length > 0 ? <SearchResults results={searchResults} onOpen={openSearchItem} /> : null}

        <Suspense fallback={<div className="detail-panel">正在加载阅读组件...</div>}>
          {view === 'distill-desk' ? <DistillDeskView /> : null}
          {view === 'projects' && selectedProject ? (
            <ProjectsView
              projects={filteredProjects}
              selectedProject={selectedProject}
              projectTypes={projectTypes}
              selectedType={selectedType}
              mode={projectViewMode}
              onTypeChange={setSelectedType}
              onOpenDetail={(id) => {
                setSelectedProjectId(id);
                setProjectViewMode('detail');
              }}
              onBackToOverview={() => setProjectViewMode('overview')}
              onOpenReader={openReader}
            />
          ) : null}
          {view === 'solutions' && selectedSolution ? <SolutionsView solutions={data.solutions} selectedSolution={selectedSolution} onSelect={setSelectedSolutionId} onOpenReader={openReader} /> : null}
          {view === 'pain-points' && selectedPainPoint ? (
            <PainPointsView painPoints={data.painPoints} selectedPainPoint={selectedPainPoint} projects={data.projects} onSelect={setSelectedPainPointId} onOpenReader={openReader} />
          ) : null}
          {view === 'engineering-logic' ? <EngineeringLogicView engineeringLogic={data.engineeringLogic} projects={data.projects} solutions={data.solutions} painPoints={data.painPoints} onOpenReader={openReader} /> : null}
          {view === 'sources' && selectedSource ? <SourcesView sources={data.sources} selectedSource={selectedSource} onSelect={setSelectedSourceId} onOpenReader={openReader} /> : null}
          {view === 'interviews' && selectedInterview ? <InterviewsView items={data.interviews.items} selectedItem={selectedInterview} onSelect={setSelectedInterviewId} /> : null}
          {view === 'interviewer' ? <InterviewerView items={data.interviews.items} memory={data.interviews.memory} /> : null}
          {view === 'radar' ? <RadarView projects={data.projects} /> : null}
          {view === 'feedback' ? <FeedbackSummaryView /> : null}
          {view === 'visual-generation' ? <VisualGenerationView /> : null}
        </Suspense>
          </>
        )}
      </main>
    </div>
  );
}

function ProjectsView({
  projects,
  selectedProject,
  projectTypes,
  selectedType,
  mode,
  onTypeChange,
  onOpenDetail,
  onBackToOverview,
  onOpenReader,
}: {
  projects: Project[];
  selectedProject: Project;
  projectTypes: string[];
  selectedType: string;
  mode: 'overview' | 'detail';
  onTypeChange: (type: string) => void;
  onOpenDetail: (id: string) => void;
  onBackToOverview: () => void;
  onOpenReader: (kind: ReaderKind, id: string) => void;
}) {
  if (mode === 'detail') {
    return (
      <section className="workspace single-column">
        <article className="detail-panel document-detail-panel">
          <div className="detail-toolbar">
            <button type="button" className="ghost-button" onClick={onBackToOverview}>
              <ArrowLeft size={16} />
              <span>返回项目概览</span>
            </button>
            {selectedProject.url ? (
              <a className="ghost-link" href={selectedProject.url} target="_blank" rel="noreferrer">
                <ExternalLink size={16} />
                <span>查看原项目</span>
              </a>
            ) : null}
          </div>

          <div className="document-hero">
            <div className="eyebrow">项目详情</div>
            <h2>{selectedProject.name}</h2>
            <p className="lead">{selectedProject.oneLineVerdict || selectedProject.summary}</p>
            <div className="inline-facts">
              <span className="badge good">{selectedProject.primaryCategory}</span>
              <span className="badge">{selectedProject.status}</span>
              {selectedProject.score ? <span className="badge">评分 {selectedProject.score}</span> : null}
            </div>
          </div>

          <div className="overview-strip">
            <FactItem label="主分类" value={selectedProject.primaryCategory} />
            <FactItem label="业务场景" value={selectedProject.businessScenario} />
            <FactItem label="最大亮点" value={selectedProject.biggestHighlight} />
            <FactItem label="关联方案" value={String(selectedProject.relatedPatterns.length)} />
          </div>

          <div className="reader-preface-grid">
            <section className="answer-box">
              <h3>为什么现在读</h3>
              <p>{selectedProject.whyReadNow || buildProjectTakeaway(selectedProject)}</p>
            </section>
            <section className="answer-box">
              <h3>读完要带走什么</h3>
              <p>{buildProjectTakeaway(selectedProject)}</p>
            </section>
            <section className="answer-box">
              <h3>最容易误读什么</h3>
              <p>{buildProjectMisreadWarning(selectedProject)}</p>
            </section>
            <section className="answer-box">
              <h3>最容易追问什么</h3>
              <p>{buildProjectPressurePrompt(selectedProject)}</p>
            </section>
          </div>

          <div className="reader-preface-grid">
            <section className="answer-box">
              <h3>口语版回答</h3>
              <p>{selectedProject.oralAnswer || buildProjectOralAnswer(selectedProject)}</p>
            </section>
            <section className="answer-box">
              <h3>三分钟工程讲法</h3>
              <p>{selectedProject.engineeringPitch || buildProjectEngineeringPitch(selectedProject)}</p>
            </section>
          </div>

          <div className="evidence-grid">
            <InfoBlock title="项目标签" items={selectedProject.types} empty="暂无标签" />
            <InfoBlock title="当前行动项" items={selectedProject.nextActions} empty="暂无行动项" />
            <InfoBlock title="关联方案" items={selectedProject.relatedPatterns} empty="暂无关联方案" />
          </div>

          {selectedProject.writebackSummary || (selectedProject.writebackTargets?.patterns?.length ?? 0) > 0 || (selectedProject.writebackTargets?.painPoints?.length ?? 0) > 0 || (selectedProject.writebackTargets?.interviews?.length ?? 0) > 0 ? (
            <section className="answer-box">
              <h3>自动回写影响</h3>
              <p>{selectedProject.writebackSummary || '这次项目沉淀已经反哺到方案、痛点或面试资产。'}</p>
              <p>
                当前状态：{selectedProject.writebackStatus || 'none'}
                {selectedProject.writebackUpdatedAt ? ` · 最近更新：${selectedProject.writebackUpdatedAt}` : ''}
              </p>
              <div className="evidence-grid compact-grid">
                <InfoBlock title="补强的方案" items={selectedProject.writebackTargets?.patterns ?? []} empty="暂无自动回写方案" />
                <InfoBlock title="补强的痛点" items={selectedProject.writebackTargets?.painPoints ?? []} empty="暂无自动回写痛点" />
                <InfoBlock title="新增面试资产" items={selectedProject.writebackTargets?.interviews ?? []} empty="暂无自动回写面试资产" />
              </div>
              {selectedProject.writebackReasoning?.length ? <InfoBlock title="命中原因" items={selectedProject.writebackReasoning} empty="暂无命中原因" /> : null}
            </section>
          ) : null}

          <section className="deep-dive-panel">
            <div className="detail-header">
              <div>
                <div className="eyebrow">深度拆解</div>
                <h3>不要只看结论，要看这个项目具体怎么做</h3>
              </div>
            </div>
            <p className="lead">
              这里直接抽取项目正文里的“通用问题 / 技术框架 / 可迁移原则”原文结构，重点看这个项目是如何拆问题、落方案、做步骤和形成工程边界的。
            </p>
            <MarkdownPreview
              title={`${selectedProject.name} 深度拆解`}
              content={buildProjectDeepDiveMarkdown(selectedProject)}
              sourceFile={selectedProject.sourceFile}
              showHeader={false}
              showOutline={false}
              showFeedback={false}
            />
          </section>

          <div className="source-line">
            <span>来源文件</span>
            <strong>{selectedProject.sourceFile}</strong>
          </div>

          <ReaderLaunchPanel
            label="项目全文阅读器"
            title="进入整页阅读"
            description="这里先做项目判断和导读，真正的长文阅读放到独立阅读器里，避免和概览信息混在一起。"
            onOpen={() => onOpenReader('project', selectedProject.id)}
          />
        </article>
      </section>
    );
  }

  return (
    <section className="workspace single-column">
      <div className="list-panel overview-panel">
        <div className="detail-header">
          <div>
            <div className="eyebrow">项目概览</div>
            <h2>先判断值不值得看，再进入深读</h2>
          </div>
          <ClipboardList size={22} />
        </div>
        <p className="lead">
          这里不再把项目概述和长文详情混在一起。你先看主分类、业务场景和最大亮点，确认这是不是你现在该花时间读的样本，再进入详情页。
        </p>
        <div className="segmented compact">
          {projectTypes.map((type) => (
            <button key={type} className={selectedType === type ? 'selected' : ''} onClick={() => onTypeChange(type)}>
              {type}
            </button>
          ))}
        </div>
        <div className="project-overview-grid">
          {projects.map((project) => (
            <article key={project.id} className="project-overview-card">
              <div className="card-row">
                <strong>{project.name}</strong>
                {project.score ? <span className="badge">评分 {project.score}</span> : <StatusBadge status={project.status} />}
              </div>
              <p className="overview-verdict">{project.oneLineVerdict || project.summary}</p>
              <div className="overview-meta-list">
                <OverviewMeta label="主分类" value={project.primaryCategory} />
                <OverviewMeta label="业务场景" value={project.businessScenario} />
                <OverviewMeta label="最大亮点" value={project.biggestHighlight} />
              </div>
              <div className="overview-footer">
                <TagList tags={project.types.slice(0, 4)} />
                <button type="button" className="primary-button" onClick={() => onOpenDetail(project.id)}>
                  进入详情
                </button>
              </div>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}

function SolutionsView({
  solutions,
  selectedSolution,
  onSelect,
  onOpenReader,
}: {
  solutions: Solution[];
  selectedSolution: Solution;
  onSelect: (id: string) => void;
  onOpenReader: (kind: ReaderKind, id: string) => void;
}) {
  return (
    <section className="workspace two-column">
      <div className="list-panel">
        <div className="panel-title">
          <Layers3 size={18} />
          <span>方案方法</span>
        </div>
        <div className="list-meta">这里不是术语目录，而是会反复出现在真实项目里的共性工程问题。</div>
        <div className="item-list">
          {solutions.map((solution) => (
            <button key={solution.id} className={`item-card ${selectedSolution.id === solution.id ? 'selected' : ''}`} onClick={() => onSelect(solution.id)}>
              <strong>{solution.title}</strong>
              <p>{solution.problemDefinition || '暂无问题定义'}</p>
              <span className="badge">{solution.actions.length} 个行动项</span>
            </button>
          ))}
        </div>
      </div>
      <article className="detail-panel">
        <div className="eyebrow">方案导读</div>
        <h2>{selectedSolution.title}</h2>
        <p className="lead">{selectedSolution.problemDefinition || '暂无问题定义'}</p>
        <div className="source-line">
          <span>来源文件</span>
          <strong>{selectedSolution.sourceFile}</strong>
        </div>
        <LearningGuide
          title="方案阅读方式"
          items={[
            '先回答这个方案到底在解决什么行业通用问题。',
            '再看常见误区和成熟做法，理解为什么不能只靠堆功能。',
            '最后把行动项转成你当前平台或项目的实现顺序。',
          ]}
        />
        <div className="workflow-grid">
          <section className="answer-box">
            <h3>带走的判断</h3>
            <p>{buildSolutionTakeaway(selectedSolution)}</p>
          </section>
          <section className="answer-box">
            <h3>继续追问</h3>
            <p>{buildSolutionPressurePrompt(selectedSolution)}</p>
          </section>
        </div>
        <div className="evidence-grid">
          <InfoBlock title="为什么重要" items={selectedSolution.whyImportant} empty="暂无内容" />
          <InfoBlock title="常见误区" items={selectedSolution.commonMistakes} empty="暂无内容" />
          <InfoBlock title="成熟做法" items={selectedSolution.maturePractices} empty="暂无内容" />
          <InfoBlock title="当前行动项" items={selectedSolution.actions} empty="暂无行动项" />
        </div>
        <section className="deep-dive-panel">
          <div className="detail-header">
            <div>
              <div className="eyebrow">深度拆解</div>
              <h3>把“这套方案怎么落地”写成能直接学习的正文</h3>
            </div>
          </div>
          <p className="lead">
            这里不再只保留术语和要点，而是按“问题定义 / 方案结构 / 成熟做法 / 常见误区 / 当前动作”的顺序展开，方便你直接拿去学习、复述和迁移。
          </p>
          <MarkdownPreview
            title={`${selectedSolution.title} 深度拆解`}
            content={buildSolutionDeepDiveMarkdown(selectedSolution)}
            sourceFile={selectedSolution.sourceFile}
            showHeader={false}
            showOutline={false}
            showFeedback={false}
          />
        </section>
        <ReaderLaunchPanel
          label="方案全文阅读器"
          title="进入整页阅读"
          description="方案页先保留判断、误区和行动项，正文放进独立阅读器，读起来会更像真正的知识库文档。"
          onOpen={() => onOpenReader('solution', selectedSolution.id)}
        />
      </article>
    </section>
  );
}

function PainPointsView({
  painPoints,
  selectedPainPoint,
  projects,
  onSelect,
  onOpenReader,
}: {
  painPoints: PainPoint[];
  selectedPainPoint: PainPoint;
  projects: Project[];
  onSelect: (id: string) => void;
  onOpenReader: (kind: ReaderKind, id: string) => void;
}) {
  const projectNames = new Map(projects.map((project) => [project.id, project.name]));
  const evidenceCount = selectedPainPoint.evidenceProjectCount ?? selectedPainPoint.evidenceProjects.length;
  const commonPractices = selectedPainPoint.commonPractices ?? selectedPainPoint.maturePractices ?? [];
  const lastUpdatedFromProjects = (selectedPainPoint.lastUpdatedFromProjects ?? []).map((id) => projectNames.get(id) || id);
  const lastUpdatedLabel = selectedPainPoint.lastUpdatedAt
    ? new Date(selectedPainPoint.lastUpdatedAt).toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
      })
    : '';

  return (
    <section className="workspace two-column">
      <div className="list-panel">
        <div className="panel-title">
          <AlertTriangle size={18} />
          <span>??????</span>
        </div>
        <div className="list-meta">???????? bug??? Agent / ????????????????????????????</div>
        <div className="item-list">
          {painPoints.map((painPoint) => (
            <button key={painPoint.id} className={`item-card ${selectedPainPoint.id === painPoint.id ? 'selected' : ''}`} onClick={() => onSelect(painPoint.id)}>
              <div className="card-row">
                <strong>{painPoint.title}</strong>
                <span className={`badge severity-${painPoint.severity}`}>{severityLabel(painPoint.severity)}</span>
              </div>
              <p>{painPoint.industryPain || painPoint.solutionMethod}</p>
              <div className="inline-badges">
                <span className="badge">{painPoint.topic}</span>
                <span className="badge">???? {painPoint.evidenceProjectCount ?? painPoint.evidenceProjects.length}</span>
              </div>
            </button>
          ))}
        </div>
      </div>
      <article className="detail-panel">
        <div className="eyebrow">????</div>
        <h2>{selectedPainPoint.title}</h2>
        <p className="lead">{selectedPainPoint.industryPain || selectedPainPoint.solutionMethod}</p>
        <div className="fact-grid">
          <FactItem label="???" value={severityLabel(selectedPainPoint.severity)} />
          <FactItem label="????" value={String(evidenceCount)} />
          <FactItem label="????" value={String(commonPractices.length)} />
          <FactItem label="???" value={String(selectedPainPoint.actions.length)} />
        </div>
        <div className="source-line">
          <span>????</span>
          <strong>{selectedPainPoint.relatedSolution}</strong>
        </div>
        {(lastUpdatedLabel || lastUpdatedFromProjects.length) && (
          <div className="evidence-grid">
            <InfoBlock title="??????" items={lastUpdatedFromProjects} empty="????????" />
            <InfoBlock title="??????" items={lastUpdatedLabel ? [lastUpdatedLabel] : []} empty="??????" />
          </div>
        )}
        <LearningGuide
          title="??????"
          items={[
            '???????????????????????????????????',
            '??????????????????????????????????',
            '???????????????????????????????',
          ]}
        />
        <div className="workflow-grid">
          <section className="answer-box">
            <h3>?????</h3>
            <p>{buildPainPointTakeaway(selectedPainPoint)}</p>
          </section>
          <section className="answer-box">
            <h3>????</h3>
            <p>{buildPainPointPressurePrompt(selectedPainPoint)}</p>
          </section>
        </div>
        <div className="evidence-grid">
          <InfoBlock title="????" items={selectedPainPoint.evidenceSources ?? []} empty="??????" />
          <InfoBlock title="????" items={selectedPainPoint.evidenceProjects.map((id) => projectNames.get(id) || id)} empty="??????" />
          <InfoBlock title="????" items={commonPractices} empty="??????" />
          <InfoBlock title="????" items={selectedPainPoint.dataSignals ?? []} empty="??????" />
          <InfoBlock title="????" items={selectedPainPoint.commonMistakes} empty="????" />
          <InfoBlock title="??????" items={selectedPainPoint.evolutionRule ? [selectedPainPoint.evolutionRule] : []} empty="????????" />
        </div>
        <section className="deep-dive-panel">
          <div className="detail-header">
            <div>
              <div className="eyebrow">????</div>
              <h3>???????????????????</h3>
            </div>
          </div>
          <p className="lead">??????????????????????????????????????????????????????????????????</p>
          <MarkdownPreview
            title={`${selectedPainPoint.title} ????`}
            content={buildPainPointDeepDiveMarkdown(selectedPainPoint, projects)}
            sourceFile={selectedPainPoint.sourceFile ?? selectedPainPoint.id}
            showHeader={false}
            showOutline={false}
            showFeedback={false}
          />
        </section>
        <ReaderLaunchPanel
          label="???????"
          title="??????"
          description="??????????????????????????????????????????????"
          onOpen={() => onOpenReader('pain-point', selectedPainPoint.id)}
        />
      </article>
    </section>
  );
}

function EngineeringLogicView({
  engineeringLogic,
  projects,
  solutions,
  painPoints,
  onOpenReader,
}: {
  engineeringLogic: EngineeringLogic;
  projects: Project[];
  solutions: Solution[];
  painPoints: PainPoint[];
  onOpenReader: (kind: ReaderKind, id: string) => void;
}) {
  return (
    <section className="workspace single-column">
      <article className="detail-panel">
        <div className="eyebrow">工程主线</div>
        <h2>{engineeringLogic.title}</h2>
        <p className="lead">{engineeringLogic.summary}</p>
        <div className="fact-grid">
          <FactItem label="项目" value={String(projects.length)} />
          <FactItem label="方案" value={String(solutions.length)} />
          <FactItem label="痛点" value={String(painPoints.length)} />
          <FactItem label="当前焦点" value={String(engineeringLogic.currentFocus.length)} />
        </div>
        <div className="source-line">
          <span>来源文件</span>
          <strong>{engineeringLogic.sourceFile}</strong>
        </div>
        <div className="evidence-grid">
          <InfoBlock title="当前焦点" items={engineeringLogic.currentFocus} empty="暂无当前焦点" />
          <InfoBlock title="行动项" items={engineeringLogic.actions} empty="暂无行动项" />
          <InfoBlock title="推荐顺序" items={engineeringLogic.recommendedOrder ?? []} empty="暂无推荐顺序" />
          <InfoBlock title="风险边界" items={engineeringLogic.riskBoundaries ?? []} empty="暂无风险边界" />
        </div>
        <ReaderLaunchPanel
          label="工程逻辑全文阅读器"
          title="进入整页阅读"
          description="总纲文档更适合用整页阅读器慢慢读，不跟统计卡片和结构摘要混排在一层。"
          onOpen={() => onOpenReader('engineering-logic', 'engineering-logic')}
        />
      </article>
    </section>
  );
}

function SourcesView({
  sources,
  selectedSource,
  onSelect,
  onOpenReader,
}: {
  sources: SourceItem[];
  selectedSource: SourceItem;
  onSelect: (id: string) => void;
  onOpenReader: (kind: ReaderKind, id: string) => void;
}) {
  return (
    <section className="workspace two-column">
      <div className="list-panel">
        <div className="panel-title">
          <FileSearch size={18} />
          <span>外部资料源</span>
        </div>
        <div className="list-meta">不是资料越多越好，关键是它能不能补强项目判断、方案证据与痛点研究。</div>
        <div className="item-list">
          {sources.map((source) => (
            <button key={source.id} className={`item-card ${selectedSource.id === source.id ? 'selected' : ''}`} onClick={() => onSelect(source.id)}>
              <div className="card-row">
                <strong>{source.title}</strong>
                <div className="inline-badges">
                  <span className="badge">{source.sourceType}</span>
                  <span className={`badge severity-${source.evidenceStrength}`}>{strengthLabel(source.evidenceStrength)}</span>
                </div>
              </div>
              <p>{source.summary}</p>
              <TagList tags={[...source.relatedPainPoints, ...source.relatedPatterns].slice(0, 6)} />
            </button>
          ))}
        </div>
      </div>
      <article className="detail-panel">
        <div className="eyebrow">资料源导读</div>
        <h2>{selectedSource.title}</h2>
        <p className="lead">{selectedSource.summary}</p>
        <div className="source-line">
          <span>来源文件</span>
          <strong>{selectedSource.sourceFile}</strong>
        </div>
        <div className="evidence-grid">
          <InfoBlock title="证据强度" items={[strengthLabel(selectedSource.evidenceStrength)]} empty="暂无" />
          <InfoBlock title="关联痛点" items={selectedSource.relatedPainPoints} empty="暂无关联痛点" />
          <InfoBlock title="关联方案" items={selectedSource.relatedPatterns} empty="暂无关联方案" />
          <InfoBlock title="推荐用法" items={selectedSource.recommendedUse ? [selectedSource.recommendedUse] : []} empty="暂无推荐用法" />
          <InfoBlock title="当前行动项" items={selectedSource.actions} empty="暂无行动项" />
        </div>
        <ReaderLaunchPanel
          label="资料源全文阅读器"
          title="进入整页阅读"
          description="资料源的长文和案例摘录适合放到完整阅读器里，避免和摘要卡片混在同一屏。"
          onOpen={() => onOpenReader('source', selectedSource.id)}
        />
      </article>
    </section>
  );
}

function InterviewsView({
  items,
  selectedItem,
  onSelect,
}: {
  items: InterviewItem[];
  selectedItem: InterviewItem;
  onSelect: (id: string) => void;
}) {
  return (
    <section className="workspace two-column">
      <div className="list-panel">
        <div className="panel-title">
          <MessageSquareText size={18} />
          <span>面经列表</span>
        </div>
        <div className="list-meta">{items.length} 道题目，支持按项目、方案与痛点反复训练。</div>
        <div className="item-list">
          {items.map((item) => (
            <button key={item.id} className={`item-card ${selectedItem.id === item.id ? 'selected' : ''}`} onClick={() => onSelect(item.id)}>
              <strong>{item.rawQuestion}</strong>
              <TagList tags={[item.questionType, ...item.knowledgePoints]} />
            </button>
          ))}
        </div>
      </div>
      <article className="detail-panel">
        <div className="eyebrow">答题骨架</div>
        <h2>{selectedItem.rawQuestion}</h2>
        <TagList tags={[selectedItem.questionType, ...selectedItem.knowledgePoints]} />
        <section className="answer-box">
          <h3>推荐答法</h3>
          <p>{selectedItem.recommendedAnswer}</p>
        </section>
        <div className="evidence-grid">
          <InfoBlock title="继续追问" items={selectedItem.followUps} empty="暂无追问" />
          <InfoBlock title="关联项目" items={selectedItem.relatedProjects} empty="暂无关联项目" />
          <InfoBlock title="关联方案" items={selectedItem.relatedPatterns} empty="暂无关联方案" />
        </div>
      </article>
    </section>
  );
}

function InterviewerView({
  items,
  memory,
}: {
  items: InterviewItem[];
  memory: KnowledgeIndex['interviews']['memory'];
}) {
  const focusItems = items.slice(0, 4);
  return (
    <section className="workspace single-column">
      <div className="interviewer-panel">
        <div className="detail-header">
          <div>
            <div className="eyebrow">训练视图</div>
            <h2>围绕项目、痛点与方案反复练习表达</h2>
          </div>
          <BrainCircuit size={28} />
        </div>
        <div className="evidence-grid">
          <InfoBlock title="当前训练重点" items={[memory.focus]} empty="暂无" />
          <InfoBlock title="回答风格" items={[memory.answerStyle]} empty="暂无" />
          <InfoBlock title="薄弱点" items={memory.weakSpots} empty="暂无薄弱点" />
        </div>
        <div className="interviewer-grid">
          {focusItems.map((item) => (
            <div key={item.id} className="question-card">
              <span className="badge">{item.questionType}</span>
              <h3>{item.rawQuestion}</h3>
              <p>{item.recommendedAnswer}</p>
              <InfoBlock title="继续追问" items={item.followUps} empty="暂无追问" />
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

function RadarView({ projects }: { projects: Project[] }) {
  const sorted = [...projects].sort((a, b) => (b.score ?? 0) - (a.score ?? 0));
  const highScoreCount = sorted.filter((project) => (project.score ?? 0) >= 80).length;
  return (
    <section className="workspace single-column">
      <article className="detail-panel">
        <div className="eyebrow">雷达状态</div>
        <h2>候选样本与沉淀状态</h2>
        <p className="lead">高分项目不应该直接变成链接垃圾场，而要先评分、再候选、再沉淀、再反哺痛点与方案。</p>
        <div className="fact-grid">
          <FactItem label="总项目数" value={String(projects.length)} />
          <FactItem label="高分样本" value={String(highScoreCount)} />
          <FactItem label="深度沉淀" value={String(projects.filter((item) => item.status === '深度沉淀').length)} />
          <FactItem label="草稿" value={String(projects.filter((item) => item.status !== '深度沉淀').length)} />
        </div>
        <section className="radar-table">
          <div className="table-header">
            <span>项目</span>
            <span>状态</span>
            <span>评分</span>
            <span>类型</span>
          </div>
          {sorted.map((project) => (
            <div key={project.id} className="table-row">
              <strong>{project.name}</strong>
              <span>{project.status}</span>
              <span>{project.score ?? '-'}</span>
              <span>{project.types.slice(0, 3).join(' / ')}</span>
            </div>
          ))}
        </section>
      </article>
    </section>
  );
}

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

function DistillDeskView() {
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
      // ignore invalid history
    }
    const savedBridgeUrl = window.localStorage.getItem('knowledge-bridge-url');
    if (savedBridgeUrl) {
      setBridgeUrl(savedBridgeUrl);
    }
  }, []);

  const repoName = useMemo(() => parseGitHubRepo(intent.source), [intent.source]);
  const recommendedFolder = useMemo(() => recommendFolder(intent.goal), [intent.goal]);
  const codexPrompt = useMemo(() => buildDistillPrompt(intent, repoName, recommendedFolder), [intent, repoName, recommendedFolder]);
  const commandHints = useMemo(() => buildDistillCommands(intent, repoName, selectedAction), [intent, repoName, selectedAction]);
  const selectedActionMeta = distillActionMeta[selectedAction];

  async function writebackCurrentAnalysis() {
    if (!latestAnalysisResult) return;
    setExecutionState((current) => ({
      ...current,
      status: 'running',
      message: '正在把分析结果回写到 patterns / pain-points / interviews ...',
    }));
    try {
      const response = await fetch(`${bridgeUrl}/api/writeback-analysis`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(latestAnalysisResult),
      });
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
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
        ]
          .filter(Boolean)
          .join('\n'),
        result,
      });
    } catch (error) {
      setExecutionState((current) => ({
        ...current,
        status: 'error',
        message: error instanceof Error ? error.message : '回写失败',
      }));
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
    const entry: DistillHistoryEntry = {
      ...intent,
      id: `${Date.now()}`,
      createdAt: new Date().toLocaleString('zh-CN'),
    };
    const next = [entry, ...history].slice(0, 10);
    setHistory(next);
    if (typeof window !== 'undefined') {
      window.localStorage.setItem('knowledge-distill-history', JSON.stringify(next));
    }
  }

  function buildRequestPayload(action: DistillDeskAction) {
    if (action === 'ingest') {
      return {
        source: intent.source,
        sourceType: intent.sourceType,
        focus: intent.ingestFocus,
      };
    }
    return {
      ...intent,
      refresh: true,
      rebuildIndex: true,
      autoWriteback: intent.autoWriteback,
    };
  }

  async function executeCurrentIntent(action: DistillDeskAction = selectedAction) {
    const endpoint = action === 'ingest' ? '/api/ingest-repo' : action === 'analyze' ? '/api/analyze-project' : '/api/distill';
    setExecutionState({
      status: 'running',
      action,
      message: `正在执行：${distillActionMeta[action].title}`,
      result: null,
    });
    try {
      const response = await fetch(`${bridgeUrl}${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(buildRequestPayload(action)),
      });
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      const result = (await response.json()) as Record<string, unknown>;
      setExecutionState({
        status: 'done',
        action,
        message: buildExecutionMessage(action, result),
        result,
      });
      if (action === 'analyze') {
        setLatestAnalysisResult(result);
        const nextDocument = buildAnalyzeReaderDocument(result);
        if (nextDocument) {
          setAnalysisReaderDocument(nextDocument);
        }
      }
      if (action !== 'ingest') {
        saveCurrentIntent();
      }
    } catch (error) {
      setExecutionState({
        status: 'error',
        action,
        message: error instanceof Error ? error.message : '执行失败',
        result: null,
      });
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
          这里不再把“仓库理解、分析项目、正式沉淀”混成一个动作。你先定义来源，再决定这次要先看结构、先做判断，还是正式落库，平台会按这一层的目标给你不同结果。
        </p>

        <div className="distill-grid">
          <section className="distill-form">
            <div className="form-field">
              <label>桥接服务地址</label>
              <textarea
                value={bridgeUrl}
                onChange={(event) => {
                  const next = event.target.value;
                  setBridgeUrl(next);
                  if (typeof window !== 'undefined') {
                    window.localStorage.setItem('knowledge-bridge-url', next);
                  }
                }}
                placeholder="例如：http://127.0.0.1:8765"
              />
            </div>

            <div className="form-field">
              <label>来源地址或本地路径</label>
              <textarea
                value={intent.source}
                onChange={(event) => setIntent((current) => ({ ...current, source: event.target.value }))}
                placeholder="例如：https://github.com/owner/repo 或 D:\\pico 或 某篇博客 / 论文链接"
              />
            </div>

            <div className="form-field">
              <label>项目理解增强</label>
              <label className="checkbox-card">
                <input
                  type="checkbox"
                  checked={intent.useGitingest}
                  onChange={(event) => setIntent((current) => ({ ...current, useGitingest: event.target.checked }))}
                />
                <span>启用 Gitingest 深度理解，把仓库先转成 summary / tree / content 再进入沉淀</span>
              </label>
            </div>

            <div className="form-field">
              <label>自动回写闭环</label>
              <label className="checkbox-card">
                <input
                  type="checkbox"
                  checked={intent.autoWriteback}
                  onChange={(event) => setIntent((current) => ({ ...current, autoWriteback: event.target.checked }))}
                />
                <span>分析完成后默认自动回写到 patterns / pain-points / interviews，并立即重建索引</span>
              </label>
            </div>

            {intent.useGitingest ? (
              <div className="form-field">
                <label>Gitingest 聚焦目录（可选）</label>
                <textarea
                  value={intent.ingestFocus}
                  onChange={(event) => setIntent((current) => ({ ...current, ingestFocus: event.target.value }))}
                  placeholder="例如：src / packages/core / apps/web；留空表示全仓"
                />
              </div>
            ) : null}

            <div className="form-field">
              <label>来源类型</label>
              <div className="segmented">
                {[
                  ['github', 'GitHub 项目'],
                  ['local', '本地项目'],
                  ['article', '博客 / 论文 / 文档'],
                  ['legacy', '旧目录补写'],
                ].map(([value, label]) => (
                  <button
                    key={value}
                    className={intent.sourceType === value ? 'selected' : ''}
                    onClick={() => setIntent((current) => ({ ...current, sourceType: value as DistillIntent['sourceType'] }))}
                  >
                    {label}
                  </button>
                ))}
              </div>
            </div>

            <div className="form-field">
              <label>这次最主要的沉淀目标</label>
              <div className="segmented">
                {[
                  ['project', '项目沉淀'],
                  ['pattern', '方案抽象'],
                  ['pain-point', '痛点补强'],
                  ['interview', '面试训练'],
                  ['frontend', '前端风格'],
                ].map(([value, label]) => (
                  <button
                    key={value}
                    className={intent.goal === value ? 'selected' : ''}
                    onClick={() => setIntent((current) => ({ ...current, goal: value as DistillIntent['goal'] }))}
                  >
                    {label}
                  </button>
                ))}
              </div>
            </div>

            <div className="form-field">
              <label>你更希望这次偏哪种写法</label>
              <div className="segmented">
                {[
                  ['article', '文章感深读'],
                  ['engineering', '工程判断'],
                  ['interview', '面试表达'],
                  ['product', '平台产品化'],
                ].map(([value, label]) => (
                  <button
                    key={value}
                    className={intent.style === value ? 'selected' : ''}
                    onClick={() => setIntent((current) => ({ ...current, style: value as DistillIntent['style'] }))}
                  >
                    {label}
                  </button>
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
              <textarea
                value={intent.extraNotes}
                onChange={(event) => setIntent((current) => ({ ...current, extraNotes: event.target.value }))}
                placeholder="例如：重点看源码、要补面试追问、参考黄同学h写法、顺便回写痛点页"
              />
            </div>

            <div className="form-field">
              <label>这一步想先做什么</label>
              <div className="distill-action-grid">
                {(Object.entries(distillActionMeta) as Array<[DistillDeskAction, (typeof distillActionMeta)[DistillDeskAction]]>).map(([key, meta]) => (
                  <button
                    key={key}
                    type="button"
                    className={`distill-action-card ${selectedAction === key ? 'selected' : ''}`}
                    onClick={() => setSelectedAction(key)}
                  >
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
              <button type="button" className="ghost-button" onClick={saveCurrentIntent}>
                保存到本地草稿
              </button>
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
                    <button
                      type="button"
                      className="ghost-button"
                      onClick={() => {
                        const nextDocument = buildAnalyzeReaderDocument(latestAnalysisResult);
                        if (!nextDocument && latestAnalysisResult) {
                          const fallbackDocument = buildAnalyzeReaderDocument(latestAnalysisResult);
                          if (fallbackDocument) {
                            setAnalysisReaderDocument(fallbackDocument);
                          }
                          return;
                        }
                        if (nextDocument) {
                          setAnalysisReaderDocument(nextDocument);
                        }
                      }}
                    >
                      打开分析阅读器
                    </button>
                    <button type="button" className="ghost-button" onClick={writebackCurrentAnalysis}>
                      一键回写
                    </button>
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
                  <p>
                    {goalLabel(entry.goal)} / {styleLabel(entry.style)} / {entry.outputs.join('、')}
                  </p>
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

function FeedbackSummaryView() {
  const entries = useFeedbackEntries();
  return (
    <section className="workspace single-column">
      <article className="detail-panel">
        <div className="eyebrow">阅读反馈汇总</div>
        <h2>你在文档阅读中留下的判断</h2>
        <p className="lead">这些反馈会反过来影响平台的后续改写、面试追问和内容补强优先级。</p>
        {entries.length ? (
          <div className="feedback-reference-list">
            {entries.map((entry) => (
              <div key={entry.key} className={`feedback-reference-card ${entry.vote === 'needs-work' ? 'needs-work' : ''}`}>
                <div className="card-row">
                  <strong>{entry.title}</strong>
                  <span className={`badge ${entry.vote === 'needs-work' ? 'draft' : 'good'}`}>{entry.vote === 'needs-work' ? '需补强' : '有帮助'}</span>
                </div>
                <p>{entry.note || '暂无备注'}</p>
                <div className="search-hint">
                  <span>来源文件</span>
                  <strong>{entry.sourceFile || '未知'}</strong>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="muted">暂时还没有阅读反馈。你在文档阅读器里保存反馈后，这里会自动汇总。</p>
        )}
      </article>
    </section>
  );
}

function VisualGenerationView() {
  return (
    <section className="workspace single-column">
      <article className="detail-panel">
        <div className="eyebrow">视觉生成</div>
        <h2>中文页面设计与生成工作流</h2>
        <p className="lead">把 DESIGN.md、前端风格样本、生成图和真实 DOM 实现串成稳定工作流，而不是只看单次截图效果。</p>
        <div className="evidence-grid">
          <InfoBlock
            title="当前重点"
            items={[
              '先沉淀中文页面的版式、信息密度和阅读体验规则。',
              '把优质前端项目的风格判断回写到 DESIGN.md。',
              '让生成图、真实 React 页面和最终截图校验形成闭环。',
            ]}
            empty="暂无"
          />
          <InfoBlock
            title="后续动作"
            items={[
              '继续补充优质前端样本。',
              '把可复用的页面结构抽成组件规范。',
              '让平台页面更像真正的阅读产品，而不是文档壳。',
            ]}
            empty="暂无"
          />
        </div>
      </article>
    </section>
  );
}

type ReaderDocument = {
  kind: ReaderKind;
  id: string;
  title: string;
  eyebrow: string;
  summary: string;
  sourceFile: string;
  content: string;
  badges: string[];
  quickFacts: Array<{ label: string; value: string }>;
  guideCards: Array<{ title: string; body: string }>;
  actionItems: string[];
};

function buildAnalyzeReaderDocument(result: Record<string, unknown>): ReaderDocument | null {
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
  const actions = Array.isArray(analysis.actions) ? analysis.actions.map((item) => String(item)) : [];
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

${actions.map((item) => `- ${item}`).join('\n')}
`;

  return {
    kind: 'project',
    id: `analysis-${slugify(title || source)}` ,
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

function FullReaderView({ document, onClose }: { document: ReaderDocument; onClose: () => void }) {
  const docId = slugify(`${document.title}-${document.sourceFile}`) ? `doc-${slugify(`${document.title}-${document.sourceFile}`)}` : 'document';
  const outline = extractReaderHeadings(document.content);
  const quickJumps = [
    { id: 'reader-hero', label: '概览' },
    { id: 'reader-guides', label: '导读' },
    { id: docId, label: '正文' },
    ...(document.actionItems.length ? [{ id: 'reader-actions', label: '行动项' }] : []),
  ];

  return (
    <section className="reader-screen">
      <div className="reader-screen-topbar">
        <button type="button" className="ghost-button" onClick={onClose}>
          <ArrowLeft size={16} />
          <span>返回上一页</span>
        </button>
        <div className="reader-screen-actions">
          {quickJumps.map((jump) => (
            <button key={jump.id} type="button" className="ghost-button compact-button" onClick={() => scrollToElement(jump.id)}>
              {jump.label}
            </button>
          ))}
          <span className="badge good">完整阅读器</span>
          <span className="badge">{document.eyebrow}</span>
        </div>
      </div>

      <div className="reader-screen-layout">
        <div className="reader-main-column">
          <div id="reader-hero" className="reader-hero-card">
            <div className="eyebrow">{document.eyebrow}</div>
            <h1>{document.title}</h1>
            <p>{document.summary}</p>
            <div className="reader-badge-row">
              <TagList tags={document.badges} />
            </div>
          </div>

          <div id="reader-guides" className="reader-guide-grid">
            {document.guideCards.map((card) => (
              <section key={card.title} className="reader-guide-card">
                <h3>{card.title}</h3>
                <p>{card.body}</p>
              </section>
            ))}
          </div>

          <div className="reader-article-shell">
            <div className="reader-article-topline">
              <span>来源文件</span>
              <strong>{document.sourceFile}</strong>
            </div>
            <MarkdownPreview
              title={document.title}
              content={document.content}
              sourceFile={document.sourceFile}
              showHeader={false}
              showOutline={false}
              showFeedback={false}
            />
          </div>

          {document.actionItems.length ? (
            <section id="reader-actions" className="reader-action-card">
              <div className="eyebrow">行动收束</div>
              <h3>把这次阅读继续变成项目动作</h3>
              <ul className="reader-side-list">
                {document.actionItems.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </section>
          ) : null}
        </div>

        <aside className="reader-side">
          <div className="reader-side-block">
            <div className="eyebrow">阅读摘要</div>
            <h2>{document.title}</h2>
            <p>{document.summary}</p>
          </div>

          <div className="reader-side-block">
            <strong>快速信息</strong>
            <div className="reader-fact-list">
              {document.quickFacts.map((fact) => (
                <div key={`${fact.label}-${fact.value}`} className="reader-fact-row">
                  <span>{fact.label}</span>
                  <strong>{fact.value}</strong>
                </div>
              ))}
            </div>
          </div>

          <div className="reader-side-block">
            <strong>目录跳转</strong>
            {outline.length ? (
              <div className="reader-outline-list">
                {outline.map((heading) => (
                  <button
                    key={`${heading.id}-${heading.level}`}
                    type="button"
                    className={`reader-outline-link level-${heading.level}`}
                    onClick={() => scrollToElement(heading.id)}
                  >
                    {heading.text}
                  </button>
                ))}
              </div>
            ) : (
              <p className="muted">当前文档还没有可跳转标题。</p>
            )}
          </div>

          <div className="reader-side-block">
            <strong>当前落点</strong>
            <p className="reader-source-file">{document.sourceFile}</p>
          </div>
        </aside>
      </div>
    </section>
  );
}

function ReaderLaunchPanel({
  label,
  title,
  description,
  onOpen,
}: {
  label: string;
  title: string;
  description: string;
  onOpen: () => void;
}) {
  return (
    <section className="reader-launch-panel">
      <div>
        <div className="eyebrow">{label}</div>
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
            <button type="button" className="primary-button" onClick={onOpen}>
        打开完整阅读器
      </button>
    </section>
  );
}

function SearchResults({ results, onOpen }: { results: SearchItem[]; onOpen: (item: SearchItem) => void }) {
  return (
    <section className="search-results">
      <div className="panel-title">
        <Search size={18} />
        <span>搜索结果</span>
      </div>
      <div className="list-meta">{results.length} 条命中</div>
      <div className="search-result-grid">
        {results.map((item) => (
          <button key={item.id} className="search-result-card" onClick={() => onOpen(item)}>
            <div className="card-row">
              <strong>{item.title}</strong>
              <span className="badge">{kindLabel(item.kind)}</span>
            </div>
            <p>{item.summary || item.context || '暂无摘要'}</p>
            {item.tags.length ? <TagList tags={item.tags.slice(0, 4)} /> : null}
            <div className="search-hint">
              <span>命中位置</span>
              <strong>{item.sourceFile}</strong>
            </div>
          </button>
        ))}
      </div>
    </section>
  );
}

function StatusBadge({ status }: { status: string }) {
  const tone = status === '深度沉淀' ? 'good' : status === '草稿' ? 'draft' : '';
  return <span className={`badge ${tone}`}>{status}</span>;
}

function TagList({ tags }: { tags: string[] }) {
  if (!tags.length) return null;
  return (
    <div className="tags">
      {tags.map((tag) => (
        <span key={tag} className="tag">
          {tag}
        </span>
      ))}
    </div>
  );
}

function LearningGuide({ title, items }: { title: string; items: string[] }) {
  return (
    <section className="learning-guide">
      <h3>{title}</h3>
      <div className="learning-steps">
        {items.map((item, index) => (
          <div key={item} className="learning-step">
            <span className="step-index">{index + 1}</span>
            <p>{item}</p>
          </div>
        ))}
      </div>
    </section>
  );
}

function InfoBlock({ title, items, empty }: { title: string; items: string[]; empty: string }) {
  return (
    <section className="info-block">
      <h3>{title}</h3>
      {items.length ? (
        <ul>
          {items.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      ) : (
        <p className="muted">{empty}</p>
      )}
    </section>
  );
}

function FactItem({ label, value }: { label: string; value: string }) {
  return (
    <div className="fact-item">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

function OverviewMeta({ label, value }: { label: string; value: string }) {
  return (
    <div className="overview-meta-item">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

function buildProjectPressurePrompt(project: Project) {
  return `如果你把 ${project.name} 放进学习样本里，继续追问通常会落到三个问题上：它真正解决了什么工程边界、为什么这个做法值得迁移、以及它对你当前平台的下一步设计到底有什么启发。`;
}

function buildProjectTakeaway(project: Project) {
  if (project.relatedPatterns.length) {
    return `${project.name} 最值得学的不是功能数量，而是它如何把 ${project.relatedPatterns.slice(0, 2).join(' / ')} 这些问题落成可执行的工程做法。继续往下读时，要重点看它的边界判断、证据链和可迁移动作。`;
  }
  return `${project.name} 最值得学的不是表面功能，而是它到底把哪个真实工程问题做成了可迁移样本。继续看时，优先追问它解决了什么边界问题、留下了什么证据、对当前平台有什么行动启发。`;
}

function buildProjectMisreadWarning(project: Project) {
  if (project.primaryCategory === 'Agent Runtime') {
    return `最容易把 ${project.name} 误读成“又一个会调模型的工具”。真正该看的是它有没有把运行边界、恢复协议、工具副作用和上下文治理做成正式结构。`;
  }
  if (project.primaryCategory === 'Frontend Design' || project.primaryCategory === 'Workbench UI') {
    return `最容易把 ${project.name} 误读成“风格不错的页面样本”。真正该看的是它如何把设计约束、信息密度和阅读路径固化成可复用规则。`;
  }
  if (project.primaryCategory === 'MCP' || project.primaryCategory === 'Tool Runtime') {
    return `最容易把 ${project.name} 误读成“接了更多工具”。真正该看的是它怎么处理权限、结果治理、可追踪性和失败恢复。`;
  }
  return `最容易的误区是只看功能表面，不看它为什么这样拆、代价是什么、哪些做法其实并不适合直接照搬。`;
}

function buildProjectOralAnswer(project: Project) {
  return `如果面试里要用一句比较顺的口语去讲 ${project.name}，我会先把它定义成一个${project.primaryCategory}样本，然后重点说它不是表面功能多，而是它把 ${project.businessScenario} 这类场景里的关键边界收进了正式工程结构。`;
}

function buildProjectEngineeringPitch(project: Project) {
  return `如果用三分钟讲工程，我会先讲 ${project.name} 解决的真实场景，再讲它最值钱的亮点是 ${project.biggestHighlight}，然后落到它怎样把运行边界、证据链和后续行动项组织起来。这样讲不会停留在功能介绍，而会更像真实项目复盘。`;
}

function escapeRegExp(value: string) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function extractMarkdownSection(content: string, headings: string[]) {
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

function buildProjectDeepDiveMarkdown(project: Project) {
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

  return blocks.join('\n\n') || `## 深度拆解待补充\n\n当前项目的正文结构还没有被完整沉淀，后续需要补齐“通用问题、具体做法、步骤和行动项”。`;
}

function buildSolutionDeepDiveMarkdown(solution: Solution) {
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
    `## 深度拆解待补充\n\n当前方案还缺少“典型结构、成熟做法、误区和行动项”的完整正文，后续需要优先补齐。`
  );
}

function buildSolutionPressurePrompt(solution: Solution) {
  return `继续追问时，真正的问题通常不是“这个方案是什么”，而是“为什么普通做法不够、它适合什么边界、代价又是什么”。`;
}

function buildSolutionTakeaway(solution: Solution) {
  if (solution.maturePractices.length) {
    return `${solution.title} 这页最该带走的不是术语，而是成熟系统通常会用哪些固定机制来稳定解决这类问题。`;
  }
  return `${solution.title} 这页最该带走的是：先定义通用问题，再决定方案，而不是先堆实现名词。`;
}

function buildPainPointPressurePrompt(painPoint: PainPoint) {
  return `?????????????????????${painPoint.title}?????????????????????????????????????????????`;
}

function buildPainPointTakeaway(painPoint: PainPoint) {
  return `??${painPoint.title}????????????????????????????????????????????????????????????????`;
}

function buildPainPointDeepDiveMarkdown(painPoint: PainPoint, projects: Project[]) {
  return painPoint.content?.trim() || buildPainPointDocument(painPoint, projects);
}

function buildPainPointDocument(painPoint: PainPoint, projects: Project[]) {
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
    `??????????${projects.length} ?`,
    `???????${evidenceCount} ?`,
    `???????${relatedProjects.length} ?`,
    `?????${(painPoint.evidenceSources ?? []).join(' / ') || '???'}`,
    `?????${commonPractices.length} ?`,
    `??????${painPoint.commonMistakes.length} ?`,
    `??????${painPoint.actions.length} ?`,
    `???????${lastUpdatedFromProjects.join(' / ') || '??'}`,
    `???????${painPoint.lastUpdatedAt || '??'}`,
  ];

  return `# ?????${painPoint.title}

> ????????????????????????????????????????????????????????????????????????????????

## 1. ????????????

${painPoint.industryPain || painPoint.solutionMethod}

??????????????????????????????????????????????????????????????????????????????????????????????????????

## 2. ????????????

${metricLines.map((item) => `- ${item}`).join(lineBreak)}

## 3. ?????????

${painPoint.solutionMethod}

## 4. ?????????

${practices.length ? practices.map((project) => `### ${project.name}

- ????${project.primaryCategory}
- ?????${project.types.join(' / ')}
- ?????${project.status}
- ?????${project.score ?? '??'}
- ??????????${project.summary || '??????????????????'}
- ?????${project.relatedPatterns.length ? project.relatedPatterns.join('?') : '???'}
- ???????????????????????????????????${painPoint.topic}????????????????????????????`).join(doubleLineBreak) : '??????????????????'}

## 5. ????????????

${commonPractices.length ? commonPractices.map((item) => `- ${item}`).join(lineBreak) : '- ?????????????? GitHub????????????????'}

## 6. ????????????

${(painPoint.dataSignals ?? []).length ? painPoint.dataSignals!.map((item) => `- ${item}`).join(lineBreak) : '- ????????????????????????????????'}

## 7. ?????????

${painPoint.commonMistakes.length ? painPoint.commonMistakes.map((item) => `- ${item}`).join(lineBreak) : '- ???????'}

## 8. ???????????

- ????????????????????????????????????
- ?????????????????????????????????
- ??????????????????????????????????????????

## 9. ??????

${painPoint.evolutionRule || '??????????????????????????????????????????????????????'}

## 10. ??????????

${painPoint.actions.length ? painPoint.actions.map((item) => `- [ ] ${item}`).join(lineBreak) : '- [ ] ?????????'}
`;
}

function buildReaderDocument(
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
        eyebrow: '??????',
        summary: painPoint.industryPain || painPoint.solutionMethod,
        sourceFile: painPoint.sourceFile ?? painPoint.id,
        content: buildPainPointDeepDiveMarkdown(painPoint, projects),
        badges: [painPoint.topic, painPoint.severity, ...(painPoint.evidenceSources ?? [])],
        quickFacts: [
          { label: '??', value: painPoint.topic },
          { label: '???', value: severityLabel(painPoint.severity) },
          { label: '????', value: String(painPoint.evidenceProjectCount ?? painPoint.evidenceProjects.length) },
          { label: '???', value: String(painPoint.actions.length) },
        ],
        guideCards: [
          { title: '????????', body: painPoint.industryPain || '??' },
          { title: '?????????', body: painPoint.solutionMethod },
          { title: '???????', body: commonPractices.join('?') || '??' },
          { title: '????', body: (painPoint.dataSignals ?? []).join('?') || '??' },
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

function parseReaderHash(hash: string): ReaderTarget | null {
  const trimmed = hash.replace(/^#/, '');
  const match = trimmed.match(/^reader\/(project|solution|pain-point|source|engineering-logic)\/(.+)$/);
  if (!match) return null;
  return { kind: match[1] as ReaderKind, id: decodeURIComponent(match[2]) };
}

function scrollToElement(id: string) {
  document.getElementById(id)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function slugify(value: string) {
  return value
    .toLowerCase()
    .replace(/[^\w\u4e00-\u9fa5]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

function extractReaderHeadings(content: string) {
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

function kindLabel(kind: SearchItem['kind']) {
  switch (kind) {
    case 'project':
      return '项目';
    case 'solution':
      return '方案';
    case 'painPoint':
      return '痛点';
    case 'source':
      return '资料源';
    case 'interview':
      return '面经';
    default:
      return '内容';
  }
}

function severityLabel(severity: PainPoint['severity']) {
  switch (severity) {
    case 'high':
      return '高';
    case 'medium':
      return '中';
    case 'low':
      return '低';
    default:
      return severity;
  }
}

function strengthLabel(strength: SourceItem['evidenceStrength']) {
  switch (strength) {
    case 'high':
      return '高';
    case 'medium':
      return '中';
    case 'low':
      return '低';
    default:
      return strength;
  }
}

function parseGitHubRepo(source: string) {
  const match = source.match(/github\.com\/([^/\s]+)\/([^/\s?#]+)/i);
  if (!match) return '';
  return `${match[1]}/${match[2].replace(/\.git$/i, '')}`;
}

function recommendFolder(goal: DistillIntent['goal']) {
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

function goalLabel(goal: DistillIntent['goal']) {
  switch (goal) {
    case 'project':
      return '项目沉淀';
    case 'pattern':
      return '方案抽象';
    case 'pain-point':
      return '痛点补强';
    case 'interview':
      return '面试训练';
    case 'frontend':
      return '前端风格';
    default:
      return goal;
  }
}

function styleLabel(style: DistillIntent['style']) {
  switch (style) {
    case 'article':
      return '文章感深读';
    case 'engineering':
      return '工程判断';
    case 'interview':
      return '面试表达';
    case 'product':
      return '平台产品化';
    default:
      return style;
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
    if (!result.analysis) {
      return JSON.stringify(result, null, 2);
    }
    const analysis = (result.analysis as Record<string, unknown> | undefined) ?? {};
    return JSON.stringify(
      {
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
      },
      null,
      2,
    );
  }
  return JSON.stringify(result, null, 2);
}

function buildDistillPrompt(intent: DistillIntent, repoName: string, recommendedFolder: string) {
  const sourceLabel =
    intent.sourceType === 'github'
      ? 'GitHub 项目'
      : intent.sourceType === 'local'
        ? '本地项目'
        : intent.sourceType === 'article'
          ? '博客 / 论文 / 文档'
          : '旧目录补写';
  const outputText = intent.outputs.length ? intent.outputs.join('、') : '项目沉淀文档';
  const repoHint = repoName ? `如果适用，优先参考仓库 ${repoName} 的源码、README、docs、examples 和 changelog。` : '';
  const ingestHint = intent.useGitingest
    ? `这次先用 Gitingest 做仓库理解增强${intent.ingestFocus.trim() ? `，聚焦目录是 ${intent.ingestFocus.trim()}。` : '，默认看全仓。'}请优先利用 summary、directory tree 和 content 来理解结构，而不是只看 README。`
    : '这次先按常规方式阅读 README、docs 和关键源码，不强制使用 Gitingest。';
  const styleHint =
    intent.style === 'article'
      ? '写法要更像真正有文章感的深读内容，先立题，再讲场景压力、判断、误区、证据和行动项。'
      : intent.style === 'engineering'
        ? '重点写工程边界、取舍、约束、验证信号和为什么普通做法不够。'
        : intent.style === 'interview'
          ? '重点补口语版回答、三分钟工程讲法、面试官追问和容易被问爆的点。'
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
  ]
    .filter(Boolean)
    .join('\n');
}

function useFeedbackEntries() {
  const [entries, setEntries] = useState<Array<{ key: string; title: string; sourceFile: string; vote: string | null; note: string }>>([]);

  useEffect(() => {
    if (typeof window === 'undefined') return;
    const collected: Array<{ key: string; title: string; sourceFile: string; vote: string | null; note: string }> = [];
    for (let index = 0; index < window.localStorage.length; index += 1) {
      const key = window.localStorage.key(index);
      if (!key || !key.startsWith('knowledge-feedback:')) continue;
      const raw = window.localStorage.getItem(key);
      if (!raw) continue;
      try {
        const parsed = JSON.parse(raw) as { title?: string; sourceFile?: string; vote?: string | null; note?: string };
        collected.push({
          key,
          title: parsed.title || key.replace('knowledge-feedback:', ''),
          sourceFile: parsed.sourceFile || '',
          vote: parsed.vote ?? null,
          note: parsed.note || '',
        });
      } catch {
        // ignore invalid entries
      }
    }
    setEntries(collected.sort((a, b) => a.title.localeCompare(b.title, 'zh-CN')));
  }, []);

  return entries;
}

const root = createRoot(document.getElementById('root')!);
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
