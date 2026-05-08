import React, { Suspense, lazy } from 'react';
import { ArrowLeft } from 'lucide-react';
import type { ReaderDocument } from '../constants';
import { TagList } from './SharedComponents';
import { extractReaderHeadings, scrollToElement, slugify } from '../utils';

const MarkdownPreview = lazy(() => import('../MarkdownPreview'));

export function FullReaderView({ document, onClose }: { document: ReaderDocument; onClose: () => void }) {
  const docId = slugify(`${document.title}-${document.sourceFile}`) ? `doc-${slugify(`${document.title}-${document.sourceFile}`)}` : 'document';
  const outline = extractReaderHeadings(document.content);
  const quickJumps = [
    { id: 'reader-hero', label: '概览' },
    { id: 'reader-guides', label: '导读' },
    { id: docId, label: '正文' },
    ...(document.actionItems.length ? [{ id: 'reader-actions', label: '行动项' }] : []),
  ];

  return (
    <section className="reader-screen">
      <div className="reader-screen-topbar">
        <button type="button" className="ghost-button" onClick={onClose}>
          <ArrowLeft size={16} />
          <span>返回上一页</span>
        </button>
        <div className="reader-screen-actions">
          {quickJumps.map((jump) => (
            <button key={jump.id} type="button" className="ghost-button compact-button" onClick={() => scrollToElement(jump.id)}>
              {jump.label}
            </button>
          ))}
          <span className="badge good">完整阅读器</span>
          <span className="badge">{document.eyebrow}</span>
        </div>
      </div>

      <div className="reader-screen-layout">
        <div className="reader-main-column">
          <div id="reader-hero" className="reader-hero-card">
            <div className="eyebrow">{document.eyebrow}</div>
            <h1>{document.title}</h1>
            <p>{document.summary}</p>
            <div className="reader-badge-row">
              <TagList tags={document.badges} />
            </div>
          </div>

          <div id="reader-guides" className="reader-guide-grid">
            {document.guideCards.map((card) => (
              <section key={card.title} className="reader-guide-card">
                <h3>{card.title}</h3>
                <p>{card.body}</p>
              </section>
            ))}
          </div>

          <div className="reader-article-shell">
            <div className="reader-article-topline">
              <span>来源文件</span>
              <strong>{document.sourceFile}</strong>
            </div>
            <Suspense fallback={<div className="detail-panel">正在加载阅读组件...</div>}>
              <MarkdownPreview
                title={document.title}
                content={document.content}
                sourceFile={document.sourceFile}
                showHeader={false}
                showOutline={false}
                showFeedback={false}
              />
            </Suspense>
          </div>

          {document.actionItems.length ? (
            <section id="reader-actions" className="reader-action-card">
              <div className="eyebrow">行动收束</div>
              <h3>把这次阅读继续变成项目动作</h3>
              <ul className="reader-side-list">
                {document.actionItems.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </section>
          ) : null}
        </div>

        <aside className="reader-side">
          <div className="reader-side-block">
            <div className="eyebrow">阅读摘要</div>
            <h2>{document.title}</h2>
            <p>{document.summary}</p>
          </div>

          <div className="reader-side-block">
            <strong>快速信息</strong>
            <div className="reader-fact-list">
              {document.quickFacts.map((fact) => (
                <div key={`${fact.label}-${fact.value}`} className="reader-fact-row">
                  <span>{fact.label}</span>
                  <strong>{fact.value}</strong>
                </div>
              ))}
            </div>
          </div>

          <div className="reader-side-block">
            <strong>目录跳转</strong>
            {outline.length ? (
              <div className="reader-outline-list">
                {outline.map((heading) => (
                  <button
                    key={`${heading.id}-${heading.level}`}
                    type="button"
                    className={`reader-outline-link level-${heading.level}`}
                    onClick={() => scrollToElement(heading.id)}
                  >
                    {heading.text}
                  </button>
                ))}
              </div>
            ) : (
              <p className="muted">当前文档还没有可跳转标题。</p>
            )}
          </div>
        </aside>
      </div>
    </section>
  );
}
