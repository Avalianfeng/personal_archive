import { useEffect, useRef } from 'react';
import { useUiStore } from '../store/useUiStore';

// 使用 base64 编码的简短氛围音（也可以替换为外部 URL）
// 一期先占位，音频文件可后续替换 public/audio/ambient-space.mp3
export default function AudioSystem() {
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const { audioMuted } = useUiStore();

  useEffect(() => {
    if (!audioRef.current) {
      const audio = new Audio();
      // 尝试加载氛围音频，失败时静默
      audio.loop = true;
      audio.volume = 0;
      audio.preload = 'auto';
      audio.src = '/audio/ambient-space.mp3';

      audio.play().catch(() => {
        // 音频文件不存在或无法播放，静默处理
      });

      audioRef.current = audio;
    }

    return () => {
      audioRef.current?.pause();
      audioRef.current = null;
    };
  }, []);

  useEffect(() => {
    const audio = audioRef.current;
    if (!audio) return;

    if (audioMuted) {
      audio.volume = 0;
    } else {
      // fade in to 0.25
      const fadeIn = () => {
        if (audio.volume < 0.25) {
          audio.volume = Math.min(0.25, audio.volume + 0.02);
          requestAnimationFrame(fadeIn);
        }
      };
      audio.play().catch(() => {});
      fadeIn();
    }
  }, [audioMuted]);

  return null;
}
