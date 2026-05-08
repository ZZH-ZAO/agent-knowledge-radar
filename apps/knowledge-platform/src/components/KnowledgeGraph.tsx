import React, { useEffect, useRef, useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import type { GraphData, GraphNode, RelationType } from '../types';

const NODE_COLORS: Record<string, string> = {
  project: '#3b82f6',
  solution: '#10b981',
  painPoint: '#f59e0b',
  source: '#8b5cf6',
  interview: '#ec4899',
};

const RELATION_COLORS: Record<RelationType, string> = {
  supports: '#94a3b8',
  solves: '#10b981',
  implements: '#3b82f6',
  'evidence-for': '#f59e0b',
  related: '#6b7280',
};

const NODE_KIND_LABELS: Record<string, string> = {
  project: '项目',
  solution: '方案',
  painPoint: '痛点',
  source: '资料源',
  interview: '面经',
};

function routeForNode(node: GraphNode): string {
  switch (node.kind) {
    case 'project': return `/projects/${node.id}`;
    case 'solution': return `/solutions/${node.id}`;
    case 'painPoint': return `/pain-points/${node.id}`;
    case 'source': return `/sources/${node.id}`;
    case 'interview': return `/interviews/${node.id}`;
    default: return '/';
  }
}

type SimNode = GraphNode & { x: number; y: number; vx: number; vy: number };

const MIN_ZOOM = 0.2;
const MAX_ZOOM = 4;
const ZOOM_SENSITIVITY = 0.001;

export function KnowledgeGraph({ data }: { data: GraphData }) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const navigate = useNavigate();
  const [filter, setFilter] = useState<string>('all');
  const [hoveredNode, setHoveredNode] = useState<SimNode | null>(null);
  const nodesRef = useRef<SimNode[]>([]);
  const animRef = useRef<number>(0);
  const zoomRef = useRef(1);
  const panRef = useRef({ x: 0, y: 0 });
  const dragRef = useRef<{ startX: number; startY: number; panX: number; panY: number } | null>(null);

  const filteredData = React.useMemo(() => {
    if (filter === 'all') return data;
    const nodeIds = new Set(data.nodes.filter((n) => n.kind === filter).map((n) => n.id));
    // Include connected nodes
    for (const rel of data.relations) {
      if (nodeIds.has(rel.from)) nodeIds.add(rel.to);
      if (nodeIds.has(rel.to)) nodeIds.add(rel.from);
    }
    return {
      nodes: data.nodes.filter((n) => nodeIds.has(n.id)),
      relations: data.relations.filter((r) => nodeIds.has(r.from) && nodeIds.has(r.to)),
    };
  }, [data, filter]);

  const initSimulation = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const w = canvas.width;
    const h = canvas.height;
    const cx = w / 2;
    const cy = h / 2;

    const nodes: SimNode[] = filteredData.nodes.map((n, i) => {
      const angle = (i / filteredData.nodes.length) * Math.PI * 2;
      const radius = 250 + Math.random() * 200;
      return {
        ...n,
        x: cx + Math.cos(angle) * radius,
        y: cy + Math.sin(angle) * radius,
        vx: 0,
        vy: 0,
      };
    });

    nodesRef.current = nodes;
    return nodes;
  }, [filteredData]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const dpr = window.devicePixelRatio || 1;
    const rect = canvas.getBoundingClientRect();
    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;
    ctx.scale(dpr, dpr);

    const maybeNodes = initSimulation();
    if (!maybeNodes) return;
    const nodes = maybeNodes;

    const nodeMap = new Map(nodes.map((n) => [n.id, n]));
    const w = rect.width;
    const h = rect.height;

    function tick() {
      if (!ctx) return;

      // Simple force simulation
      for (const node of nodes) {
        // Center gravity
        node.vx += (w / 2 - node.x) * 0.0005;
        node.vy += (h / 2 - node.y) * 0.0005;

        // Node repulsion
        for (const other of nodes) {
          if (other === node) continue;
          const dx = node.x - other.x;
          const dy = node.y - other.y;
          const dist = Math.sqrt(dx * dx + dy * dy) || 1;
          const force = 3000 / (dist * dist);
          node.vx += (dx / dist) * force;
          node.vy += (dy / dist) * force;
        }
      }

      // Edge attraction
      for (const rel of filteredData.relations) {
        const a = nodeMap.get(rel.from);
        const b = nodeMap.get(rel.to);
        if (!a || !b) continue;
        const dx = b.x - a.x;
        const dy = b.y - a.y;
        const dist = Math.sqrt(dx * dx + dy * dy) || 1;
        const force = (dist - 250) * 0.003;
        a.vx += (dx / dist) * force;
        a.vy += (dy / dist) * force;
        b.vx -= (dx / dist) * force;
        b.vy -= (dy / dist) * force;
      }

      // Apply velocity with damping
      for (const node of nodes) {
        node.vx *= 0.85;
        node.vy *= 0.85;
        node.x += node.vx;
        node.y += node.vy;
        // Keep in bounds
        node.x = Math.max(30, Math.min(w - 30, node.x));
        node.y = Math.max(30, Math.min(h - 30, node.y));
      }

      // Draw
      ctx.clearRect(0, 0, w, h);
      ctx.save();
      ctx.translate(panRef.current.x, panRef.current.y);
      ctx.scale(zoomRef.current, zoomRef.current);

      // Draw edges
      for (const rel of filteredData.relations) {
        const a = nodeMap.get(rel.from);
        const b = nodeMap.get(rel.to);
        if (!a || !b) continue;
        ctx.beginPath();
        ctx.moveTo(a.x, a.y);
        ctx.lineTo(b.x, b.y);
        ctx.strokeStyle = RELATION_COLORS[rel.type] || '#6b7280';
        ctx.lineWidth = rel.weight * 0.5;
        ctx.globalAlpha = 0.4;
        ctx.stroke();
        ctx.globalAlpha = 1;
      }

      // Draw nodes
      for (const node of nodes) {
        const r = node.kind === 'project' ? 8 : 6;
        ctx.beginPath();
        ctx.arc(node.x, node.y, r, 0, Math.PI * 2);
        ctx.fillStyle = NODE_COLORS[node.kind] || '#6b7280';
        ctx.fill();
        if (node === hoveredNode) {
          ctx.strokeStyle = '#fff';
          ctx.lineWidth = 2;
          ctx.stroke();
        }

        // Label
        ctx.font = '11px system-ui, sans-serif';
        ctx.fillStyle = '#e2e8f0';
        ctx.textAlign = 'center';
        const label = node.label.length > 16 ? node.label.slice(0, 15) + '…' : node.label;
        ctx.fillText(label, node.x, node.y + r + 14);
      }

      ctx.restore();

      animRef.current = requestAnimationFrame(tick);
    }

    tick();
    return () => cancelAnimationFrame(animRef.current);
  }, [filteredData, initSimulation, hoveredNode]);

  function screenToWorld(sx: number, sy: number): [number, number] {
    return [
      (sx - panRef.current.x) / zoomRef.current,
      (sy - panRef.current.y) / zoomRef.current,
    ];
  }

  function handleWheel(e: React.WheelEvent<HTMLCanvasElement>) {
    e.preventDefault();
    const canvas = canvasRef.current;
    if (!canvas) return;
    const rect = canvas.getBoundingClientRect();
    const sx = e.clientX - rect.left;
    const sy = e.clientY - rect.top;

    const [wx, wy] = screenToWorld(sx, sy);
    const delta = -e.deltaY * ZOOM_SENSITIVITY;
    const newZoom = Math.min(MAX_ZOOM, Math.max(MIN_ZOOM, zoomRef.current * (1 + delta)));
    const factor = newZoom / zoomRef.current;

    panRef.current.x = sx - wx * newZoom;
    panRef.current.y = sy - wy * newZoom;
    zoomRef.current = newZoom;
  }

  function handleClick(e: React.MouseEvent<HTMLCanvasElement>) {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const rect = canvas.getBoundingClientRect();
    const [wx, wy] = screenToWorld(e.clientX - rect.left, e.clientY - rect.top);

    for (const node of nodesRef.current) {
      const dx = wx - node.x;
      const dy = wy - node.y;
      if (dx * dx + dy * dy < 100) {
        navigate(routeForNode(node));
        return;
      }
    }
  }

  function handleMouseMove(e: React.MouseEvent<HTMLCanvasElement>) {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const rect = canvas.getBoundingClientRect();
    const [wx, wy] = screenToWorld(e.clientX - rect.left, e.clientY - rect.top);

    // Handle panning
    if (dragRef.current) {
      panRef.current.x = dragRef.current.panX + (e.clientX - dragRef.current.startX);
      panRef.current.y = dragRef.current.panY + (e.clientY - dragRef.current.startY);
      return;
    }

    for (const node of nodesRef.current) {
      const dx = wx - node.x;
      const dy = wy - node.y;
      if (dx * dx + dy * dy < 100) {
        setHoveredNode(node);
        canvas.style.cursor = 'pointer';
        return;
      }
    }
    setHoveredNode(null);
    canvas.style.cursor = 'grab';
  }

  function handleMouseDown(e: React.MouseEvent<HTMLCanvasElement>) {
    // Only start drag on middle click or if no node under cursor
    const canvas = canvasRef.current;
    if (!canvas) return;
    const rect = canvas.getBoundingClientRect();
    const [wx, wy] = screenToWorld(e.clientX - rect.left, e.clientY - rect.top);

    for (const node of nodesRef.current) {
      const dx = wx - node.x;
      const dy = wy - node.y;
      if (dx * dx + dy * dy < 100) return; // clicking a node, don't drag
    }

    dragRef.current = {
      startX: e.clientX,
      startY: e.clientY,
      panX: panRef.current.x,
      panY: panRef.current.y,
    };
    canvas.style.cursor = 'grabbing';
  }

  function handleMouseUp() {
    dragRef.current = null;
    const canvas = canvasRef.current;
    if (canvas) canvas.style.cursor = 'grab';
  }

  function resetView() {
    zoomRef.current = 1;
    panRef.current = { x: 0, y: 0 };
  }

  const kindCounts = React.useMemo(() => {
    const counts: Record<string, number> = {};
    for (const n of data.nodes) {
      counts[n.kind] = (counts[n.kind] || 0) + 1;
    }
    return counts;
  }, [data]);

  return (
    <section className="workspace single-column">
      <article className="detail-panel">
        <div className="eyebrow">知识图谱</div>
        <h2>项目、方案、痛点与资料的关系网络</h2>
        <p className="lead">节点可点击跳转到对应详情页。用筛选器聚焦特定类型，查看它们的关联关系。</p>

        <div className="fact-grid">
          <div className="fact-item">
            <span className="fact-label">节点</span>
            <strong className="fact-value">{data.nodes.length}</strong>
          </div>
          <div className="fact-item">
            <span className="fact-label">关系</span>
            <strong className="fact-value">{data.relations.length}</strong>
          </div>
          {Object.entries(kindCounts).map(([kind, count]) => (
            <div key={kind} className="fact-item">
              <span className="fact-label">{NODE_KIND_LABELS[kind] || kind}</span>
              <strong className="fact-value">{count}</strong>
            </div>
          ))}
        </div>

        <div className="segmented compact" style={{ marginBottom: '1rem' }}>
          {['all', ...Object.keys(NODE_COLORS)].map((kind) => (
            <button
              key={kind}
              className={filter === kind ? 'selected' : ''}
              onClick={() => setFilter(kind)}
            >
              {kind === 'all' ? '全部' : NODE_KIND_LABELS[kind] || kind}
            </button>
          ))}
        </div>

        <div className="graph-legend" style={{ display: 'flex', gap: '1rem', marginBottom: '1rem', flexWrap: 'wrap' }}>
          {Object.entries(RELATION_COLORS).map(([type, color]) => (
            <span key={type} style={{ display: 'flex', alignItems: 'center', gap: '4px', fontSize: '0.85rem' }}>
              <span style={{ width: 20, height: 2, background: color, display: 'inline-block' }} />
              {type}
            </span>
          ))}
        </div>

        <div style={{ position: 'relative' }}>
          <canvas
            ref={canvasRef}
            onClick={handleClick}
            onMouseMove={handleMouseMove}
            onMouseDown={handleMouseDown}
            onMouseUp={handleMouseUp}
            onMouseLeave={handleMouseUp}
            onWheel={handleWheel}
            style={{ width: '100%', height: '700px', background: '#0f172a', borderRadius: '8px', border: '1px solid #1e293b', cursor: 'grab' }}
          />
          <div style={{ position: 'absolute', top: 8, right: 8, display: 'flex', gap: 4 }}>
            <button
              onClick={resetView}
              style={{ background: '#1e293b', color: '#e2e8f0', border: '1px solid #334155', borderRadius: 4, padding: '4px 10px', fontSize: '0.8rem', cursor: 'pointer' }}
            >
              重置视图
            </button>
          </div>
          <div style={{ position: 'absolute', bottom: 8, left: 8, fontSize: '0.75rem', color: '#64748b' }}>
            滚轮缩放 · 拖拽平移 · 点击节点跳转
          </div>
        </div>

        {hoveredNode && (
          <div style={{ marginTop: '0.5rem', padding: '0.5rem', background: '#1e293b', borderRadius: '6px', fontSize: '0.85rem' }}>
            <strong>{hoveredNode.label}</strong>
            <span style={{ marginLeft: '0.5rem', color: NODE_COLORS[hoveredNode.kind] }}>
              {NODE_KIND_LABELS[hoveredNode.kind] || hoveredNode.kind}
            </span>
            {hoveredNode.score != null && <span style={{ marginLeft: '0.5rem' }}>评分 {hoveredNode.score}</span>}
          </div>
        )}
      </article>
    </section>
  );
}
