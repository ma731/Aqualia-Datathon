import { useMemo } from "react";

type Props = {
  count?: number;
  className?: string;
  color?: string;
  minSize?: number;
  maxSize?: number;
};

export default function WaterDroplets({
  count = 36,
  className = "",
  color = "#5db9d9",
  minSize = 2,
  maxSize = 5,
}: Props) {
  const drops = useMemo(() => {
    const seed = (i: number) => {
      // Deterministic-ish pseudo random so droplets don't jump on rerenders
      const x = Math.sin(i * 9973.13) * 10000;
      return x - Math.floor(x);
    };
    return Array.from({ length: count }, (_, i) => {
      const size = minSize + seed(i * 3 + 1) * (maxSize - minSize);
      return {
        id: i,
        left: seed(i * 7 + 2) * 100,
        delay: -seed(i * 11 + 3) * 12,
        duration: 5 + seed(i * 13 + 5) * 9,
        size,
        opacity: 0.25 + seed(i * 17 + 7) * 0.45,
        blur: seed(i * 19 + 11) * 0.8,
      };
    });
  }, [count, minSize, maxSize]);

  return (
    <div
      aria-hidden
      className={`absolute inset-0 overflow-hidden pointer-events-none ${className}`}
    >
      {drops.map((d) => (
        <span
          key={d.id}
          className="absolute block rounded-full animate-drop-fall"
          style={{
            left: `${d.left}%`,
            top: 0,
            width: `${d.size}px`,
            height: `${d.size * 3.2}px`,
            opacity: d.opacity,
            animationDelay: `${d.delay}s`,
            animationDuration: `${d.duration}s`,
            background: `linear-gradient(180deg, ${color}88 0%, ${color} 60%, ${color}aa 100%)`,
            boxShadow: `0 0 6px ${color}66`,
            filter: `blur(${d.blur}px)`,
            willChange: "transform, opacity",
          }}
        />
      ))}
    </div>
  );
}
