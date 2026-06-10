import { Outlet } from 'react-router-dom';
import { AnimatePresence } from 'framer-motion';
import TopBar from './TopBar';
import ParticleBackground from '../effects/ParticleBackground';
import AudioSystem from '../audio/AudioSystem';

export default function AppShell() {
  return (
    <div className="relative min-h-screen overflow-hidden bg-space-void">
      <ParticleBackground />
      <AudioSystem />
      <TopBar />
      <main className="relative z-10 max-w-lg mx-auto px-5 pt-20 pb-24">
        <AnimatePresence mode="wait">
          <Outlet />
        </AnimatePresence>
      </main>
    </div>
  );
}
