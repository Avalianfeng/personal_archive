import { useSessionStore } from '../store/useSessionStore';
import { useUiStore } from '../store/useUiStore';
import ProgressOrbit from '../components/ProgressOrbit';

export default function TopBar() {
  const { currentIndex, questions, status } = useSessionStore();
  const { audioMuted, unlockAudio, toggleAudio } = useUiStore();
  const total = questions.length;
  const showProgress = status === 'active' && total > 0;

  return (
    <header className="fixed top-0 left-0 right-0 z-50 h-16 flex items-center justify-between px-5 bg-space-void/50 backdrop-blur-sm">
      <span className="text-sm tracking-widest text-star-dim font-serif">
        人格深潜
      </span>

      <div className="flex items-center gap-4">
        {showProgress && (
          <ProgressOrbit current={currentIndex + 1} total={total} />
        )}
        <button
          type="button"
          onClick={() => {
            unlockAudio();
            toggleAudio();
          }}
          className="p-2 -mr-2 text-star-dim hover:text-star-bright transition-colors text-lg"
          aria-label={audioMuted ? '开启声音' : '静音'}
        >
          {audioMuted ? '🔇' : '🔊'}
        </button>
      </div>
    </header>
  );
}
