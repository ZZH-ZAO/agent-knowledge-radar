import React, { Suspense, lazy, useEffect, useMemo, useState } from 'react';
import { BrowserRouter, Routes, Route, useParams, useNavigate, Navigate, useLocation } from 'react-router-dom';
import { Search, Sparkles } from 'lucide-react';
import rawData from './data/knowledge-index.json';
import type { KnowledgeIndex, SearchItem } from './types';
import type { View, ReaderKind, ReaderTarget } from './constants';
import { navItems, viewMeta } from './constants';
import { buildReaderDocument } from './utils';
import { SearchResults } from './components/SharedComponents';
import { FullReaderView } from './components/FullReaderView';
import { DistillDeskView } from './pages/DistillDeskView';
import { ProjectsView } from './pages/ProjectsView';
import { SolutionsView } from './pages/SolutionsView';
import { PainPointsView } from './pages/PainPointsView';
import { EngineeringLogicView, SourcesView, InterviewsView, InterviewerView, RadarView, FeedbackSummaryView, VisualGenerationView } from './pages/OtherViews';
import { KnowledgeGraph } from './components/KnowledgeGraph';
import { CompareView } from './pages/CompareView';
import { LearningPathView } from './pages/LearningPathView';
import { buildGraphData } from './utils';

const data = rawData as KnowledgeIndex;

const viewToPath: Record<View, string> = {
  'distill-desk': '/distill-desk',
  projects: '/projects',
  solutions: '/solutions',
  'pain-points': '/pain-points',
  'engineering-logic': '/engineering-logic',
  sources: '/sources',
  interviews: '/interviews',
  interviewer: '/interviewer',
  radar: '/radar',
  feedback: '/feedback',
  'visual-generation': '/visual-generation',
  graph: '/graph',
  compare: '/compare',
  'learning-path': '/learning-path',
};

function pathToView(pathname: string): View {
  const match = Object.entries(viewToPath).find(([, path]) => pathname.startsWith(path));
  return match ? match[0] as View : 'projects';
}

export default function App() {
  return (
    <BrowserRouter>
      <AppShell />
    </BrowserRouter>
  );
}

function AppShell() {
  const location = useLocation();
  const navigate = useNavigate();
  const [query, setQuery] = useState('');
  const [readerTarget, setReaderTarget] = useState<ReaderTarget | null>(null);

  const view = pathToView(location.pathname);

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
    if (typeof window === 'undefined') return;
    const applyHash = () => {
      const hash = window.location.hash;
      if (!hash.startsWith('#reader/')) {
        setReaderTarget(null);
        return;
      }
      const parts = hash.replace('#reader/', '').split('/');
      if (parts.length >= 2) {
        const kind = parts[0] as ReaderKind;
        const id = decodeURIComponent(parts.slice(1).join('/'));
        setReaderTarget({ kind, id });
      }
    };
    applyHash();
    window.addEventListener('hashchange', applyHash);
    return () => window.removeEventListener('hashchange', applyHash);
  }, []);

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
        navigate(`/projects/${item.entityId}`);
        break;
      case 'solution':
        navigate(`/solutions/${item.entityId}`);
        break;
      case 'painPoint':
        navigate(`/pain-points/${item.entityId}`);
        break;
      case 'source':
        navigate(`/sources/${item.entityId}`);
        break;
      case 'interview':
        navigate(`/interviews/${item.entityId}`);
        break;
      default:
        break;
    }
    setQuery('');
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
                onClick={() => navigate(viewToPath[item.id])}
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
          <Routes>
            <Route path="/" element={<Navigate to="/projects" replace />} />
            <Route path="/distill-desk" element={<DistillDeskView />} />
            <Route path="/projects" element={<ProjectsListRoute onOpenReader={openReader} />} />
            <Route path="/projects/:id" element={<ProjectsDetailRoute onOpenReader={openReader} />} />
            <Route path="/solutions" element={<SolutionsRoute onOpenReader={openReader} />} />
            <Route path="/solutions/:id" element={<SolutionsRoute onOpenReader={openReader} />} />
            <Route path="/pain-points" element={<PainPointsRoute onOpenReader={openReader} />} />
            <Route path="/pain-points/:id" element={<PainPointsRoute onOpenReader={openReader} />} />
            <Route path="/engineering-logic" element={<EngineeringLogicView engineeringLogic={data.engineeringLogic} projects={data.projects} solutions={data.solutions} painPoints={data.painPoints} onOpenReader={openReader} />} />
            <Route path="/sources" element={<SourcesRoute onOpenReader={openReader} />} />
            <Route path="/sources/:id" element={<SourcesRoute onOpenReader={openReader} />} />
            <Route path="/interviews" element={<InterviewsRoute />} />
            <Route path="/interviews/:id" element={<InterviewsRoute />} />
            <Route path="/interviewer" element={<InterviewerView items={data.interviews.items} memory={data.interviews.memory} />} />
            <Route path="/radar" element={<RadarView projects={data.projects} />} />
            <Route path="/feedback" element={<FeedbackSummaryView />} />
            <Route path="/visual-generation" element={<VisualGenerationView />} />
            <Route path="/graph" element={<GraphRoute />} />
            <Route path="/compare" element={<CompareView projects={data.projects} />} />
            <Route path="/learning-path" element={<LearningPathView projects={data.projects} solutions={data.solutions} painPoints={data.painPoints} />} />
          </Routes>
        </Suspense>
          </>
        )}
      </main>
    </div>
  );
}

