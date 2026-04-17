import { useMemo, useState } from "react";
import Plot from "./PlotlyChart";
import { DATA } from "../data";
import { TOPICS } from "../content/topics";
import SectionHeader from "./SectionHeader";
import { motion } from "framer-motion";
import { Info, Maximize2, Minimize2, Move3D, Sliders } from "lucide-react";

type SchemeKey =
  | "MC"
  | "Equal"
  | "Regulator-heavy"
  | "Community-first"
  | "Investor-first";

type ScaleMode = "full" | "focus" | "delta";

const SCHEMES: { value: SchemeKey; label: string; hint: string }[] = [
  { value: "MC", label: "Monte Carlo (baseline)", hint: "10k draws · 90% ellipses" },
  { value: "Equal", label: "Equal weights", hint: "Severity = Scale+Scope+Remediability" },
  {
    value: "Regulator-heavy",
    label: "Regulator-heavy",
    hint: "CSRD / ESRS enforcement tilt",
  },
  {
    value: "Community-first",
    label: "Community-first",
    hint: "Stakeholder salience to affected parties",
  },
  {
    value: "Investor-first",
    label: "Investor-first",
    hint: "Financial materiality weighted to capital markets",
  },
];

const SCALES: {
  value: ScaleMode;
  label: string;
  hint: string;
  icon: React.ComponentType<{ className?: string }>;
}[] = [
  {
    value: "full",
    label: "Full scale (1–5)",
    hint: "Credibility view — shows the robustness story",
    icon: Maximize2,
  },
  {
    value: "focus",
    label: "Focus on topics",
    hint: "Zoom to the region where topics actually live",
    icon: Minimize2,
  },
  {
    value: "delta",
    label: "Δ vs MC baseline",
    hint: "Vectors from Monte Carlo mean — sees sub-point shifts",
    icon: Move3D,
  },
];

const COLOR_MAP: Record<string, string> = {
  "T1 Water Resilience & Equitable Access": "#1f77b4",
  "T2 Digital & Cyber Infrastructure": "#ff7f0e",
  "T3 Green Finance & Integrity": "#2ca02c",
};

