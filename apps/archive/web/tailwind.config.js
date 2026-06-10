/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        paper: '#fafafa',
        ink: '#1a1a1a',
        'ink-muted': '#6b7280',
        'ink-faint': '#9ca3af',
        border: '#e5e7eb',
        accent: '#2563eb',
        'accent-hover': '#1d4ed8',
      },
      fontFamily: {
        sans: ['"Inter"', '"PingFang SC"', '"Microsoft YaHei"', 'sans-serif'],
        mono: ['"JetBrains Mono"', '"Consolas"', 'monospace'],
      },
    },
  },
  plugins: [],
};
