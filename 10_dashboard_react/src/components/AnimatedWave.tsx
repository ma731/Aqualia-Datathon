type Props = {
  color?: string;
  height?: number;
  flipY?: boolean;
  className?: string;
};

/**
 * Horizontally-scrolling SVG wave used as a section divider.
 * Two identical wave paths are drawn side-by-side and translated
 * together inside an animated group for a seamless loop.
 */
export default function AnimatedWave({
  color = "#ffffff",
  height = 100,
  flipY = false,
  className = "",
}: Props) {
  return (
    <div
      aria-hidden
      className={`absolute left-0 right-0 overflow-hidden pointer-events-none ${className}`}
      style={{ height, ...(flipY ? { top: -1 } : { bottom: -1 }) }}
    >
      <svg
        viewBox="0 0 2880 120"
        width="2880"
        height={height}
        preserveAspectRatio="none"
        style={{
          position: "absolute",
          left: 0,
          top: 0,
          transform: flipY ? "scaleY(-1)" : undefined,
          minWidth: "200%",
          height,
        }}
      >
        <g className="animate-wave-flow">
          <path
            d="M0,80 C240,120 480,40 720,60 C960,80 1200,110 1440,70 L1440,120 L0,120 Z"
            fill={color}
          />
          <path
            d="M1440,80 C1680,120 1920,40 2160,60 C2400,80 2640,110 2880,70 L2880,120 L1440,120 Z"
            fill={color}
          />
        </g>
      </svg>
      {/* Secondary slower layer for depth */}
      <svg
        viewBox="0 0 2880 120"
        width="2880"
        height={height}
        preserveAspectRatio="none"
        style={{
          position: "absolute",
          left: 0,
          top: 0,
          transform: flipY ? "scaleY(-1)" : undefined,
          minWidth: "200%",
          height,
          opacity: 0.5,
          animationDuration: "32s",
        }}
      >
        <g className="animate-wave-flow" style={{ animationDuration: "32s" }}>
          <path
            d="M0,90 C300,50 600,110 900,80 C1200,50 1440,90 1440,90 L1440,120 L0,120 Z"
            fill={color}
          />
          <path
            d="M1440,90 C1740,50 2040,110 2340,80 C2640,50 2880,90 2880,90 L2880,120 L1440,120 Z"
            fill={color}
          />
        </g>
      </svg>
    </div>
  );
}
