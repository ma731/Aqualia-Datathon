import { useMemo, useState } from "react";
import { motion } from "framer-motion";
import {
  ResponsiveContainer,
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ZAxis,
  Cell,
  ReferenceLine,
} from "recharts";
import { PEERS } from "../content/topics";
import SectionHeader from "./SectionHeader";
import { Maximize2, Minimize2, Move3D } from "lucide-react";

const COLORS = ["#5db9d9", "#1f77b4", "#c83c35", "#2ca02c", "#f2b039", "#8e44ad"];

type ScaleMode = "full" | "focus" | "delta";

const SCALES: {
  value: ScaleMode;
  label: string;
  hint: string;
  icon: React.ComponentType<{ className?: string }>;
}[] = [
  {
    value: "full",
    label: "Full scale",
    hint: "1–5 axes — context against the whole materiality space",
    icon: Maximize2,
  },
  {
    value: "focus",
    label: "Focus",
    hint: "Auto-zoom to the peer cluster",
    icon: Minimize2,
  },
  {
    value: "delta",
    label: "Δ vs 2027 plan",
    hint: "Vectors from Aqualia's 2027 target",
    icon: Move3D,
  },
];

export default function Peers() {
  const [scaleMode, setScaleMode] = useState<ScaleMode>("focus");

  const planIdx = PEERS.findIndex((p) => p.name.includes("plan"));
  const plan = PEERS[planIdx];

  const data = useMemo(() => {
    if (scaleMode === "delta") {
      return PEERS.map((p) => ({
        ...p,
        x: p.impact - plan.impact,
        y: p.financial - plan.financial,
      }));
    }
    return PEERS.map((p) => ({ ...p, x: p.impact, y: p.financial }));
  }, [scaleMode, plan]);

  const axisProps = useMemo(() => {
    if (scaleMode === "full") {
      return {
        xDomain: [1, 5] as [number, number],
        yDomain: [1, 5] as [number, number],
        xLabel: "Impact materiality",
        yLabel: "Financial materiality",
        xTick: (v: number) => v.toFixed(0),
        yTick: (v: number) => v.toFixed(0),
      };
    }
    if (scaleMode === "focus") {
      return {
        xDomain: [3.2, 4.3] as [number, number],
        yDomain: [2.4, 3.4] as [number, number],
        xLabel: "Impact materiality",
        yLabel: "Financial materiality",
        xTick: (v: number) => v.toFixed(1),
        yTick: (v: number) => v.toFixed(1),
      };
    }
    return {
      xDomain: [-0.6, 0.4] as [number, number],
      yDomain: [-0.5, 0.4] as [number, number],
      xLabel: "Δ Impact vs Aqualia 2027 plan",
      yLabel: "Δ Financial vs Aqualia 2027 plan",
      xTick: (v: number) => (v >= 0 ? `+${v.toFixed(2)}` : v.toFixed(2)),
      yTick: (v: number) => (v >= 0 ? `+${v.toFixed(2)}` : v.toFixed(2)),
    };
  }, [scaleMode]);

  // reference lines: in delta mode, axes at 0; elsewhere, the Aqualia 2027 plan
  const refX = scaleMode === "delta" ? 0 : plan.impact;
  const refY = scaleMode === "delta" ? 0 : plan.financial;

  return (
    <section id="peers" className="relative py-28 bg-[#f4f8fb] border-t border-grid">
      <div className="wrap">
        <SectionHeader
          kicker="Peer benchmark"
          title={
            <>
              Where we sit today{" "}
              <span className="text-aqua">vs. where the plan takes us.</span>
            </>
          }
          lede="DMA maturity (bubble size) against the impact × financial signal. Switch the scale to see the cluster up close, or the exact Δ to Aqualia's 2027 target."
        />

        <div className="mt-10 grid lg:grid-cols-12 gap-6">
          {/* Scale switcher */}
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="lg:col-span-3 card p-5 self-start"
          >
            <div className="kicker mb-3">Axis scale</div>
            <div className="flex flex-col gap-2">
              {SCALES.map((s) => {
                const Icon = s.icon;
                const active = scaleMode === s.value;
                return (
                  <button
                    key={s.value}
                    onClick={() => setScaleMode(s.value)}
                    className={`text-left px-3 py-2.5 rounded-lg border text-xs font-bold transition-all flex items-center gap-2 ${
                      active
                        ? "border-aqua bg-aqua/15 text-navy shadow-soft"
                        : "border-grid text-slate2 hover:border-aqua/60"
                    }`}
                  >
                    <Icon
                      className={`w-4 h-4 ${active ? "text-aqua" : "text-slate2/60"}`}
                    />
                    <span className="flex-1">{s.label}</span>
                  </button>
                );
              })}
            </div>
            <div className="text-[11px] text-slate2/60 mt-3 leading-relaxed">
              {SCALES.find((s) => s.value === scaleMode)!.hint}
            </div>

            <div className="mt-5 pt-5 border-t border-grid text-[11px] text-slate2/70 leading-relaxed">
              <strong className="text-navy">Reading the delta view:</strong> origin is
              Aqualia's 2027 target. Peers to the upper-right are ahead of our plan on
              both axes; the 2027 plan sits at (0,0).
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="lg:col-span-9 card p-6"
          >
            <div className="flex items-center gap-2 mb-2">
              <span className="chip bg-aqua/15 text-navy text-[11px]">
                {SCALES.find((s) => s.value === scaleMode)!.label}
              </span>
              <span className="text-xs text-slate2/70">
                Bubble size = DMA maturity index
              </span>
            </div>

            <ResponsiveContainer width="100%" height={460}>
              <ScatterChart margin={{ top: 20, right: 30, left: 10, bottom: 20 }}>
                <CartesianGrid stroke="#eef1f5" />
                <XAxis
                  type="number"
                  dataKey="x"
                  name={axisProps.xLabel}
                  domain={axisProps.xDomain}
                  tick={{ fontSize: 12, fill: "#4a5663" }}
                  tickFormatter={axisProps.xTick}
                  label={{
                    value: axisProps.xLabel,
                    position: "insideBottom",
                    offset: -8,
                    fill: "#002f5f",
                    fontSize: 13,
                    fontWeight: 600,
                  }}
                />
                <YAxis
                  type="number"
                  dataKey="y"
                  name={axisProps.yLabel}
                  domain={axisProps.yDomain}
                  tick={{ fontSize: 12, fill: "#4a5663" }}
                  tickFormatter={axisProps.yTick}
                  label={{
                    value: axisProps.yLabel,
                    angle: -90,
                    position: "insideLeft",
                    fill: "#002f5f",
                    fontSize: 13,
                    fontWeight: 600,
                  }}
                />
                <ZAxis dataKey="dma" range={[150, 900]} />
                {scaleMode !== "delta" && (
                  <>
                    <ReferenceLine
                      x={refX}
                      stroke="#5db9d9"
                      strokeDasharray="4 4"
                      label={{
                        value: "Aqualia 2027",
                        position: "top",
                        fill: "#002f5f",
                        fontSize: 11,
                      }}
                    />
                    <ReferenceLine
                      y={refY}
                      stroke="#5db9d9"
                      strokeDasharray="4 4"
                    />
                  </>
                )}
                {scaleMode === "delta" && (
                  <>
                    <ReferenceLine x={0} stroke="#002f5f" strokeDasharray="3 3" />
                    <ReferenceLine y={0} stroke="#002f5f" strokeDasharray="3 3" />
                  </>
                )}
                <Tooltip
                  cursor={{ strokeDasharray: "3 3" }}
                  content={({ active, payload }) => {
                    if (!active || !payload?.length) return null;
                    const p = payload[0].payload;
                    const isDelta = scaleMode === "delta";
                    return (
                      <div className="bg-white border border-grid rounded-xl px-3 py-2 text-xs shadow-soft">
                        <div className="font-bold text-navy">{p.name}</div>
                        <div className="text-slate2/70">{p.label}</div>
                        <div className="mt-1 num-tabular">
                          {isDelta ? (
                            <>
                              ΔImpact {p.x >= 0 ? "+" : ""}
                              {p.x.toFixed(2)} · ΔFinancial {p.y >= 0 ? "+" : ""}
                              {p.y.toFixed(2)}
                            </>
                          ) : (
                            <>
                              Impact {p.impact.toFixed(2)} · Financial{" "}
                              {p.financial.toFixed(2)}
                            </>
                          )}
                        </div>
                        <div className="num-tabular">
                          DMA maturity {(p.dma * 100).toFixed(0)}%
                        </div>
                      </div>
                    );
                  }}
                />
                <Scatter data={data} isAnimationActive animationDuration={700}>
                  {data.map((p, i) => (
                    <Cell
                      key={p.name}
                      fill={p.name.includes("plan") ? "#5db9d9" : COLORS[i % COLORS.length]}
                      stroke={p.name.includes("plan") ? "#002f5f" : "#ffffff"}
                      strokeWidth={p.name.includes("plan") ? 3 : 2}
                    />
                  ))}
                </Scatter>
              </ScatterChart>
            </ResponsiveContainer>

            <div className="flex flex-wrap gap-2 mt-4 px-2">
              {PEERS.map((p, i) => (
                <span
                  key={p.name}
                  className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full text-xs border border-grid bg-white"
                >
                  <span
                    className="w-2.5 h-2.5 rounded-full"
                    style={{
                      background: p.name.includes("plan")
                        ? "#5db9d9"
                        : COLORS[i % COLORS.length],
                    }}
                  />
                  <span className="font-bold text-navy">{p.name}</span>
                  <span className="text-slate2/60">· {p.label}</span>
                </span>
              ))}
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
}
