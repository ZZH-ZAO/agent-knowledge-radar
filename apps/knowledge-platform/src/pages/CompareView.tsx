import React, { useMemo, useState } from 'react';
import { GitCompare } from 'lucide-react';
import type { Project } from '../types';
import { TagList } from '../components/SharedComponents';

const COMPARE_DIMENSIONS = [
  { key: 'primaryCategory', label: '主分类' },
  { key: 'businessScenario', label: '业务场景' },
  { key: 'biggestHighlight', label: '最大亮点' },
  { key: 'status', label: '状态' },
  { key: 'score', label: '评分' },
  { key: 'relatedPatterns', label: '关联方案' },
  { key: 'nextActions', label: '行动项' },
] as const;

export function CompareView({ projects }: { projects: Project[] }) {
  const [selectedIds, setSelectedIds] = useState<string[]>([]);
  const [search, setSearch] = useState('');

  const filtered = useMemo(() => {
    if (!search.trim()) return projects;
    const q = search.trim().toLowerCase();
    return projects.filter((p) => p.name.toLowerCase().includes(q) || p.types.join(' ').toLowerCase().includes(q));
  }, [projects, search]);

  const selected = useMemo(() => projects.filter((p) => selectedIds.includes(p.id)), [projects, selectedIds]);

  function toggle(id: string) {
    setSelectedIds((prev) => (prev.includes(id) ? prev.filter((x) => x !== id) : prev.length < 4 ? [...prev, id] : prev));
  }

  return (
    <section className="workspace single-column">
      <article className="detail-panel">
        <div className="eyebrow">方案对比</div>
        <h2>并排对比最多 4 个项目</h2>
        <p className="lead">选择 2-4 个项目，按主分类、业务场景、最大亮点、关联方案和行动项并排对比，快速判断哪个更适合当前场景。</p>

        <label className="search-box" style={{ marginBottom: '1rem' }}>
          <input value={search} onChange={(e) => setSearch(e.target.value)} placeholder="搜索项目名称或类型标签" />
        </label>

        <div className="compare-selector" style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem', marginBottom: '1.5rem' }}>
          {filtered.map((p) => (
            <button
              key={p.id}
              type="button"
              className={`item-card ${selectedIds.includes(p.id) ? 'selected' : ''}`}
              onClick={() => toggle(p.id)}
              style={{ flex: '0 0 auto', maxWidth: '220px', cursor: 'pointer' }}
            >
              <strong>{p.name}</strong>
              <span className="badge">{p.primaryCategory}</span>
            </button>
          ))}
        </div>

        {selected.length >= 2 ? (
          <CompareTable projects={selected} />
        ) : (
          <p className="muted" style={{ textAlign: 'center', padding: '2rem' }}>
            请从上方选择 2-4 个项目进行对比。
          </p>
        )}
      </article>
    </section>
  );
}

function CompareTable({ projects }: { projects: Project[] }) {
  return (
    <div className="compare-table" style={{ overflowX: 'auto' }}>
      <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.9rem' }}>
        <thead>
          <tr>
            <th style={{ textAlign: 'left', padding: '0.75rem', borderBottom: '2px solid #334155', color: '#94a3b8', minWidth: '120px' }}>维度</th>
            {projects.map((p) => (
              <th key={p.id} style={{ textAlign: 'left', padding: '0.75rem', borderBottom: '2px solid #334155', minWidth: '200px' }}>
                <strong>{p.name}</strong>
                {p.score ? <span className="badge" style={{ marginLeft: '0.5rem' }}>{p.score}</span> : null}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {COMPARE_DIMENSIONS.map((dim) => (
            <tr key={dim.key}>
              <td style={{ padding: '0.75rem', borderBottom: '1px solid #1e293b', color: '#94a3b8', fontWeight: 600 }}>{dim.label}</td>
              {projects.map((p) => (
                <td key={p.id} style={{ padding: '0.75rem', borderBottom: '1px solid #1e293b' }}>
                  <CompareCell project={p} dimKey={dim.key} />
                </td>
              ))}
            </tr>
          ))}
          <tr>
            <td style={{ padding: '0.75rem', borderBottom: '1px solid #1e293b', color: '#94a3b8', fontWeight: 600 }}>标签</td>
            {projects.map((p) => (
              <td key={p.id} style={{ padding: '0.75rem', borderBottom: '1px solid #1e293b' }}>
                <TagList tags={p.types.slice(0, 5)} />
              </td>
            ))}
          </tr>
          <tr>
            <td style={{ padding: '0.75rem', color: '#94a3b8', fontWeight: 600 }}>一句话判断</td>
            {projects.map((p) => (
              <td key={p.id} style={{ padding: '0.75rem' }}>
                {p.oneLineVerdict || p.summary || '暂无'}
              </td>
            ))}
          </tr>
        </tbody>
      </table>
    </div>
  );
}

function CompareCell({ project, dimKey }: { project: Project; dimKey: string }) {
  const value = (project as Record<string, unknown>)[dimKey];
  if (value == null) return <span className="muted">暂无</span>;
  if (Array.isArray(value)) {
    if (value.length === 0) return <span className="muted">暂无</span>;
    return (
      <ul style={{ margin: 0, paddingLeft: '1.2em' }}>
        {value.slice(0, 4).map((item, i) => (
          <li key={i}>{String(item)}</li>
        ))}
        {value.length > 4 && <li className="muted">+{value.length - 4} 更多</li>}
      </ul>
    );
  }
  return <span>{String(value)}</span>;
}
