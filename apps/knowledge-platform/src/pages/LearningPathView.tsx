import React, { useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { BookOpen, CheckCircle2, Circle, ChevronRight } from 'lucide-react';
import type { Project, Solution, PainPoint } from '../types';
import { TagList } from '../components/SharedComponents';

type PathNode = {
  id: string;
  title: string;
  description: string;
  kind: 'project' | 'solution' | 'painPoint';
  route: string;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  tags: string[];
};

type LearningPath = {
  id: string;
  title: string;
  description: string;
  nodes: PathNode[];
};

function buildLearningPaths(
  projects: Project[],
  solutions: Solution[],
  painPoints: PainPoint[],
): LearningPath[] {
  const highScoreProjects = [...projects].filter((p) => (p.score ?? 0) >= 70).sort((a, b) => (b.score ?? 0) - (a.score ?? 0));
  const allProjects = [...projects].sort((a, b) => (b.score ?? 0) - (a.score ?? 0));

  return [
    {
      id: 'beginner',
      title: '入门路径：从概念到第一个项目',
      description: '适合刚开始接触 Agent 工程的同学。先理解行业痛点，再看方案框架，最后用高分项目验证理解。',
      nodes: [
        ...painPoints.slice(0, 3).map((pp): PathNode => ({
          id: pp.id,
          title: pp.title,
          description: pp.industryPain || pp.solutionMethod,
          kind: 'painPoint',
          route: `/pain-points/${pp.id}`,
          difficulty: 'beginner',
          tags: [pp.topic],
        })),
        ...solutions.slice(0, 3).map((s): PathNode => ({
          id: s.id,
          title: s.title,
          description: s.problemDefinition,
          kind: 'solution',
          route: `/solutions/${s.id}`,
          difficulty: 'beginner',
          tags: [],
        })),
        ...highScoreProjects.slice(0, 3).map((p): PathNode => ({
          id: p.id,
          title: p.name,
          description: p.oneLineVerdict || p.summary,
          kind: 'project',
          route: `/projects/${p.id}`,
          difficulty: 'beginner',
          tags: p.types.slice(0, 3),
        })),
      ],
    },
    {
      id: 'intermediate',
      title: '进阶路径：从项目实践到方案抽象',
      description: '适合已有基础的同学。深入高分项目的技术细节，理解方案的 trade-off，再反哺到自己的工程动作。',
      nodes: [
        ...highScoreProjects.slice(0, 5).map((p): PathNode => ({
          id: p.id,
          title: p.name,
          description: p.oneLineVerdict || p.summary,
          kind: 'project',
          route: `/projects/${p.id}`,
          difficulty: 'intermediate',
          tags: p.types.slice(0, 3),
        })),
        ...solutions.slice(0, 5).map((s): PathNode => ({
          id: s.id,
          title: s.title,
          description: s.problemDefinition,
          kind: 'solution',
          route: `/solutions/${s.id}`,
          difficulty: 'intermediate',
          tags: [],
        })),
        ...painPoints.slice(0, 3).map((pp): PathNode => ({
          id: pp.id,
          title: pp.title,
          description: pp.industryPain || pp.solutionMethod,
          kind: 'painPoint',
          route: `/pain-points/${pp.id}`,
          difficulty: 'intermediate',
          tags: [pp.topic],
        })),
      ],
    },
    {
      id: 'interview',
      title: '面试路径：从知识积累到表达训练',
      description: '适合准备面试的同学。先把项目、方案和痛点过一遍，再用面经和 AI 面试官训练表达。',
      nodes: [
        ...allProjects.slice(0, 5).map((p): PathNode => ({
          id: p.id,
          title: p.name,
          description: p.oralAnswer || p.oneLineVerdict || p.summary,
          kind: 'project',
          route: `/projects/${p.id}`,
          difficulty: 'intermediate',
          tags: p.types.slice(0, 3),
        })),
        ...solutions.slice(0, 3).map((s): PathNode => ({
          id: s.id,
          title: s.title,
          description: s.problemDefinition,
          kind: 'solution',
          route: `/solutions/${s.id}`,
          difficulty: 'intermediate',
          tags: [],
        })),
      ],
    },
  ];
}

const KIND_LABELS = { project: '项目', solution: '方案', painPoint: '痛点' };
const KIND_ROUTES = { project: '/projects/', solution: '/solutions/', painPoint: '/pain-points/' };
const DIFFICULTY_LABELS = { beginner: '入门', intermediate: '进阶', advanced: '高级' };

export function LearningPathView({
  projects,
  solutions,
  painPoints,
}: {
  projects: Project[];
  solutions: Solution[];
  painPoints: PainPoint[];
}) {
  const navigate = useNavigate();
  const paths = useMemo(() => buildLearningPaths(projects, solutions, painPoints), [projects, solutions, painPoints]);
  const [selectedPathId, setSelectedPathId] = useState(paths[0]?.id ?? '');
  const [completed, setCompleted] = useState<Set<string>>(() => {
    if (typeof window === 'undefined') return new Set();
    try {
      const raw = localStorage.getItem('learning-path-progress');
      return raw ? new Set(JSON.parse(raw)) : new Set();
    } catch {
      return new Set();
    }
  });

  const selectedPath = paths.find((p) => p.id === selectedPathId) ?? paths[0];

  function toggleComplete(nodeId: string) {
    setCompleted((prev) => {
      const next = new Set(prev);
      if (next.has(nodeId)) next.delete(nodeId);
      else next.add(nodeId);
      if (typeof window !== 'undefined') {
        localStorage.setItem('learning-path-progress', JSON.stringify([...next]));
      }
      return next;
    });
  }

  const progress = selectedPath ? Math.round((selectedPath.nodes.filter((n) => completed.has(n.id)).length / selectedPath.nodes.length) * 100) : 0;

  return (
    <section className="workspace single-column">
      <article className="detail-panel">
        <div className="eyebrow">学习路径</div>
        <h2>按路径系统学习 Agent 工程</h2>
        <p className="lead">选择一条路径，按顺序阅读项目、方案和痛点。完成的节点会自动记录进度。</p>

        <div className="segmented compact" style={{ marginBottom: '1rem' }}>
          {paths.map((p) => (
            <button key={p.id} className={selectedPathId === p.id ? 'selected' : ''} onClick={() => setSelectedPathId(p.id)}>
              {p.title.split('：')[0]}
            </button>
          ))}
        </div>

        {selectedPath && (
          <>
            <div className="answer-box" style={{ marginBottom: '1rem' }}>
              <h3>{selectedPath.title}</h3>
              <p>{selectedPath.description}</p>
            </div>

            <div className="fact-grid" style={{ marginBottom: '1.5rem' }}>
              <div className="fact-item">
                <span className="fact-label">总节点</span>
                <strong className="fact-value">{selectedPath.nodes.length}</strong>
              </div>
              <div className="fact-item">
                <span className="fact-label">已完成</span>
                <strong className="fact-value">{selectedPath.nodes.filter((n) => completed.has(n.id)).length}</strong>
              </div>
              <div className="fact-item">
                <span className="fact-label">进度</span>
                <strong className="fact-value">{progress}%</strong>
              </div>
            </div>

            <div style={{ background: '#1e293b', borderRadius: '6px', height: '8px', marginBottom: '1.5rem', overflow: 'hidden' }}>
              <div style={{ background: '#3b82f6', height: '100%', width: `${progress}%`, transition: 'width 0.3s' }} />
            </div>

            <div className="learning-path-nodes">
              {selectedPath.nodes.map((node, index) => {
                const isDone = completed.has(node.id);
                return (
                  <div
                    key={node.id}
                    className={`item-card ${isDone ? 'completed' : ''}`}
                    style={{ display: 'flex', alignItems: 'flex-start', gap: '0.75rem', marginBottom: '0.5rem', opacity: isDone ? 0.7 : 1 }}
                  >
                    <button
                      type="button"
                      onClick={() => toggleComplete(node.id)}
                      style={{ background: 'none', border: 'none', cursor: 'pointer', padding: '0.25rem', flexShrink: 0 }}
                    >
                      {isDone ? <CheckCircle2 size={20} color="#10b981" /> : <Circle size={20} color="#64748b" />}
                    </button>
                    <div style={{ flex: 1 }}>
                      <div className="card-row">
                        <span className="badge">{index + 1}</span>
                        <span className="badge">{KIND_LABELS[node.kind]}</span>
                        <span className="badge">{DIFFICULTY_LABELS[node.difficulty]}</span>
                      </div>
                      <strong
                        style={{ cursor: 'pointer', color: '#e2e8f0' }}
                        onClick={() => navigate(node.route)}
                      >
                        {node.title}
                        <ChevronRight size={14} style={{ marginLeft: '0.25rem', verticalAlign: 'middle' }} />
                      </strong>
                      <p style={{ margin: '0.25rem 0 0', fontSize: '0.85rem', color: '#94a3b8' }}>
                        {node.description.length > 120 ? node.description.slice(0, 119) + '…' : node.description}
                      </p>
                      {node.tags.length > 0 && <TagList tags={node.tags.slice(0, 4)} />}
                    </div>
                  </div>
                );
              })}
            </div>
          </>
        )}
      </article>
    </section>
  );
}