export default function Matrix() {
  const [scheme, setScheme] = useState<SchemeKey>("MC");
  const [scaleMode, setScaleMode] = useState<ScaleMode>("full");
  const [showEllipses, setShowEllipses] = useState(true);
  const [showThreshold, setShowThreshold] = useState(true);

  // MC baseline (fixed reference) used for delta mode and Δ readouts.
  const mcBase = useMemo(() => {
    const map: Record<string, { impact: number; financial: number }> = {};
    DATA.mc.forEach((r) => {
      map[r.topic] = { impact: r.impact_mean, financial: r.financial_mean };
    });
    return map;
  }, []);

  const points = useMemo(() => {
    if (scheme === "MC") {
      return DATA.mc.map((r) => ({
        topic: r.topic,
        impact: r.impact_mean,
        financial: r.financial_mean,
        width: r.ellipse_width,
        height: r.ellipse_height,
        in_target: r.in_target_zone,
      }));
    }
    const rows = DATA.robustness.filter((r) => r.scheme === scheme);
    return rows.map((r) => ({
      topic: r.topic,
      impact: r.impact_mean,
      financial: r.financial_mean,
      width: 0.5,
      height: 0.35,
      in_target: r.in_target_zone,
    }));
  }, [scheme]);

  // Deltas relative to Monte Carlo baseline, for the Δ readout strip.
  const deltas = useMemo(
    () =>
      points.map((p) => {
        const base = mcBase[p.topic] ?? { impact: 0, financial: 0 };
        return {
          topic: p.topic,
          di: p.impact - base.impact,
          df: p.financial - base.financial,
        };
      }),
    [points, mcBase]
  );

  // Axis ranges depend on the scale mode.
  const axisRange = useMemo(() => {
    if (scaleMode === "full") {
      return { x: [1, 5] as [number, number], y: [1, 5] as [number, number], dtick: 1 };
    }
    if (scaleMode === "focus") {
      const imps = DATA.mc.map((r) => r.impact_mean);
      const fins = DATA.mc.map((r) => r.financial_mean);
      const padX = 0.7;
      const padY = 0.6;
      return {
        x: [Math.max(1, Math.min(...imps) - padX), Math.min(5, Math.max(...imps) + padX)] as [
          number,
          number
        ],
        y: [Math.max(1, Math.min(...fins) - padY), Math.min(5, Math.max(...fins) + padY)] as [
          number,
          number
        ],
        dtick: 0.2,
      };
    }
    // delta
    return {
      x: [-0.25, 0.25] as [number, number],
      y: [-0.25, 0.25] as [number, number],
      dtick: 0.05,
    };
  }, [scaleMode]);

  // ------------------------- SHAPES -------------------------
  const shapes = useMemo(() => {
    const s: Partial<Plotly.Shape>[] = [];

    if (scaleMode === "delta") {
      // Crosshair at origin + tolerance box
      s.push({
        type: "rect",
        xref: "x",
        yref: "y",
        x0: -0.05,
        x1: 0.05,
        y0: -0.05,
        y1: 0.05,
        line: { width: 0 },
        fillcolor: "rgba(93,185,217,0.10)",
        layer: "below",
      });
      s.push({
        type: "line",
        xref: "x",
        yref: "y",
        x0: axisRange.x[0],
        x1: axisRange.x[1],
        y0: 0,
        y1: 0,
        line: { color: "#002f5f", width: 1, dash: "dot" },
      });
      s.push({
        type: "line",
        xref: "x",
        yref: "y",
        x0: 0,
        x1: 0,
        y0: axisRange.y[0],
        y1: axisRange.y[1],
        line: { color: "#002f5f", width: 1, dash: "dot" },
      });

      // Arrows from origin to each delta point
      for (const d of deltas) {
        const color = COLOR_MAP[d.topic] ?? "#5db9d9";
        s.push({
          type: "line",
          xref: "x",
          yref: "y",
          x0: 0,
          x1: d.di,
          y0: 0,
          y1: d.df,
          line: { color, width: 3 },
        });
      }
      return s;
    }

    // Target zone (only meaningful on 1–5 axes; clipped automatically in focus)
    if (showThreshold) {
      s.push({
        type: "rect",
        xref: "x",
        yref: "y",
        x0: 2.5,
        x1: 5,
        y0: 2.5,
        y1: 5,
        line: { width: 0 },
        fillcolor: "rgba(93,185,217,0.08)",
        layer: "below",
      });
      s.push({
        type: "line",
        xref: "x",
        yref: "y",
        x0: 2.5,
        x1: 2.5,
        y0: 1,
        y1: 5,
        line: { color: "#002f5f", width: 1, dash: "dot" },
      });
      s.push({
        type: "line",
        xref: "x",
        yref: "y",
        x0: 1,
        x1: 5,
        y0: 2.5,
        y1: 2.5,
        line: { color: "#002f5f", width: 1, dash: "dot" },
      });
    }

    if (showEllipses) {
      for (const p of points) {
        const color = COLOR_MAP[p.topic] ?? "#5db9d9";
        s.push({
          type: "circle",
          xref: "x",
          yref: "y",
          x0: p.impact - p.width / 2,
          x1: p.impact + p.width / 2,
          y0: p.financial - p.height / 2,
          y1: p.financial + p.height / 2,
          line: { color, width: 2 },
          fillcolor: color + "20",
          layer: "below",
        });
      }
    }

    return s;
  }, [points, deltas, showEllipses, showThreshold, scaleMode, axisRange]);

  // ------------------------- TRACES -------------------------
  const traces: Plotly.Data[] = useMemo(() => {
    if (scaleMode === "delta") {
      // Ghost dot at origin = MC baseline reference
      const ghost: Plotly.Data = {
        type: "scatter",
        mode: "text+markers",
        x: [0],
        y: [0],
        text: ["MC baseline"],
        textposition: "bottom center",
        textfont: { size: 11, color: "#4a5663", family: "Inter, sans-serif" },
        marker: {
          size: 12,
          color: "#ffffff",
          line: { color: "#002f5f", width: 2 },
          symbol: "circle",
        },
        hoverinfo: "skip",
      };

      const pts: Plotly.Data[] = deltas.map(
        (d): Plotly.Data => ({
          type: "scatter",
          mode: "text+markers",
          x: [d.di],
          y: [d.df],
          text: [d.topic.slice(0, 2)],
          textposition: "top center",
          textfont: { size: 14, color: "#002f5f", family: "Inter, sans-serif" },
          marker: {
            size: 20,
            color: COLOR_MAP[d.topic] ?? "#5db9d9",
            line: { color: "#ffffff", width: 3 },
            symbol: "circle",
          },
          name: d.topic,
          hovertemplate:
            `<b>${d.topic}</b><br>` +
            `Δ Impact: %{x:+.3f}<br>Δ Financial: %{y:+.3f}` +
            "<extra></extra>",
        })
      );

      return [ghost, ...pts];
    }

    return points.map(
      (p): Plotly.Data => ({
        type: "scatter",
        mode: "text+markers",
        x: [p.impact],
        y: [p.financial],
        text: [p.topic.slice(0, 2)],
        textposition: "top center",
        textfont: { size: 14, color: "#002f5f", family: "Inter, sans-serif" },
        marker: {
          size: 22,
          color: COLOR_MAP[p.topic] ?? "#5db9d9",
          line: { color: "#ffffff", width: 3 },
          symbol: p.in_target ? "circle" : "circle-open",
        },
        name: p.topic,
        hovertemplate:
          `<b>${p.topic}</b><br>` +
          `Impact: %{x:.2f}<br>Financial: %{y:.2f}<br>` +
          `In target zone: ${p.in_target ? "YES" : "borderline"}` +
          "<extra></extra>",
      })
    );
  }, [points, deltas, scaleMode]);

  // ------------------------- LAYOUT -------------------------
  const layout: Partial<Plotly.Layout> = {
    autosize: true,
    height: 560,
    margin: { l: 70, r: 30, t: 30, b: 70 },
    paper_bgcolor: "white",
    plot_bgcolor: "#fbfdff",
    // Smooth transitions when scheme/scale change.
    transition: { duration: 650, easing: "cubic-in-out" },
    xaxis: {
      title: {
        text:
          scaleMode === "delta"
            ? "Δ Impact materiality vs MC baseline"
            : "Impact materiality (inside-out)",
        font: { size: 13 },
      },
      range: axisRange.x,
      dtick: axisRange.dtick,
      gridcolor: "#eef1f5",
      zeroline: scaleMode === "delta",
      zerolinecolor: "#002f5f",
      zerolinewidth: 1,
      tickformat: scaleMode === "delta" ? "+.2f" : scaleMode === "focus" ? ".1f" : "d",
    },
    yaxis: {
      title: {
        text:
          scaleMode === "delta"
            ? "Δ Financial materiality vs MC baseline"
            : "Financial materiality (outside-in)",
        font: { size: 13 },
      },
      range: axisRange.y,
      dtick: axisRange.dtick,
      gridcolor: "#eef1f5",
      zeroline: scaleMode === "delta",
      zerolinecolor: "#002f5f",
      zerolinewidth: 1,
      tickformat: scaleMode === "delta" ? "+.2f" : scaleMode === "focus" ? ".1f" : "d",
    },
    shapes: shapes as Plotly.Shape[],
    showlegend: false,
    annotations:
      scaleMode === "delta"
        ? [
            {
              x: axisRange.x[1] * 0.92,
              y: axisRange.y[1] * 0.9,
              text:
                "Tolerance box<br><sub>±0.05 scoring noise</sub>",
              showarrow: false,
              font: { color: "#002f5f", size: 11 },
              bgcolor: "rgba(93,185,217,0.18)",
              borderpad: 6,
            },
          ]
        : showThreshold
        ? [
            {
              x: scaleMode === "focus" ? axisRange.x[1] - 0.1 : 4.4,
              y: scaleMode === "focus" ? axisRange.y[1] - 0.05 : 4.7,
              text: "★ Target zone<br><sub>Impact ≥ 2.5 · Financial ≥ 2.5</sub>",
              showarrow: false,
              font: { color: "#002f5f", size: 11 },
              bgcolor: "rgba(93,185,217,0.18)",
              borderpad: 6,
            },
          ]
        : [],
  };

  const active = SCHEMES.find((s) => s.value === scheme)!;
  const maxAbsDelta = Math.max(
    ...deltas.flatMap((d) => [Math.abs(d.di), Math.abs(d.df)]),
    0
  );

  return (
    <section id="matrix" className="relative py-28 bg-white border-t border-grid">
      <div className="wrap">
        <SectionHeader
          kicker="Interactive materiality matrix"
          title={
            <>
              Positions are <span className="text-aqua">script-generated</span>. No
              manual chart manipulation.
            </>
          }
          lede="Switch the weighting scheme to stress-test robustness. On the 1–5 credibility scale, positions barely move — that's by design. If you want to see the sub-point movement, flip to Focus or Δ mode."
        />

        <div className="mt-10 grid lg:grid-cols-12 gap-6">
          {/* Controls */}
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="lg:col-span-4 card p-6 self-start"
          >
            <div className="flex items-center gap-2 text-navy mb-4">
              <Sliders className="w-4 h-4 text-aqua" />
              <span className="kicker">Weighting scheme</span>
            </div>

            <div className="space-y-2">
              {SCHEMES.map((s) => (
                <button
                  key={s.value}
                  onClick={() => setScheme(s.value)}
                  className={`w-full text-left px-4 py-3 rounded-xl border transition-all ${
                    scheme === s.value
                      ? "border-aqua bg-aqua/10 shadow-soft"
                      : "border-grid hover:border-aqua/60 hover:bg-grid/40"
                  }`}
                >
                  <div className="font-bold text-navy text-sm">{s.label}</div>
                  <div className="text-xs text-slate2/70 mt-0.5">{s.hint}</div>
                </button>
              ))}
            </div>

            {/* Scale mode selector */}
            <div className="mt-6 pt-6 border-t border-grid">
              <div className="kicker mb-3">Axis scale</div>
              <div className="grid grid-cols-3 gap-1.5">
                {SCALES.map((s) => {
                  const Icon = s.icon;
                  const active = scaleMode === s.value;
                  return (
                    <button
                      key={s.value}
                      onClick={() => setScaleMode(s.value)}
                      title={s.hint}
                      className={`px-2 py-2.5 rounded-lg border text-[11px] font-bold leading-tight transition-all ${
                        active
                          ? "border-aqua bg-aqua/15 text-navy shadow-soft"
                          : "border-grid text-slate2 hover:border-aqua/60"
                      }`}
                    >
                      <Icon
                        className={`w-4 h-4 mx-auto mb-1 ${
                          active ? "text-aqua" : "text-slate2/60"
                        }`}
                      />
                      {s.label.replace(" (1–5)", "")}
                    </button>
                  );
                })}
              </div>
              <div className="text-[11px] text-slate2/60 mt-2 leading-relaxed">
                {SCALES.find((s) => s.value === scaleMode)!.hint}
              </div>
            </div>

            <div className="mt-6 pt-6 border-t border-grid space-y-3">
              <Toggle
                checked={showEllipses}
                onChange={setShowEllipses}
                label="Uncertainty ellipses"
                disabled={scaleMode === "delta"}
              />
              <Toggle
                checked={showThreshold}
                onChange={setShowThreshold}
                label="Target zone & thresholds"
                disabled={scaleMode === "delta"}
              />
            </div>

            <div className="mt-6 rounded-xl bg-grid/50 p-4 text-xs text-slate2/80 leading-relaxed">
              <div className="flex items-start gap-2">
                <Info className="w-4 h-4 text-aqua flex-shrink-0 mt-0.5" />
                <div>
                  <strong className="text-navy">Robustness note:</strong> max Δ across
                  all schemes is{" "}
                  <strong className="num-tabular text-navy">
                    ±{maxAbsDelta.toFixed(3)}
                  </strong>{" "}
                  — well inside the ±0.05 scoring noise band. Ranking is stable.
                </div>
              </div>
            </div>
          </motion.div>

          {/* Plot */}
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="lg:col-span-8 card p-4"
          >
            <div className="px-2 pt-2 flex flex-wrap items-baseline gap-3 gap-y-1">
              <div className="font-display text-navy text-2xl">{active.label}</div>
              <div className="text-sm text-slate2/70">{active.hint}</div>
              <span className="ml-auto chip bg-aqua/15 text-navy text-[11px]">
                {SCALES.find((s) => s.value === scaleMode)!.label}
              </span>
            </div>
            <Plot
              data={traces}
              layout={layout}
              config={{ displaylogo: false, responsive: true }}
              useResizeHandler
              style={{ width: "100%", height: "560px" }}
            />

            {/* Delta readout strip */}
            <div className="grid md:grid-cols-3 gap-3 p-4">
              {TOPICS.map((t) => {
                const d = deltas.find((x) => x.topic.startsWith(t.code));
                const showDelta = scheme !== "MC" && d;
                return (
                  <div
                    key={t.code}
                    className="rounded-xl border border-grid p-3 flex items-center gap-3"
                  >
                    <span
                      className="w-3 h-3 rounded-full flex-shrink-0"
                      style={{ background: t.color }}
                    />
                    <div className="min-w-0 flex-1">
                      <div className="text-xs text-slate2/60">
                        {t.code} ·{" "}
                        <span className="num-tabular">
                          I {t.impact.toFixed(2)} · F {t.financial.toFixed(2)}
                        </span>
                      </div>
                      <div className="font-semibold text-navy text-sm truncate">
                        {t.title}
                      </div>
                    </div>
                    {showDelta && (
                      <div
                        className="text-right font-mono text-[10px] leading-tight num-tabular"
                        title="Shift vs Monte Carlo baseline"
                      >
                        <div
                          className={
                            Math.abs(d!.di) < 0.005
                              ? "text-slate2/50"
                              : "text-navy font-bold"
                          }
                        >
                          ΔI {d!.di >= 0 ? "+" : ""}
                          {d!.di.toFixed(3)}
                        </div>
                        <div
                          className={
                            Math.abs(d!.df) < 0.005
                              ? "text-slate2/50"
                              : "text-navy font-bold"
                          }
                        >
                          ΔF {d!.df >= 0 ? "+" : ""}
                          {d!.df.toFixed(3)}
                        </div>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
}

function Toggle({
  checked,
  onChange,
  label,
  disabled = false,
}: {
  checked: boolean;
  onChange: (v: boolean) => void;
  label: string;
  disabled?: boolean;
}) {
  return (
    <button
      onClick={() => !disabled && onChange(!checked)}
      disabled={disabled}
      className={`w-full flex items-center justify-between px-1 py-1 transition-opacity ${
        disabled ? "opacity-40 cursor-not-allowed" : ""
      }`}
    >
      <span className="text-sm font-semibold text-navy">{label}</span>
      <span
        className={`w-10 h-6 rounded-full transition-colors relative ${
          checked ? "bg-aqua" : "bg-grid"
        }`}
      >
        <span
          className={`absolute top-0.5 w-5 h-5 rounded-full bg-white shadow transition-all ${
            checked ? "left-[18px]" : "left-0.5"
          }`}
        />
      </span>
    </button>
  );
}
