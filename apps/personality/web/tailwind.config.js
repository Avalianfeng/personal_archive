/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        'space-void': '#050508',
        'space-deep': '#0a0e1a',
        'nebula-purple': 'rgba(107, 76, 230, 0.12)',
        'nebula-cyan': 'rgba(61, 214, 208, 0.08)',
        'star-dim': '#8b9dc3',
        'star-bright': '#e8edf7',
        'accent-glow': '#a78bfa',
        'danger-soft': '#f59e0b',
      },
      fontFamily: {
        serif: ['"Noto Serif SC"', '"Source Han Serif SC"', '"SimSun"', 'serif'],
        sans: ['"Inter"', '"PingFang SC"', '"Microsoft YaHei"', 'sans-serif'],
      },
    },
  },
  plugins: [],
};
