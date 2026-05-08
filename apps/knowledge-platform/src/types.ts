export type Project = {
  id: string;
  name: string;
  url?: string;
  summary: string;
  types: string[];
  primaryCategory: string;
  businessScenario: string;
  biggestHighlight: string;
  oneLineVerdict: string;
  whyReadNow: string;
  oralAnswer?: string;
  engineeringPitch?: string;
  status: string;
  score?: number;
  sourceFile: string;
  relatedPatterns: string[];
  writebackTargets?: {
    patterns: string[];
    painPoints: string[];
    interviews: string[];
  };
  writebackSummary?: string;
  writebackStatus?: 'completed' | 'partial' | 'skipped' | 'none';
  writebackUpdatedAt?: string;
  writebackReasoning?: string[];
  nextActions: string[];
  scenarioSection?: string;
  problemSection?: string;
  solutionSection?: string;
  frameworkSection?: string;
  principleSection?: string;
  actionSection?: string;
  tradeoffSection?: string;
  content: string;
};

export type Solution = {
  id: string;
  title: string;
  problemDefinition: string;
  whyImportant: string[];
  commonMistakes: string[];
  maturePractices: string[];
  actions: string[];
  structureSection?: string;
  practiceSection?: string;
  mistakeSection?: string;
  actionSection?: string;
  sourceFile: string;
  content: string;
};

export type PainPoint = {
  id: string;
  title: string;
  topic: string;
  severity: 'high' | 'medium' | 'low';
  industryPain?: string;
  evidenceSources?: string[];
  evidenceProjects: string[];
  relatedSolution: string;
  solutionMethod: string;
  maturePractices?: string[];
  commonPractices?: string[];
  dataSignals?: string[];
  evolutionRule?: string;
  evidenceProjectCount?: number;
  lastUpdatedFromProjects?: string[];
  lastUpdatedAt?: string;
  sourceFile?: string;
  commonMistakes: string[];
  actions: string[];
  content?: string;
};

export type SourceItem = {
  id: string;
  title: string;
  sourceType: string;
  evidenceStrength: 'high' | 'medium' | 'low';
  summary: string;
  sourceFile: string;
  relatedPainPoints: string[];
  relatedPatterns: string[];
  recommendedUse?: string;
  actions: string[];
  valueSection?: string;
  insightSection?: string;
  writebackSection?: string;
  content: string;
};

export type InterviewItem = {
  id: string;
  rawQuestion: string;
  questionType: string;
  knowledgePoints: string[];
  relatedProjects: string[];
  relatedPatterns: string[];
  recommendedAnswer: string;
  followUps: string[];
  evidenceSource?: string;
};

export type SearchItem = {
  id: string;
  entityId: string;
  kind: 'project' | 'solution' | 'painPoint' | 'source' | 'interview';
  title: string;
  summary: string;
  sourceFile: string;
  tags: string[];
  context: string;
  searchableText: string;
};

export type EngineeringLogic = {
  title: string;
  summary: string;
  sourceFile: string;
  stages: Array<{
    title: string;
    route: string;
    purpose: string;
  }>;
  routeMap?: Array<{
    title: string;
    route: string;
    purpose: string;
    output: string;
  }>;
  currentFocus: string[];
  riskBoundaries?: string[];
  validationChecklist?: string[];
  recommendedOrder?: string[];
  actions: string[];
  content: string;
};

export type KnowledgeIndex = {
  generatedAt: string;
  language: string;
  projects: Project[];
  solutions: Solution[];
  painPoints: PainPoint[];
  sources: SourceItem[];
  searchIndex: SearchItem[];
  engineeringLogic: EngineeringLogic;
  interviews: {
    questionCount: number;
    items: InterviewItem[];
    memory: {
      focus: string;
      answerStyle: string;
      weakSpots: string[];
    };
  };
};

export type RelationType = 'supports' | 'solves' | 'implements' | 'evidence-for' | 'related';

export type Relation = {
  from: string;
  to: string;
  type: RelationType;
  weight: number;
};

export type GraphNode = {
  id: string;
  label: string;
  kind: 'project' | 'solution' | 'painPoint' | 'source' | 'interview';
  score?: number;
};

export type GraphData = {
  nodes: GraphNode[];
  relations: Relation[];
};
