export type ArchiveSection = 'basic' | 'social' | 'career' | 'inner';

export interface ArchiveQuestionOption {
  key: string;
  label: string;
}

export interface ArchiveQuestion {
  id: string;
  section: ArchiveSection;
  type: 'choice' | 'text';
  question: string;
  options?: ArchiveQuestionOption[];
  placeholder?: string;
  maxLength?: number;
  mapsTo: string;
  skippable: true;
}

export interface ArchiveAnswer {
  questionId: string;
  skipped: boolean;
  optionKey?: string;
  optionLabel?: string;
  textAnswer?: string;
}

export interface ArchiveBasicData {
  displayName?: string;
  ageRange?: string;
  location?: string;
}

export interface ArchiveSocialData {
  relationshipStatus?: string;
  socialCircle?: string;
}

export interface ArchiveCareerData {
  careerStage?: string;
  occupation?: string;
}

export interface ArchiveInnerData {
  currentPriority?: string;
  decisionStyle?: string;
  additionalNotes?: string;
}

export interface ArchiveData {
  basic: ArchiveBasicData;
  social: ArchiveSocialData;
  career: ArchiveCareerData;
  inner: ArchiveInnerData;
}

export interface PersonArchive {
  id: string;
  answers: ArchiveAnswer[];
  data: ArchiveData;
  completeness: number;
  createdAt: string;
  updatedAt: string;
}

export interface ArchiveReportSection {
  id: string;
  title: string;
  content: string;
}

export interface ArchiveReport {
  archiveId: string;
  generatedAt: string;
  completeness: number;
  sections: ArchiveReportSection[];
  markdown: string;
}

export interface SynthesisGenerator {
  generate(archive: PersonArchive): Promise<string>;
}
