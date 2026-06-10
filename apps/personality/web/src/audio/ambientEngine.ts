const TARGET_VOLUME = 0.25;
const AMBIENT_SRC = '/audio/ambient-space.mp3';

interface AmbientBackend {
  start(onFail?: () => void): void;
  fadeTo(volume: number, durationSec: number): void;
  dispose(): void;
}

class Mp3Backend implements AmbientBackend {
  private audio: HTMLAudioElement | null = null;
  private ctx: AudioContext | null = null;
  private gain: GainNode | null = null;
  private active = false;

  start(onFail?: () => void) {
    if (this.active) {
      void this.ctx?.resume();
      void this.audio?.play().catch(() => onFail?.());
      return;
    }

    const audio = new Audio(AMBIENT_SRC);
    audio.loop = true;
    audio.preload = 'auto';
    audio.addEventListener('error', () => onFail?.(), { once: true });

    const ctx = new AudioContext();
    const source = ctx.createMediaElementSource(audio);
    const gain = ctx.createGain();
    gain.gain.value = 0;
    source.connect(gain).connect(ctx.destination);

    this.audio = audio;
    this.ctx = ctx;
    this.gain = gain;
    this.active = true;

    void ctx.resume();
    void audio.play().catch(() => onFail?.());
  }

  fadeTo(volume: number, durationSec: number) {
    if (!this.ctx || !this.gain) return;

    const now = this.ctx.currentTime;
    this.gain.gain.cancelScheduledValues(now);
    this.gain.gain.setValueAtTime(this.gain.gain.value, now);
    this.gain.gain.linearRampToValueAtTime(volume, now + durationSec);
  }

  dispose() {
    this.audio?.pause();
    this.audio = null;
    void this.ctx?.close();
    this.ctx = null;
    this.gain = null;
    this.active = false;
  }
}

/** 柔和 D 小调音簇 — mp3 不可用时的 fallback */
const PAD_NOTES = [
  { freq: 146.83, gain: 0.07 },
  { freq: 220.0, gain: 0.05 },
  { freq: 293.66, gain: 0.04 },
  { freq: 349.23, gain: 0.03 },
  { freq: 440.0, gain: 0.02 },
] as const;

const DETUNE_CENTS = [-11, 0, 9, 14];

function createImpulseReverb(ctx: AudioContext, seconds = 4, decay = 2.8) {
  const length = Math.floor(ctx.sampleRate * seconds);
  const impulse = ctx.createBuffer(2, length, ctx.sampleRate);

  for (let channel = 0; channel < 2; channel++) {
    const data = impulse.getChannelData(channel);
    for (let i = 0; i < length; i++) {
      const t = i / length;
      data[i] = (Math.random() * 2 - 1) * Math.pow(1 - t, decay);
    }
  }

  const convolver = ctx.createConvolver();
  convolver.buffer = impulse;
  return convolver;
}

function createBreathNoise(ctx: AudioContext) {
  const buffer = ctx.createBuffer(1, ctx.sampleRate * 4, ctx.sampleRate);
  const data = buffer.getChannelData(0);
  let brown = 0;

  for (let i = 0; i < data.length; i++) {
    const white = Math.random() * 2 - 1;
    brown = brown * 0.992 + white * 0.008;
    data[i] = brown;
  }

  const source = ctx.createBufferSource();
  source.buffer = buffer;
  source.loop = true;

  const filter = ctx.createBiquadFilter();
  filter.type = 'lowpass';
  filter.frequency.value = 680;
  filter.Q.value = 0.4;

  const gain = ctx.createGain();
  gain.gain.value = 0.035;

  source.connect(filter).connect(gain);
  return { source, gain, filter };
}

class SynthBackend implements AmbientBackend {
  private ctx: AudioContext | null = null;
  private masterGain: GainNode | null = null;
  private sources: Array<OscillatorNode | AudioBufferSourceNode> = [];
  private active = false;

