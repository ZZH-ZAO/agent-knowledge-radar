import React, { Suspense, lazy } from 'react';
import { AlertTriangle } from 'lucide-react';
import type { PainPoint, Project } from '../types';
import type { ReaderKind } from '../constants';
import { FactItem, InfoBlock, LearningGuide, ReaderLaunchPanel } from '../components/SharedComponents';
import { buildPainPointDeepDiveMarkdown, buildPainPointPressurePrompt, buildPainPointTakeaway, severityLabel } from '../utils';

const MarkdownPreview = lazy(() => import('../MarkdownPreview'));

export function PainPointsView({
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
    ? new Date(selectedPainPoint.lastUpdatedAt).toLocaleString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit' })
    : '';

  return (
    <section className="workspace two-column">
      <div className="list-panel">
        <div className="panel-title">
          <AlertTriangle size={18} />
          <span>行业痛点</span>
        </div>
        <div className="list-meta">不是罗列 bug，而是 Agent / 大模型行业里反复出现的结构性问题。</div>
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
                <span className="badge">证据 {painPoint.evidenceProjectCount ?? painPoint.evidenceProjects.length}</span>
              </div>
            </button>
          ))}
        </div>
      </div>
      <article className="detail-panel">
        <div className="eyebrow">痛点导读</div>
        <h2>{selectedPainPoint.title}</h2>
        <p className="lead">{selectedPainPoint.industryPain || selectedPainPoint.solutionMethod}</p>
        <div className="fact-grid">
          <FactItem label="严重度" value={severityLabel(selectedPainPoint.severity)} />
          <FactItem label="证据项目" value={String(evidenceCount)} />
          <FactItem label="成熟做法" value={String(commonPractices.length)} />
          <FactItem label="行动项" value={String(selectedPainPoint.actions.length)} />
        </div>
        <div className="source-line">
          <span>关联方案</span>
          <strong>{selectedPainPoint.relatedSolution}</strong>
        </div>
        {(lastUpdatedLabel || lastUpdatedFromProjects.length) && (
          <div className="evidence-grid">
            <InfoBlock title="最近更新项目" items={lastUpdatedFromProjects} empty="暂无更新项目" />
            <InfoBlock title="最近更新时间" items={lastUpdatedLabel ? [lastUpdatedLabel] : []} empty="暂无更新时间" />
          </div>
        )}
        <LearningGuide
          title="痛点阅读方式"
          items={[
            '先回答这个痛点到底是什么行业共性问题，为什么反复发生。',
            '再看证据项目和成熟做法，理解优质项目怎么处理。',
            '最后把行动项转成你当前平台或项目的实现顺序。',
          ]}
        />
        <div className="workflow-grid">
          <section className="answer-box">
            <h3>带走的判断</h3>
            <p>{buildPainPointTakeaway(selectedPainPoint)}</p>
          </section>
          <section className="answer-box">
            <h3>继续追问</h3>
            <p>{buildPainPointPressurePrompt(selectedPainPoint)}</p>
          </section>
        </div>
        <div className="evidence-grid">
          <InfoBlock title="证据来源" items={selectedPainPoint.evidenceSources ?? []} empty="暂无证据来源" />
          <InfoBlock title="证据项目" items={selectedPainPoint.evidenceProjects.map((id) => projectNames.get(id) || id)} empty="暂无证据项目" />
          <InfoBlock title="成熟做法" items={commonPractices} empty="暂无成熟做法" />
          <InfoBlock title="数据信号" items={selectedPainPoint.dataSignals ?? []} empty="暂无数据信号" />
          <InfoBlock title="常见误区" items={selectedPainPoint.commonMistakes} empty="暂无误区" />
          <InfoBlock title="演化规律" items={selectedPainPoint.evolutionRule ? [selectedPainPoint.evolutionRule] : []} empty="暂无演化规律" />
        </div>
        <section className="deep-dive-panel">
          <div className="detail-header">
            <div>
              <div className="eyebrow">深度拆解</div>
              <h3>不要只看结论，要看这个痛点背后的完整证据链</h3>
            </div>
          </div>
          <p className="lead">这里直接抽取痛点正文里的行业现象、证据项目、成熟做法和行动项，重点看这个痛点为什么反复出现、优质项目怎么处理。</p>
          <Suspense fallback={<div className="detail-panel">正在加载阅读组件...</div>}>
            <MarkdownPreview
              title={`${selectedPainPoint.title} 深度拆解`}
              content={buildPainPointDeepDiveMarkdown(selectedPainPoint, projects)}
              sourceFile={selectedPainPoint.sourceFile ?? selectedPainPoint.id}
              showHeader={false}
              showOutline={false}
              showFeedback={false}
            />
          </Suspense>
        </section>
        <ReaderLaunchPanel
          label="痛点全文阅读器"
          title="进入整页阅读"
          description="痛点页的证据链和项目分析更适合放到完整阅读器里，避免和摘要卡片混在同一屏。"
          onOpen={() => onOpenReader('pain-point', selectedPainPoint.id)}
        />
      </article>
    </section>
  );
}
