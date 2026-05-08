import React, { useEffect, useMemo, useRef, useState } from 'react';
import { BookOpen, Copy, FileDown, Link2, ListTree } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import rehypeAutolinkHeadings from 'rehype-autolink-headings';
import rehypeSlug from 'rehype-slug';
import remarkGfm from 'remark-gfm';

type Props = {
  title: string;
  content: string;
  sourceFile?: string;
  searchTargetText?: string;
  showHeader?: boolean;
  showOutline?: boolean;
  showFeedback?: boolean;
};

type OutlineHeading = {
  id: string;
  text: string;
  level: number;
};

type StoredFeedback = {
  title?: string;
  sourceFile?: string;
  vote?: 'helpful' | 'needs-work' | null;
  note?: string;
  blockHash?: string;
  updatedAt?: string;
};

export default function MarkdownPreview({
  title,
  content,
  sourceFile = '',
  searchTargetText = '',
  showHeader = true,
  showOutline = true,
  showFeedback = true,
}: Props) {
  const [focused, setFocused] = useState(true);
  const [copiedLabel, setCopiedLabel] = useState<'link' | 'markdown' | null>(null);
  const [activeHeadingId, setActiveHeadingId] = useState('');
  const [feedbackVote, setFeedbackVote] = useState<'helpful' | 'needs-work' | null>(null);
  const [feedbackNote, setFeedbackNote] = useState('');
  const [feedbackSaved, setFeedbackSaved] = useState(false);
  const bodyRef = useRef<HTMLDivElement | null>(null);
  const query = useCurrentQuery();
  const feedbackStorageKey = useMemo(() => `knowledge-feedback:${sourceFile || title}`, [sourceFile, title]);
  const documentId = useMemo(() => `doc-${slugify(`${title}-${sourceFile}`) || 'document'}`, [sourceFile, title]);
  const headings = useMemo(() => extractHeadings(content).slice(0, 24), [content]);

  useEffect(() => {
    if (!query.trim()) return;
    const root = bodyRef.current;
    if (!root) return;
    const mark = root.querySelector('mark.search-highlight');
    mark?.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }, [query, content]);

  useEffect(() => {
    if (!copiedLabel) return;
    const timer = window.setTimeout(() => setCopiedLabel(null), 1400);
    return () => window.clearTimeout(timer);
  }, [copiedLabel]);

  useEffect(() => {
    if (typeof window === 'undefined') return;
    const raw = window.localStorage.getItem(feedbackStorageKey);
    if (!raw) return;
    try {
      const parsed = JSON.parse(raw) as StoredFeedback;
      setFeedbackVote(parsed.vote ?? null);
      setFeedbackNote(parsed.note ?? '');
    } catch {
      // ignore invalid local feedback cache
    }
  }, [feedbackStorageKey]);

  useEffect(() => {
    const root = bodyRef.current;
    if (!root || !headings.length) return;
    const elements = headings
      .map((heading) => root.querySelector<HTMLElement>(`#${CSS.escape(heading.id)}`))
      .filter((element): element is HTMLElement => Boolean(element));
    if (!elements.length) return;

    setActiveHeadingId((current) => current || elements[0].id);

    const observer = new IntersectionObserver(
      (entries) => {
        const visible = entries
          .filter((entry) => entry.isIntersecting)
          .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
        if (visible[0]?.target instanceof HTMLElement) {
          setActiveHeadingId(visible[0].target.id);
        }
      },
      {
        root,
        rootMargin: '0px 0px -65% 0px',
        threshold: [0, 0.2, 0.5, 1],
      },
    );

    elements.forEach((element) => observer.observe(element));
    return () => observer.disconnect();
  }, [content, headings]);

  useEffect(() => {
    const root = bodyRef.current;
    if (!root) return;

    root.querySelectorAll('.search-target-block').forEach((element) => element.classList.remove('search-target-block'));

    const target = normalizeTargetText(searchTargetText);
    if (!target) return;

    const candidates = Array.from(root.querySelectorAll<HTMLElement>('p, li, blockquote, td, th, h2, h3, h4, h5'));
    const matched = candidates.find((element) => normalizeTargetText(element.innerText).includes(target));
    if (!matched) return;

    matched.classList.add('search-target-block');
    if (!matched.id) {
      const fallbackId = `block-${slugify(matched.innerText.slice(0, 80)) || 'target'}`;
      matched.id = fallbackId;
      matched.setAttribute('data-block-id', fallbackId);
    }
    if (typeof window !== 'undefined' && matched.id) {
      const url = new URL(window.location.href);
      url.hash = matched.id;
      window.history.replaceState({}, '', url);
    }
    matched.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }, [searchTargetText, content]);

  return (
    <section id={documentId} className={`document-reader ${focused ? 'focused' : ''}`}>
      {showHeader ? (
        <div className="preview-header">
          <div className="preview-title-group">
            <BookOpen size={18} />
            <span>{title}</span>
          </div>
          <div className="reader-actions" aria-label="页面操作">
            <button type="button" className="reader-action-button" onClick={() => setFocused((value) => !value)}>
              <ListTree size={15} />
              <span>{focused ? '退出专注' : '专注阅读'}</span>
            </button>
            <button
              type="button"
              className="reader-action-button"
              onClick={async () => {
                await copyText(buildPageLink(documentId));
                setCopiedLabel('link');
              }}
            >
              <Link2 size={15} />
              <span>{copiedLabel === 'link' ? '已复制链接' : '复制链接'}</span>
            </button>
            <button
              type="button"
              className="reader-action-button"
              onClick={async () => {
                await copyText(content);
                setCopiedLabel('markdown');
              }}
            >
              <Copy size={15} />
              <span>{copiedLabel === 'markdown' ? '已复制 Markdown' : '复制 Markdown'}</span>
            </button>
            <button type="button" className="reader-action-button" onClick={() => exportMarkdown(title, content)}>
              <FileDown size={15} />
              <span>导出 Markdown</span>
            </button>
          </div>
        </div>
      ) : null}

      <div className={`document-shell ${showOutline ? '' : 'single-column-shell'}`}>
        {showOutline ? (
          <aside className="document-outline">
            <strong>章节目录</strong>
            <span>{headings.length} 个标题，可直接跳转</span>
            {headings.map((heading) => (
              <button
                key={`${heading.id}-${heading.level}`}
                type="button"
                className={`outline-link outline-level-${heading.level} ${activeHeadingId === heading.id ? 'active' : ''}`}
                onClick={() => scrollToHeading(heading.id)}
              >
                {heading.text}
              </button>
            ))}
          </aside>
        ) : null}
        <div ref={bodyRef} className="document-body markdown-body">
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            rehypePlugins={[rehypeSlug, rehypeAutolinkHeadings]}
            components={{
              h1: ({ children }) => <h2 id={headingId(children)}>{highlightNode(children, query)}</h2>,
              h2: ({ children }) => <h3 id={headingId(children)}>{highlightNode(children, query)}</h3>,
              h3: ({ children }) => <h4 id={headingId(children)}>{highlightNode(children, query)}</h4>,
              h4: ({ children }) => <h5 id={headingId(children)}>{highlightNode(children, query)}</h5>,
              p: ({ children }) => (
                <p id={blockId(children, 'p')} data-block-id={blockId(children, 'p')}>
                  {highlightNode(children, query)}
                </p>
              ),
              li: ({ children }) => (
                <li id={blockId(children, 'li')} data-block-id={blockId(children, 'li')}>
                  {highlightNode(children, query)}
                </li>
              ),
              blockquote: ({ children }) => (
                <blockquote id={blockId(children, 'quote')} data-block-id={blockId(children, 'quote')}>
                  {highlightNode(children, query)}
                </blockquote>
              ),
              td: ({ children }) => (
                <td id={blockId(children, 'td')} data-block-id={blockId(children, 'td')}>
                  {highlightNode(children, query)}
                </td>
              ),
              th: ({ children }) => (
                <th id={blockId(children, 'th')} data-block-id={blockId(children, 'th')}>
                  {highlightNode(children, query)}
                </th>
              ),
              a: ({ href, children }) => (
                <a href={href} target="_blank" rel="noreferrer">
                  {highlightNode(children, query)}
                </a>
              ),
            }}
          >
            {content}
          </ReactMarkdown>
        </div>
      </div>

      {showFeedback ? (
        <section className="reader-feedback" id={`${documentId}-feedback`}>
        <div className="reader-feedback-header">
          <strong>阅读反馈</strong>
          <span>把你的判断沉淀成后续优化、面试追问和知识补强线索</span>
        </div>
        <div className="reader-feedback-actions">
          <button
            type="button"
            className={`feedback-chip ${feedbackVote === 'helpful' ? 'active' : ''}`}
            onClick={() => {
              setFeedbackVote('helpful');
              setFeedbackSaved(false);
            }}
          >
            这页有帮助
          </button>
          <button
            type="button"
            className={`feedback-chip ${feedbackVote === 'needs-work' ? 'active' : ''}`}
            onClick={() => {
              setFeedbackVote('needs-work');
              setFeedbackSaved(false);
            }}
          >
            还需要补强
          </button>
        </div>
        <textarea
          className="reader-feedback-input"
          value={feedbackNote}
          onChange={(event) => {
            setFeedbackNote(event.target.value);
            setFeedbackSaved(false);
          }}
          placeholder="记录你觉得缺什么、哪一段最有启发，或者你希望把它转成什么行动项。"
          rows={3}
        />
        <div className="reader-feedback-footer">
          <button
            type="button"
            className="reader-action-button"
            onClick={() => {
              if (typeof window !== 'undefined') {
                window.localStorage.setItem(
                  feedbackStorageKey,
                  JSON.stringify({
                    title,
                    sourceFile,
                    vote: feedbackVote,
                    note: feedbackNote.trim(),
                    blockHash: window.location.hash || '',
                    updatedAt: new Date().toISOString(),
                  }),
                );
              }
              setFeedbackSaved(true);
            }}
          >
            保存反馈
          </button>
          <button
            type="button"
            className="reader-action-button"
            onClick={() =>
              exportMarkdown(
                `${title}-feedback`,
                [
                  `# ${title} 反馈`,
                  '',
                  `- source: ${sourceFile || 'unknown'}`,
                  `- vote: ${feedbackVote || 'unselected'}`,
                  `- block: ${typeof window !== 'undefined' ? window.location.hash || '(none)' : '(none)'}`,
                  `- updatedAt: ${new Date().toISOString()}`,
                  '',
                  '## note',
                  feedbackNote.trim() || '暂无备注',
                ].join('\n'),
              )
            }
          >
            导出反馈
          </button>
          <span>{feedbackSaved ? '反馈已保存在本地，可继续进入汇总、导出和面试追问。' : '当前先保存在本地，后续会被平台汇总为持续迭代线索。'}</span>
        </div>
        </section>
      ) : null}
    </section>
  );
}

