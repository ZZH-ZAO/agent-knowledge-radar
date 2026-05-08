import React, { Suspense, lazy } from 'react';
import { Layers3 } from 'lucide-react';
import type { Solution } from '../types';
import type { ReaderKind } from '../constants';
import { InfoBlock, LearningGuide, ReaderLaunchPanel } from '../components/SharedComponents';
import { buildSolutionDeepDiveMarkdown, buildSolutionPressurePrompt, buildSolutionTakeaway } from '../utils';

const MarkdownPreview = lazy(() => import('../MarkdownPreview'));

export function SolutionsView({
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
              <h3>把"这套方案怎么落地"写成能直接学习的正文</h3>
            </div>
          </div>
          <p className="lead">
            这里不再只保留术语和要点，而是按"问题定义 / 方案结构 / 成熟做法 / 常见误区 / 当前动作"的顺序展开，方便你直接拿去学习、复述和迁移。
          </p>
          <Suspense fallback={<div className="detail-panel">正在加载阅读组件...</div>}>
            <MarkdownPreview
              title={`${selectedSolution.title} 深度拆解`}
              content={buildSolutionDeepDiveMarkdown(selectedSolution)}
              sourceFile={selectedSolution.sourceFile}
              showHeader={false}
              showOutline={false}
              showFeedback={false}
            />
          </Suspense>
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
