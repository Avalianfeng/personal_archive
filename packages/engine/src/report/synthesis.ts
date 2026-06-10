import type { PersonArchive, SynthesisGenerator } from '../types';

/** P0 stub — returns placeholder until LLM prompts are configured. */
export class StubSynthesisGenerator implements SynthesisGenerator {
  async generate(_archive: PersonArchive): Promise<string> {
    return '本节待 AI 生成，提示词配置后将自动填充。';
  }
}

export const defaultSynthesisGenerator: SynthesisGenerator = new StubSynthesisGenerator();