  start() {
    if (this.active && this.ctx) {
      void this.ctx.resume();
      return;
    }

    const ctx = new AudioContext();
    const masterGain = ctx.createGain();
    masterGain.gain.value = 0;

    const dryGain = ctx.createGain();
    dryGain.gain.value = 0.55;

    const wetGain = ctx.createGain();
    wetGain.gain.value = 0.85;

    const reverb = createImpulseReverb(ctx);
    const bus = ctx.createGain();
    bus.connect(dryGain).connect(masterGain);
    bus.connect(reverb).connect(wetGain).connect(masterGain);
    masterGain.connect(ctx.destination);

    const filterLfo = ctx.createOscillator();
    filterLfo.type = 'sine';
    filterLfo.frequency.value = 0.035;
    const filterLfoDepth = ctx.createGain();
    filterLfoDepth.gain.value = 280;

    const padFilter = ctx.createBiquadFilter();
    padFilter.type = 'lowpass';
    padFilter.frequency.value = 920;
    padFilter.Q.value = 0.35;

    filterLfo.connect(filterLfoDepth).connect(padFilter.frequency);
    filterLfo.start();

    const padBus = ctx.createGain();
    padBus.connect(padFilter).connect(bus);

    for (const note of PAD_NOTES) {
      for (const cents of DETUNE_CENTS) {
        const osc = ctx.createOscillator();
        osc.type = 'sine';
        osc.frequency.value = note.freq;
        osc.detune.value = cents;

        const drift = ctx.createOscillator();
        drift.type = 'sine';
        drift.frequency.value = 0.04 + Math.random() * 0.03;
        const driftDepth = ctx.createGain();
        driftDepth.gain.value = note.freq * 0.003;
        drift.connect(driftDepth).connect(osc.frequency);

        const voiceGain = ctx.createGain();
        voiceGain.gain.value = note.gain / DETUNE_CENTS.length;

        osc.connect(voiceGain).connect(padBus);
        drift.start();
        osc.start();
        this.sources.push(osc, drift);
      }
    }

    const sub = ctx.createOscillator();
    sub.type = 'sine';
    sub.frequency.value = 73.42;
    const subGain = ctx.createGain();
    subGain.gain.value = 0.06;
    sub.connect(subGain).connect(bus);
    sub.start();
    this.sources.push(sub);

    const breath = createBreathNoise(ctx);
    const breathLfo = ctx.createOscillator();
    breathLfo.type = 'sine';
    breathLfo.frequency.value = 0.06;
    const breathLfoDepth = ctx.createGain();
    breathLfoDepth.gain.value = 220;
    breathLfo.connect(breathLfoDepth).connect(breath.filter.frequency);
    breath.source.connect(breath.gain).connect(bus);
    breath.source.start();
    breathLfo.start();
    this.sources.push(breath.source, breathLfo, filterLfo);

    void ctx.resume();

    this.ctx = ctx;
    this.masterGain = masterGain;
    this.active = true;
  }

  fadeTo(volume: number, durationSec: number) {
    if (!this.ctx || !this.masterGain) return;

    const now = this.ctx.currentTime;
    this.masterGain.gain.cancelScheduledValues(now);
    this.masterGain.gain.setValueAtTime(this.masterGain.gain.value, now);
    this.masterGain.gain.linearRampToValueAtTime(volume, now + durationSec);
  }

  dispose() {
    for (const source of this.sources) {
      try {
        source.stop();
      } catch {
        // already stopped
      }
    }
    this.sources = [];
    void this.ctx?.close();
    this.ctx = null;
    this.masterGain = null;
    this.active = false;
  }
}

class AmbientAudioEngine {
  private backend: AmbientBackend | null = null;
  private lastMuted = true;
  private preferMp3 = true;

  start() {
    if (this.backend) {
      this.backend.start();
      return;
    }

    if (this.preferMp3) {
      const mp3 = new Mp3Backend();
      mp3.start(() => {
        if (this.backend !== mp3) return;
        mp3.dispose();
        this.preferMp3 = false;
        this.startSynth();
      });
      this.backend = mp3;
      return;
    }

    this.startSynth();
  }

  private startSynth() {
    const synth = new SynthBackend();
    synth.start();
    this.backend = synth;
    synth.fadeTo(this.lastMuted ? 0 : TARGET_VOLUME, this.lastMuted ? 0 : 2);
  }

  fadeTo(volume: number, durationSec: number) {
    this.backend?.fadeTo(volume, durationSec);
  }

  setMuted(muted: boolean) {
    this.lastMuted = muted;
    this.fadeTo(muted ? 0 : TARGET_VOLUME, muted ? 0.5 : 2);
  }

  dispose() {
    this.backend?.dispose();
    this.backend = null;
  }
}

const engine = new AmbientAudioEngine();

export function unlockAmbientAudio() {
  engine.start();
}

export function setAmbientMuted(muted: boolean) {
  engine.setMuted(muted);
}

export function disposeAmbientAudio() {
  engine.dispose();
}
