import React, { useMemo } from 'react';
import { Activity, AlertTriangle, CheckCircle2, Clock, TrendingUp } from 'lucide-react';
import type { Project, Solution, PainPoint, SourceItem, InterviewItem, KnowledgeIndex } from '../types';

export function DashboardView({ data }: { data: KnowledgeIndex }) {
  const stats = useMemo(() => {
    const projects = data.projects;
    const solutions = data.solutions;
    const painPoints = data.painPoints;
    const sources = data.sources;
    const interviews = data.interviews.items;

    const highScoreProjects = projects.filter((p) => (p.score ?? 0) >= 80).length;
    const deepDistilled = projects.filter((p) => p.status === '深度沉淀').length;
    const withWriteback = projects.filter((p) => p.writebackStatus === 'completed').length;
    const partialWriteback = projects.filter((p) => p.writebackStatus === 'partial').length;
    const noWriteback = projects.filter((p) => !p.writebackStatus || p.writebackStatus === 'none').length;

    const highSeverityPainPoints = painPoints.filter((p) => p.severity === 'high').length;
    const withEvidence = painPoints.filter((p) => p.evidenceProjects.length > 0).length;

    const highStrengthSources = sources.filter((s) => s.evidenceStrength === 'high').length;

    const relatedPatternCount = new Set(projects.flatMap((p) => p.relatedPatterns)).size;
    const avgScore = projects.length ? Math.round(projects.reduce((sum, p) => sum + (p.score ?? 0), 0) / projects.length) : 0;

    return {
      projects: projects.length,
      solutions: solutions.length,
      painPoints: painPoints.length,
      sources: sources.length,
      interviews: interviews.length,
      highScoreProjects,
      deepDistilled,
      withWriteback,
      partialWriteback,
      noWriteback,
      highSeverityPainPoints,
      withEvidence,
      highStrengthSources,
      relatedPatternCount,
      avgScore,
    };
  }, [data]);

  const coverageItems = useMemo(() => {
    const items: Array<{ label: string; value: number; total: number; tone: string }> = [
      { label: '高分项目 (≥80)', value: stats.highScoreProjects, total: stats.projects, tone: 'green' },
      { label: '深度沉淀项目', value: stats.deepDistilled, total: stats.projects, tone: 'blue' },
      { label: '已完成回写', value: stats.withWriteback, total: stats.projects, tone: 'green' },
      { label: '部分回写', value: stats.partialWriteback, total: stats.projects, tone: 'amber' },
      { label: '未回写', value: stats.noWriteback, total: stats.projects, tone: 'red' },
      { label: '有证据的痛点', value: stats.withEvidence, total: stats.painPoints, tone: 'blue' },
      { label: '高强度资料', value: stats.highStrengthSources, total: stats.sources, tone: 'green' },
    ];
    return items;
  }, [stats]);

  const actionItems = useMemo(() => {
    const items: string[] = [];
    if (stats.noWriteback > 0) items.push(`${stats.noWriteback} 个项目尚未回写到方案和痛点`);
    if (stats.highSeverityPainPoints > 0) items.push(`${stats.highSeverityPainPoints} 个高严重度痛点需要优先补强证据`);
    if (stats.deepDistilled < stats.projects * 0.5) items.push('深度沉淀项目比例偏低，建议优先沉淀高分项目');
    if (stats.withEvidence < stats.painPoints * 0.5) items.push('有证据的痛点比例偏低，建议补充证据项目');
    if (stats.avgScore < 60) items.push(`项目平均评分 ${stats.avgScore}，建议优先提升低分项目质量`);
    if (items.length === 0) items.push('知识库状态健康，继续保持！');
    return items;
  }, [stats]);

  return (
    <section className="workspace single-column">
      <article className="detail-panel">
        <div className="eyebrow">健康仪表盘</div>
        <h2>知识库整体状态</h2>
        <p className="lead">一览知识库的覆盖度、质量和待补强项，帮助你决定下一步应该优先做什么。</p>

        <div className="fact-grid">
          <div className="fact-item">
            <span className="fact-label">项目总数</span>
            <strong className="fact-value">{stats.projects}</strong>
          </div>
          <div className="fact-item">
            <span className="fact-label">方案总数</span>
            <strong className="fact-value">{stats.solutions}</strong>
          </div>
          <div className="fact-item">
            <span className="fact-label">痛点总数</span>
            <strong className="fact-value">{stats.painPoints}</strong>
          </div>
          <div className="fact-item">
            <span className="fact-label">资料源</span>
            <strong className="fact-value">{stats.sources}</strong>
          </div>
          <div className="fact-item">
            <span className="fact-label">面试题</span>
            <strong className="fact-value">{stats.interviews}</strong>
          </div>
          <div className="fact-item">
            <span className="fact-label">关联方案数</span>
            <strong className="fact-value">{stats.relatedPatternCount}</strong>
          </div>
          <div className="fact-item">
            <span className="fact-label">平均评分</span>
            <strong className="fact-value">{stats.avgScore}</strong>
          </div>
        </div>

        <section className="deep-dive-panel" style={{ marginTop: '1.5rem' }}>
          <div className="detail-header">
            <div>
              <div className="eyebrow">覆盖度</div>
              <h3>各维度的完成情况</h3>
            </div>
            <Activity size={24} />
          </div>
          <div className="coverage-bars">
            {coverageItems.map((item) => {
              const pct = item.total > 0 ? Math.round((item.value / item.total) * 100) : 0;
              return (
                <div key={item.label} style={{ marginBottom: '0.75rem' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.25rem', fontSize: '0.85rem' }}>
                    <span>{item.label}</span>
                    <span>{item.value} / {item.total} ({pct}%)</span>
                  </div>
                  <div style={{ background: '#1e293b', borderRadius: '4px', height: '6px', overflow: 'hidden' }}>
                    <div
                      style={{
                        background: item.tone === 'green' ? '#10b981' : item.tone === 'blue' ? '#3b82f6' : item.tone === 'amber' ? '#f59e0b' : '#ef4444',
                        height: '100%',
                        width: `${pct}%`,
                        transition: 'width 0.3s',
                      }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </section>

        <section className="answer-box" style={{ marginTop: '1.5rem' }}>
          <h3>
            <AlertTriangle size={16} style={{ marginRight: '0.5rem', verticalAlign: 'middle' }} />
            待补强项
          </h3>
          <ul style={{ margin: 0, paddingLeft: '1.2em' }}>
            {actionItems.map((item, i) => (
              <li key={i}>{item}</li>
            ))}
          </ul>
        </section>
      </article>
    </section>
  );
}
