import type { ArchiveAnswer, ArchiveReport, PersonArchive } from '../types';
import { ARCHIVE_QUESTIONS } from '../questions';
import { FIELD_LABELS, INNER_QUESTION_LABELS } from './fieldLabels';

const UNFILLED = '未填写';

function formatDate(iso: string): string {
  const d = new Date(iso);
  return d.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  });
}

function formatCompleteness(ratio: number): string {
  return `${Math.round(ratio * 100)}%`;
}

function getFieldValue(data: PersonArchive['data'], path: string): string {
  const parts = path.split('.');
  let current: unknown = data;
  for (const part of parts) {
    if (current === null || current === undefined || typeof current !== 'object') {
      return UNFILLED;
    }
    current = (current as Record<string, unknown>)[part];
  }
  if (typeof current === 'string' && current.trim()) {
    return current.trim();
  }
  return UNFILLED;
}

function buildOverview(archive: PersonArchive): string {
  const name = getFieldValue(archive.data, 'basic.displayName');
  const age = getFieldValue(archive.data, 'basic.ageRange');
  const location = getFieldValue(archive.data, 'basic.location');
  const occupation = getFieldValue(archive.data, 'career.occupation');

  const parts: string[] = [];
  if (name !== UNFILLED) parts.push(name);
  if (age !== UNFILLED) parts.push(age);
  if (location !== UNFILLED) parts.push(`现居 ${location}`);
  if (occupation !== UNFILLED) parts.push(occupation);

  if (parts.length === 0) {
    return '档案信息尚不完整，请继续填写以生成更完整的概览。';
  }

  return parts.join(' · ');
}

function buildTableRows(paths: string[], archive: PersonArchive): string {
  return paths
    .map((path) => {
      const label = FIELD_LABELS[path] ?? path;
      const value = getFieldValue(archive.data, path);
      return `| ${label} | ${value} |`;
    })
    .join('\n');
}

function buildInnerRawSection(answers: ArchiveAnswer[]): string {
  const innerAnswers = answers.filter((a) => {
    if (a.skipped) return false;
    const q = ARCHIVE_QUESTIONS.find((item) => item.id === a.questionId);
    return q?.section === 'inner';
  });

  if (innerAnswers.length === 0) {
    return '_暂无内心自述内容。_';
  }

  return innerAnswers
    .map((a) => {
      const label = INNER_QUESTION_LABELS[a.questionId] ?? a.questionId;
      const text = a.textAnswer?.trim() ?? '';
      return `- **${label}** ${text}`;
    })
    .join('\n');
}

export function renderMarkdown(archive: PersonArchive): ArchiveReport {
  const generatedAt = archive.updatedAt;
  const overview = buildOverview(archive);

  const basicTable = buildTableRows(
    ['basic.displayName', 'basic.ageRange', 'basic.location'],
    archive,
  );

  const socialCareerTable = buildTableRows(
    [
      'social.relationshipStatus',
      'social.socialCircle',
      'career.careerStage',
      'career.occupation',
    ],
    archive,
  );

  const innerRaw = buildInnerRawSection(archive.answers);

  const markdown = `# 个人档案报告

> 生成时间：${formatDate(generatedAt)} · 完整度：${formatCompleteness(archive.completeness)}

## 一、概览

${overview}

## 二、基本信息

| 字段 | 内容 |
| --- | --- |
${basicTable}

## 三、社会与职业

| 字段 | 内容 |
| --- | --- |
${socialCareerTable}

## 四、内心与价值观

### 原始自述

${innerRaw}

## 五、综合解读

> _本节待 AI 生成，提示词配置后将自动填充。_
`;

  return {
    archiveId: archive.id,
    generatedAt,
    completeness: archive.completeness,
    sections: [
      { id: 'overview', title: '概览', content: overview },
      { id: 'objective_basic', title: '基本信息', content: basicTable },
      {
        id: 'objective_social_career',
        title: '社会与职业',
        content: socialCareerTable,
      },
      { id: 'inner_raw', title: '内心与价值观', content: innerRaw },
      {
        id: 'synthesis',
        title: '综合解读',
        content: '本节待 AI 生成，提示词配置后将自动填充。',
      },
    ],
    markdown,
  };
}
