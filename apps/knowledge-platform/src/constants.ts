import React from 'react';
import {
  AlertTriangle,
  BrainCircuit,
  ClipboardList,
  FileQuestion,
  FileSearch,
  FolderKanban,
  GitBranch,
  Layers3,
  MessageSquareText,
  Radar,
  Sparkles,
} from 'lucide-react';

export type View =
  | 'distill-desk'
  | 'projects'
  | 'solutions'
  | 'pain-points'
  | 'engineering-logic'
  | 'sources'
  | 'interviews'
  | 'interviewer'
  | 'radar'
  | 'feedback'
  | 'visual-generation';

export type ReaderKind = 'project' | 'solution' | 'pain-point' | 'source' | 'engineering-logic';

export type ReaderTarget = {
  kind: ReaderKind;
  id: string;
};

export type ReaderDocument = {
  kind: ReaderKind;
  id: string;
  title: string;
  eyebrow: string;
  summary: string;
  sourceFile: string;
  content: string;
  badges: string[];
  quickFacts: Array<{ label: string; value: string }>;
  guideCards: Array<{ title: string; body: string }>;
  actionItems: string[];
};

export const navItems: Array<{ id: View; label: string; icon: React.ComponentType<{ size?: number }> }> = [
  { id: 'distill-desk', label: '沉淀台', icon: ClipboardList },
  { id: 'projects', label: '项目', icon: FolderKanban },
  { id: 'solutions', label: '方案', icon: Layers3 },
  { id: 'pain-points', label: '痛点', icon: AlertTriangle },
  { id: 'engineering-logic', label: '工程逻辑', icon: GitBranch },
  { id: 'sources', label: '资料源', icon: FileSearch },
  { id: 'interviews', label: '面经', icon: FileQuestion },
  { id: 'interviewer', label: 'AI 面试官', icon: BrainCircuit },
  { id: 'radar', label: '雷达', icon: Radar },
  { id: 'feedback', label: '反馈', icon: MessageSquareText },
  { id: 'visual-generation', label: '视觉生成', icon: Sparkles },
];

export const viewMeta: Record<View, { title: string; subtitle: string }> = {
  'distill-desk': {
    title: '沉淀工作台',
    subtitle: '直接录入要沉淀的项目、资料或本地仓库，自动生成给 Codex 的沉淀指令、推荐命令与输出落点。',
  },
  projects: {
    title: '项目样本库',
    subtitle: '按项目类型、状态、评分和沉淀深度查看外部样本与自研项目，直接进入真正值得学习的内容。',
  },
  solutions: {
    title: '方案方法库',
    subtitle: '把多个项目背后的共性问题抽象成可迁移的工程框架、实践套路与当前行动项。',
  },
  'pain-points': {
    title: '行业痛点库',
    subtitle: '围绕 Agent 与大模型行业的普遍难题，持续沉淀证据项目、成熟做法、数据信号与平台启发。',
  },
  'engineering-logic': {
    title: '工程逻辑总纲',
    subtitle: '把项目、方案、痛点与资料源收束成真实项目的设计顺序、验证方法与迭代主线。',
  },
  sources: {
    title: '外部资料源',
    subtitle: '统一管理 GitHub、博客、论文和用户文档，让外部资料进入可沉淀、可学习、可反哺的平台流水线。',
  },
  interviews: {
    title: '面经与答案',
    subtitle: '把问题、答题骨架、追问方向与关联项目串起来，形成真正能练习和复盘的题库。',
  },
  interviewer: {
    title: 'AI 面试官',
    subtitle: '围绕当前项目、平台沉淀与外部高质量样本，训练项目表达、取舍判断与工程解释能力。',
  },
  radar: {
    title: 'Project Radar',
    subtitle: '跟踪项目发现、评分、候选池和沉淀状态，让知识库具备持续主动学习能力。',
  },
  feedback: {
    title: '阅读反馈',
    subtitle: '把你在阅读文档过程中的"有帮助 / 需补强 / 备注"沉淀成后续改写与追问输入。',
  },
  'visual-generation': {
    title: '视觉生成工作流',
    subtitle: '把 DESIGN.md、页面风格样本、生成图与真实前端实现串成稳定的中文页面设计流程。',
  },
};
