import { useEffect } from 'react';
import { useUiStore } from '../store/useUiStore';
import { setAmbientMuted } from './ambientEngine';

export default function AudioSystem() {
  const { audioMuted, audioUnlocked } = useUiStore();

  useEffect(() => {
    if (!audioUnlocked) return;
    setAmbientMuted(audioMuted);
  }, [audioMuted, audioUnlocked]);

  return null;
}
