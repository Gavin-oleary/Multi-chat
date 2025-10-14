/** @type {import('tailwindcss').Config} */
export default {
    content: [
      "./index.html",
      "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
      extend: {
        colors: {
          'claude': '#CC785C',
          'chatgpt': '#10A37F',
          'gemini': '#4285F4',
          'grok': '#000000',
          'perplexity': '#20808D',
        },
      },
    },
    plugins: [],
  }