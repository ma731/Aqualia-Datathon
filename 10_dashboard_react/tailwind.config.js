/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "monospace"],
        display: ["'Fraunces'", "Georgia", "serif"],
      },
      colors: {
        navy: "#002f5f",
        navy2: "#001a38",
        deep: "#0b4f74",
        aqua: "#5db9d9",
        aqua2: "#8ed3e6",
        sand: "#d6cdb7",
        slate2: "#4a5663",
        paper: "#ffffff",
        ink: "#0a1a2b",
        grid: "#e6e8eb",
        t1: "#1f77b4",
        t2: "#ff7f0e",
        t3: "#2ca02c",
        badred: "#c83c35",
        amber: "#f2b039",
        green2: "#1b7f3b",
      },
      boxShadow: {
        glow: "0 30px 60px -20px rgba(0,47,95,0.35)",
        soft: "0 10px 40px -15px rgba(0,47,95,0.22)",
        ring: "0 0 0 1px rgba(0,47,95,0.06), 0 20px 40px -20px rgba(0,47,95,0.18)",
      },
      backgroundImage: {
        "hero-grad":
          "radial-gradient(ellipse at top left, rgba(93,185,217,0.30) 0%, transparent 55%), radial-gradient(ellipse at bottom right, rgba(31,119,180,0.25) 0%, transparent 60%), linear-gradient(180deg, #001a38 0%, #002f5f 50%, #0b4f74 100%)",
        "aqua-sheen":
          "linear-gradient(135deg, rgba(93,185,217,0.16) 0%, rgba(0,47,95,0.04) 100%)",
      },
      keyframes: {
        float: {
          "0%,100%": { transform: "translateY(0)" },
          "50%": { transform: "translateY(-12px)" },
        },
        shimmer: {
          "0%": { backgroundPosition: "-1000px 0" },
          "100%": { backgroundPosition: "1000px 0" },
        },
        drift: {
          "0%": { transform: "translateX(0)" },
          "100%": { transform: "translateX(-50%)" },
        },
        pulseRing: {
          "0%": { transform: "scale(1)", opacity: "0.5" },
          "100%": { transform: "scale(2.0)", opacity: "0" },
        },
        drop: {
          "0%": {
            transform: "translateY(-20vh) scaleY(0.6)",
            opacity: "0",
          },
          "15%": { opacity: "0.85" },
          "90%": { opacity: "0.7" },
          "100%": {
            transform: "translateY(115vh) scaleY(1.3)",
            opacity: "0",
          },
        },
        ripple: {
          "0%": { transform: "scale(0)", opacity: "0.55" },
          "100%": { transform: "scale(3.2)", opacity: "0" },
        },
        waveFlow: {
          "0%": { transform: "translate3d(0,0,0)" },
          "100%": { transform: "translate3d(-1440px,0,0)" },
        },
      },
      animation: {
        float: "float 7s ease-in-out infinite",
        shimmer: "shimmer 2.5s linear infinite",
        drift: "drift 48s linear infinite",
        "pulse-ring": "pulseRing 2.2s infinite",
        "drop-fall": "drop 8s linear infinite",
        ripple: "ripple 2.6s ease-out infinite",
        "wave-flow": "waveFlow 18s linear infinite",
      },
    },
  },
  plugins: [],
};
