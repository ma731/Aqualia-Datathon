import { useMemo } from "react";

type Props = {
  count?: number;
  className?: string;
  color?: string;
};

export default function Ripples({
  count = 5,
  className = "",
  color = "#5db9d9",
}: Props) {
  const pts = useMemo(() => {
    const seed = (i: number) => {
      const x = Math.sin(i * 7321.7) * 10000;
      return x - Math.floor(x);
    };
    return Array.from({ length: count }, (_, i) => ({
      id: i,
      left: 10 + seed(i * 3 + 1) * 80,
      delay: -seed(i * 7 + 2) * 3,
      duration: 2.2 + seed(i * 11 + 4) * 1.8,
      size: 30 + seed(i * 13 + 6) * 40,
    }));
  }, [count]);

  return (
    <div
      aria-hidden
      className={`absolute left-0 right-0 bottom-0 h-24 pointer-events-none ${className}`}
    >
      {pts.map((p) => (
        <span
          key={p.id}
          className="absolute rounded-full animate-ripple"
          style={{
            left: `${p.left}%`,
            bottom: 12,
            width: `${p.size}px`,
            height: `${p.size / 3}px`,
            border: `2px solid ${color}`,
            animationDelay: `${p.delay}s`,
            animationDuration: `${p.duration}s`,
            transformOrigin: "center",
          }}
        />
      ))}
    </div>
  );
}
