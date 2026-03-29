/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          green: '#2D6A4F',
          'green-light': '#40916C',
          'green-lighter': '#52B788',
          'green-pale': '#D8F3DC',
          orange: '#E76F51',
          'orange-light': '#F4A261',
          brown: '#BC6C25',
          'brown-light': '#DDA15E',
          sand: '#FEFAE0',
          cream: '#F5F0E8',
        },
      },
      fontFamily: {
        sans: ['"Noto Sans SC"', 'system-ui', 'sans-serif'],
      },
      keyframes: {
        'worm-wiggle': {
          '0%, 100%': { transform: 'translateX(0) rotate(0deg)' },
          '25%': { transform: 'translateX(-3px) rotate(-3deg)' },
          '75%': { transform: 'translateX(3px) rotate(3deg)' },
        },
        'tunnel-emerge': {
          '0%': { transform: 'translateY(30px) scale(0.8)', opacity: '0' },
          '60%': { transform: 'translateY(-5px) scale(1.02)', opacity: '1' },
          '100%': { transform: 'translateY(0) scale(1)', opacity: '1' },
        },
        'number-roll': {
          '0%': { transform: 'translateY(0)' },
          '100%': { transform: 'translateY(-100%)' },
        },
      },
      animation: {
        'worm-wiggle': 'worm-wiggle 2s ease-in-out infinite',
        'tunnel-emerge': 'tunnel-emerge 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards',
        'number-roll': 'number-roll 0.3s ease-out',
      },
    },
  },
  plugins: [],
}