function ProjectsListRoute({ onOpenReader }: { onOpenReader: (kind: ReaderKind, id: string) => void }) {
  const navigate = useNavigate();
  const [selectedType, setSelectedType] = useState('全部');

  const projectTypes = useMemo(() => {
    const set = new Set<string>();
    data.projects.forEach((project) => project.types.forEach((type) => set.add(type)));
    return ['全部', ...Array.from(set).sort((a, b) => a.localeCompare(b, 'zh-CN'))];
  }, []);

  const filteredProjects = useMemo(() => {
    return data.projects.filter((project) => selectedType === '全部' || project.types.includes(selectedType));
  }, [selectedType]);

  const selectedProject = filteredProjects[0] ?? data.projects[0];

  return (
    <ProjectsView
      projects={filteredProjects}
      selectedProject={selectedProject}
      projectTypes={projectTypes}
      selectedType={selectedType}
      mode="overview"
      onTypeChange={setSelectedType}
      onOpenDetail={(id) => navigate(`/projects/${id}`)}
      onBackToOverview={() => navigate('/projects')}
      onOpenReader={onOpenReader}
    />
  );
}

function ProjectsDetailRoute({ onOpenReader }: { onOpenReader: (kind: ReaderKind, id: string) => void }) {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [selectedType, setSelectedType] = useState('全部');

  const projectTypes = useMemo(() => {
    const set = new Set<string>();
    data.projects.forEach((project) => project.types.forEach((type) => set.add(type)));
    return ['全部', ...Array.from(set).sort((a, b) => a.localeCompare(b, 'zh-CN'))];
  }, []);

  const selectedProject = data.projects.find((p) => p.id === id) ?? data.projects[0];

  return (
    <ProjectsView
      projects={data.projects}
      selectedProject={selectedProject}
      projectTypes={projectTypes}
      selectedType={selectedType}
      mode="detail"
      onTypeChange={setSelectedType}
      onOpenDetail={(id) => navigate(`/projects/${id}`)}
      onBackToOverview={() => navigate('/projects')}
      onOpenReader={onOpenReader}
    />
  );
}

function SolutionsRoute({ onOpenReader }: { onOpenReader: (kind: ReaderKind, id: string) => void }) {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const selectedSolution = data.solutions.find((s) => s.id === id) ?? data.solutions[0];

  return (
    <SolutionsView
      solutions={data.solutions}
      selectedSolution={selectedSolution}
      onSelect={(id) => navigate(`/solutions/${id}`)}
      onOpenReader={onOpenReader}
    />
  );
}

function PainPointsRoute({ onOpenReader }: { onOpenReader: (kind: ReaderKind, id: string) => void }) {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const selectedPainPoint = data.painPoints.find((p) => p.id === id) ?? data.painPoints[0];

  return (
    <PainPointsView
      painPoints={data.painPoints}
      selectedPainPoint={selectedPainPoint}
      projects={data.projects}
      onSelect={(id) => navigate(`/pain-points/${id}`)}
      onOpenReader={onOpenReader}
    />
  );
}

function SourcesRoute({ onOpenReader }: { onOpenReader: (kind: ReaderKind, id: string) => void }) {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const selectedSource = data.sources.find((s) => s.id === id) ?? data.sources[0];

  return (
    <SourcesView
      sources={data.sources}
      selectedSource={selectedSource}
      onSelect={(id) => navigate(`/sources/${id}`)}
      onOpenReader={onOpenReader}
    />
  );
}

function InterviewsRoute() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const selectedInterview = data.interviews.items.find((i) => i.id === id) ?? data.interviews.items[0];

  return (
    <InterviewsView
      items={data.interviews.items}
      selectedItem={selectedInterview}
      onSelect={(id) => navigate(`/interviews/${id}`)}
    />
  );
}

function GraphRoute() {
  const graphData = useMemo(
    () => buildGraphData(data.projects, data.solutions, data.painPoints, data.sources, data.interviews.items),
    [],
  );
  return <KnowledgeGraph data={graphData} />;
}
