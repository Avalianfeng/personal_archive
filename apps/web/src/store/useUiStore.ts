import { create } from 'zustand';

interface UiStore {
  audioMuted: boolean;
  reducedMotion: boolean;
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
  reducedMotion: prefersReduced,

  toggleAudio: () =>
    set((s) => {
      const next = !s.audioMuted;
      localStorage.setItem('renge_shenqian_audio_muted', String(next));
      return { audioMuted: next };
    }),

  setReducedMotion: (value) => set({ reducedMotion: value }),
}));
