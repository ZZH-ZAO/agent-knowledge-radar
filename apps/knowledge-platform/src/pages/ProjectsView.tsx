import React, { Suspense, lazy } from 'react';
import { ArrowLeft, ClipboardList, ExternalLink } from 'lucide-react';
import type { Project } from '../types';
import type { ReaderKind } from '../constants';
import { FactItem, InfoBlock, OverviewMeta, ReaderLaunchPanel, StatusBadge, TagList } from '../components/SharedComponents';
import { buildProjectDeepDiveMarkdown, buildProjectEngineeringPitch, buildProjectMisreadWarning, buildProjectOralAnswer, buildProjectPressurePrompt, buildProjectTakeaway } from '../utils';

const MarkdownPreview = lazy(() => import('../MarkdownPreview'));

export function ProjectsView({
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
              这里直接抽取项目正文里的"通用问题 / 技术框架 / 可迁移原则"原文结构，重点看这个项目是如何拆问题、落方案、做步骤和形成工程边界的。
            </p>
            <Suspense fallback={<div className="detail-panel">正在加载阅读组件...</div>}>
              <MarkdownPreview
                title={`${selectedProject.name} 深度拆解`}
                content={buildProjectDeepDiveMarkdown(selectedProject)}
                sourceFile={selectedProject.sourceFile}
                showHeader={false}
                showOutline={false}
                showFeedback={false}
              />
            </Suspense>
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
