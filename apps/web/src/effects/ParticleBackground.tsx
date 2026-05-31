import { useCallback, useEffect, useState } from 'react';
import Particles, { initParticlesEngine } from '@tsparticles/react';
import { loadSlim } from '@tsparticles/slim';
import { useUiStore } from '../store/useUiStore';

const STAR_POSITIONS = Array.from({ length: 30 }, () => ({
  left: `${Math.random() * 100}%`,
  top: `${Math.random() * 100}%`,
  size: Math.random() * 2 + 1,
  delay: Math.random() * 4,
}));

export default function ParticleBackground() {
  const [init, setInit] = useState(false);
  const { reducedMotion } = useUiStore();

  useEffect(() => {
    initParticlesEngine(async (engine) => {
      await loadSlim(engine);
    }).then(() => setInit(true));
  }, []);

  if (!init || reducedMotion) {
    // 静态星图降级
    return (
      <div className="fixed inset-0 z-0 pointer-events-none">
        {STAR_POSITIONS.map((star, i) => (
          <div
            key={i}
            className="absolute rounded-full bg-star-dim"
            style={{
              left: star.left,
              top: star.top,
              width: star.size,
              height: star.size,
              opacity: 0.2 + Math.sin(star.delay) * 0.3,
              animation: `twinkle ${3 + star.delay}s ease-in-out infinite`,
            }}
          />
        ))}
      </div>
    );
  }

  return (
    <Particles
      id="tsparticles"
      className="fixed inset-0 z-0"
      options={{
        fpsLimit: 60,
        particles: {
          number: {
            value: 60,
            density: { enable: true },
          },
          color: {
            value: ['#8b9dc3', '#a78bfa'],
          },
          opacity: {
            value: { min: 0.2, max: 0.5 },
          },
          size: {
            value: { min: 0.5, max: 2 },
          },
          move: {
            enable: true,
            speed: 0.3,
            direction: 'none',
            random: true,
            straight: false,
            outModes: { default: 'bounce' },
          },
          links: {
            enable: false,
          },
        },
        interactivity: {
          events: {
            onHover: {
              enable: true,
              mode: 'repulse',
            },
          },
          modes: {
            repulse: {
              distance: 80,
              duration: 0.4,
              factor: 2,
            },
          },
        },
        detectRetina: true,
      }}
    />
  );
}