function useCurrentQuery() {
  const [query, setQuery] = useState('');

  useEffect(() => {
    const read = () => {
      const input = document.querySelector<HTMLInputElement>('.search-box input');
      setQuery(input?.value ?? '');
    };
    read();
    const input = document.querySelector<HTMLInputElement>('.search-box input');
    input?.addEventListener('input', read);
    return () => input?.removeEventListener('input', read);
  }, []);

  return query;
}

function buildPageLink(documentId: string) {
  const url = new URL(window.location.href);
  url.hash = documentId;
  return url.toString();
}

function exportMarkdown(title: string, content: string) {
  const safeTitle = title.replace(/[\\/:*?"<>|]+/g, '-').trim() || 'document';
  const blob = new Blob([content], { type: 'text/markdown;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement('a');
  anchor.href = url;
  anchor.download = `${safeTitle}.md`;
  anchor.click();
  URL.revokeObjectURL(url);
}

async function copyText(value: string) {
  if (navigator.clipboard?.writeText) {
    await navigator.clipboard.writeText(value);
    return;
  }
  const textarea = document.createElement('textarea');
  textarea.value = value;
  textarea.style.position = 'fixed';
  textarea.style.opacity = '0';
  document.body.appendChild(textarea);
  textarea.focus();
  textarea.select();
  document.execCommand('copy');
  document.body.removeChild(textarea);
}

function scrollToHeading(id: string) {
  document.getElementById(id)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function extractHeadings(content: string): OutlineHeading[] {
  return content
    .split('\n')
    .map((line) => line.trim())
    .filter((line) => /^#{1,4}\s+/.test(line))
    .map((line) => {
      const match = line.match(/^(#{1,4})\s+(.+)$/);
      const level = match?.[1].length ?? 1;
      const text = (match?.[2] ?? line).replace(/^\d+\.\s*/, '').trim();
      return { id: slugify(text), text, level };
    });
}

function slugify(value: string) {
  return value
    .toLowerCase()
    .replace(/[^\w\u4e00-\u9fa5]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

function headingId(children: React.ReactNode) {
  return slugify(flattenText(children));
}

function blockId(children: React.ReactNode, prefix: string) {
  const text = flattenText(children).trim();
  if (!text) return undefined;
  return `${prefix}-${slugify(text.slice(0, 80)) || 'block'}`;
}

function flattenText(children: React.ReactNode): string {
  if (typeof children === 'string' || typeof children === 'number') return String(children);
  if (Array.isArray(children)) return children.map(flattenText).join('');
  if (React.isValidElement<{ children?: React.ReactNode }>(children)) return flattenText(children.props.children);
  return '';
}

function highlightNode(node: React.ReactNode, query: string): React.ReactNode {
  if (!query.trim()) return node;
  if (typeof node === 'string' || typeof node === 'number') return highlightText(String(node), query);
  if (Array.isArray(node)) return node.map((child, index) => <React.Fragment key={index}>{highlightNode(child, query)}</React.Fragment>);
  if (React.isValidElement<{ children?: React.ReactNode }>(node)) {
    return React.cloneElement(node, {
      ...node.props,
      children: highlightNode(node.props.children, query),
    });
  }
  return node;
}

function highlightText(text: string, query: string) {
  const safe = query.trim();
  if (!safe) return text;
  const pattern = new RegExp(`(${escapeRegExp(safe)})`, 'gi');
  const parts = text.split(pattern);
  if (parts.length === 1) return text;
  return parts.map((part, index) =>
    part.toLowerCase() === safe.toLowerCase() ? (
      <mark key={`${part}-${index}`} className="search-highlight">
        {part}
      </mark>
    ) : (
      <React.Fragment key={`${part}-${index}`}>{part}</React.Fragment>
    ),
  );
}

function escapeRegExp(value: string) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function normalizeTargetText(value: string) {
  return value.replace(/\.\.\./g, '').replace(/\s+/g, ' ').trim().toLowerCase();
}
