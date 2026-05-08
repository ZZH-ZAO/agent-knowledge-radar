import React, { Suspense, lazy, useEffect, useMemo, useState } from 'react';
import { Search, Sparkles } from 'lucide-react';
import rawData from './data/knowledge-index.json';
import type { KnowledgeIndex, SearchItem } from './types';
import type { View, ReaderKind, ReaderTarget } from './constants';
import { navItems, viewMeta } from './constants';
import { buildReaderDocument, parseReaderHash } from './utils';
import { SearchResults } from './components/SharedComponents';
import { FullReaderView } from './components/FullReaderView';
import { DistillDeskView } from './pages/DistillDeskView';
import { ProjectsView } from './pages/ProjectsView';
import { SolutionsView } from './pages/SolutionsView';
import { PainPointsView } from './pages/PainPointsView';
import { EngineeringLogicView, SourcesView, InterviewsView, InterviewerView, RadarView, FeedbackSummaryView, VisualGenerationView } from './pages/OtherViews';

const data = rawData as KnowledgeIndex;

export default function App() {
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
