import { create } from 'zustand';
import { unlockAmbientAudio } from '../audio/ambientEngine';

interface UiStore {
  audioMuted: boolean;
  audioUnlocked: boolean;
  reducedMotion: boolean;
  unlockAudio: () => void;
  toggleAudio: () => void;
  setReducedMotion: (value: boolean) => void;
}

const storedMuted = typeof window !== 'undefined'
  ? localStorage.getItem('renge_shenqian_audio_muted') === 'true'
  : false;

const prefersReduced = typeof window !== 'undefined'
  ? window.matchMedia('(prefers-reduced-motion: reduce)').matches
  : false;

export const useUiStore = create<UiStore>((set) => ({
  audioMuted: storedMuted || prefersReduced,
  audioUnlocked: false,
  reducedMotion: prefersReduced,

  unlockAudio: () => {
    try {
      unlockAmbientAudio();
    } catch {
      // 音频初始化失败不应阻断 UI 交互
    }
    set({ audioUnlocked: true });
  },

  toggleAudio: () =>
    set((s) => {
      const next = !s.audioMuted;
      localStorage.setItem('renge_shenqian_audio_muted', String(next));
      return { audioMuted: next };
    }),

  setReducedMotion: (value) => set({ reducedMotion: value }),
}));
