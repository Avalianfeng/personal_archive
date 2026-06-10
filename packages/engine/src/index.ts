export type {
  ArchiveSection,
  ArchiveQuestion,
  ArchiveQuestionOption,
  ArchiveAnswer,
  ArchiveBasicData,
  ArchiveSocialData,
  ArchiveCareerData,
  ArchiveInnerData,
  ArchiveData,
  PersonArchive,
  ArchiveReport,
  ArchiveReportSection,
  SynthesisGenerator,
} from './types';

export { ARCHIVE_QUESTIONS, getQuestionById } from './questions';
export { mapAnswersToData, computeCompleteness, buildArchive } from './mapAnswers';
export { renderMarkdown } from './report/renderMarkdown';
export { FIELD_LABELS, INNER_QUESTION_LABELS } from './report/fieldLabels';
export {
  StubSynthesisGenerator,
  defaultSynthesisGenerator,
} from './report/synthesis';
