import React from 'react';
import { BrainCircuit, FileSearch, MessageSquareText } from 'lucide-react';
import type { EngineeringLogic, InterviewItem, PainPoint, Project, Solution, SourceItem } from '../types';
import type { ReaderKind } from '../constants';
import { FactItem, InfoBlock, ReaderLaunchPanel, TagList } from '../components/SharedComponents';
import { useFeedbackEntries } from '../hooks/useFeedbackEntries';
import { severityLabel, strengthLabel } from '../utils';

export function EngineeringLogicView({
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

export function SourcesView({
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

export function InterviewsView({
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

export function InterviewerView({
  items,
  memory,
}: {
  items: InterviewItem[];
  memory: { focus: string; answerStyle: string; weakSpots: string[] };
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

export function RadarView({ projects }: { projects: Project[] }) {
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

export function FeedbackSummaryView() {
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

export function VisualGenerationView() {
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
