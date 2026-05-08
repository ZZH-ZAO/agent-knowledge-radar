import React from 'react';
import type { SearchItem } from '../types';
import { kindLabel } from '../utils';

export function SearchResults({ results, onOpen }: { results: SearchItem[]; onOpen: (item: SearchItem) => void }) {
  return (
    <section className="search-results">
      <div className="panel-title">
        <span>搜索结果</span>
        <span className="badge">{results.length} 条</span>
      </div>
      <div className="item-list">
        {results.map((item) => (
          <button key={item.id} type="button" className="item-card" onClick={() => onOpen(item)}>
            <div className="card-row">
              <strong>{item.title}</strong>
              <span className="badge">{kindLabel(item.kind)}</span>
            </div>
            <p>{item.summary}</p>
            {item.tags.length ? (
              <div className="inline-badges">
                {item.tags.slice(0, 4).map((tag) => (
                  <span key={tag} className="badge">{tag}</span>
                ))}
              </div>
            ) : null}
          </button>
        ))}
      </div>
    </section>
  );
}

export function StatusBadge({ status }: { status: string }) {
  return <span className={`badge ${status === '深度沉淀' ? 'good' : 'draft'}`}>{status}</span>;
}

export function TagList({ tags }: { tags: string[] }) {
  if (!tags.length) return null;
  return (
    <div className="inline-badges">
      {tags.map((tag) => (
        <span key={tag} className="badge">{tag}</span>
      ))}
    </div>
  );
}

export function LearningGuide({ title, items }: { title: string; items: string[] }) {
  return (
    <section className="learning-guide">
      <div className="detail-header">
        <div>
          <div className="eyebrow">阅读指引</div>
          <h3>{title}</h3>
        </div>
      </div>
      <ol className="guide-list">
        {items.map((item, index) => (
          <li key={index}>{item}</li>
        ))}
      </ol>
    </section>
  );
}

export function InfoBlock({ title, items, empty }: { title: string; items: string[]; empty: string }) {
  return (
    <section className="info-block">
      <strong>{title}</strong>
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

export function FactItem({ label, value }: { label: string; value: string }) {
  return (
    <div className="fact-item">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

export function OverviewMeta({ label, value }: { label: string; value: string }) {
  return (
    <div className="overview-meta">
      <span className="overview-meta-label">{label}</span>
      <span className="overview-meta-value">{value}</span>
    </div>
  );
}

export function ReaderLaunchPanel({
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
      <div className="detail-header">
        <div>
          <div className="eyebrow">{label}</div>
          <h3>{title}</h3>
        </div>
      </div>
      <p className="lead">{description}</p>
      <button type="button" className="primary-button" onClick={onOpen}>
        {title}
      </button>
    </section>
  );
}
