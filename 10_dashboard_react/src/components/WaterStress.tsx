import { useMemo, useState } from "react";
import { motion } from "framer-motion";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Cell,
  ReferenceLine,
} from "recharts";
import { DATA } from "../data";
import SectionHeader from "./SectionHeader";
import { Droplets, Flame, TrendingUp, BarChart2, Coins } from "lucide-react";

type ViewMode = "scores" | "delta" | "weighted";

const VIEWS: {
  value: ViewMode;
  label: string;
  hint: string;
  icon: React.ComponentType<{ className?: string }>;
}[] = [
  {
    value: "scores",
    label: "BWS scores",
    hint: "2024 baseline vs 2030 BAU — the physical signal",
    icon: BarChart2,
  },
  {
    value: "delta",
    label: "Δ 2024 → 2030",
    hint: "Stress *added* by the BAU scenario — the transition risk",
    icon: TrendingUp,
  },
  {
    value: "weighted",
    label: "Revenue-weighted",
    hint: "BWS × revenue share — true P&L exposure by region",
    icon: Coins,
  },
];

const SEV_COLOR = (score: number) => {
  if (score >= 4.2) return "#7c1d1d";
  if (score >= 3.5) return "#c83c35";
  if (score >= 2.5) return "#f2b039";
  if (score >= 1.5) return "#eadc6b";
  return "#1b7f3b";
};

export default function WaterStress() {
  const [view, setView] = useState<ViewMode>("scores");

  const rows = useMemo(
    () => DATA.aqueduct.slice().sort((a, b) => b.bws_score_2030_BAU - a.bws_score_2030_BAU),
    []
  );

  type ChartRow = {
    region: string;
    country: string;
    bws2024: number;
    bws2030: number;
    revenue: number;
    delta: number;
    exposure2024: number;
    exposure2030: number;
  };

  const sortedChartData = useMemo<ChartRow[]>(() => {
    const mapped: ChartRow[] = rows.map((r) => ({
      region: r.region_label,
      country: r.country,
      bws2024: r.bws_score_2024,
      bws2030: r.bws_score_2030_BAU,
      revenue: r.revenue_share_pct,
      delta: +(r.bws_score_2030_BAU - r.bws_score_2024).toFixed(2),
      exposure2024: +(r.bws_score_2024 * (r.revenue_share_pct / 100) * 100).toFixed(2),
      exposure2030: +(r.bws_score_2030_BAU * (r.revenue_share_pct / 100) * 100).toFixed(2),
    }));
    if (view === "delta") return mapped.sort((a, b) => b.delta - a.delta);
    if (view === "weighted")
      return mapped.sort((a, b) => b.exposure2030 - a.exposure2030);
    return mapped;
  }, [rows, view]);

  const topStress = rows[0];

  return (
    <section id="water" className="relative py-28 bg-white border-t border-grid">
      <div className="wrap">
        <SectionHeader
          kicker="Physical climate & Aqueduct"
          title={
            <>
              Where the water leaves first:{" "}
              <span className="text-aqua">Segura, Algarve, Andalucía.</span>
            </>
          }
          lede="WRI Aqueduct 2024 baseline vs 2030 BAU, mapped against Aqualia's revenue share. Flip to Δ to isolate the stress *added* by the scenario, or to the revenue-weighted view to see true P&L exposure."
        />

        {/* View switcher */}
        <div className="mt-10 grid sm:grid-cols-3 gap-3 max-w-3xl">
          {VIEWS.map((v) => {
            const Icon = v.icon;
            const active = view === v.value;
            return (
              <button
                key={v.value}
                onClick={() => setView(v.value)}
                className={`text-left p-4 rounded-xl border transition-all ${
                  active
                    ? "border-aqua bg-aqua/10 shadow-soft"
                    : "border-grid bg-white hover:border-aqua/60"
                }`}
              >
                <div className="flex items-center gap-2 mb-1">
                  <Icon
                    className={`w-4 h-4 ${active ? "text-aqua" : "text-slate2/60"}`}
                  />
                  <span className="font-bold text-navy text-sm">{v.label}</span>
                </div>
                <div className="text-[11px] text-slate2/65 leading-snug">{v.hint}</div>
              </button>
            );
          })}
        </div>

        <div className="grid lg:grid-cols-12 gap-6 mt-8">
          <motion.div
            key={view}
            initial={{ opacity: 0, x: -12 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.45 }}
            className="lg:col-span-8 card p-6"
          >
            <div className="flex items-baseline justify-between mb-4 flex-wrap gap-2">
              <div className="kicker text-aqua">
                {view === "scores" && "Baseline water stress · BWS score (0–5)"}
                {view === "delta" && "Stress added by 2030 BAU · Δ BWS"}
                {view === "weighted" && "Revenue-weighted exposure · BWS × rev%"}
              </div>
              <div className="text-xs text-slate2/60">
                Source: WRI Aqueduct 4.0 · 2024 vs 2030 BAU
              </div>
            </div>
            <ResponsiveContainer width="100%" height={460}>
              <BarChart
                data={sortedChartData}
                layout="vertical"
                margin={{ top: 10, right: 50, left: 20, bottom: 10 }}
              >
                <CartesianGrid stroke="#eef1f5" horizontal={false} />
                <XAxis
                  type="number"
                  domain={view === "delta" ? [0, 1.2] : view === "weighted" ? [0, "auto"] : [0, 5]}
                  tick={{ fontSize: 12, fill: "#4a5663" }}
                  tickFormatter={(v: number) => v.toFixed(view === "scores" ? 1 : 2)}
                />
                <YAxis
                  dataKey="region"
                  type="category"
                  width={230}
                  tick={{ fontSize: 12, fill: "#002f5f", fontWeight: 600 }}
                  axisLine={false}
                  tickLine={false}
                />

                {view === "scores" && (
                  <>
                    <Tooltip
                      contentStyle={tooltipStyle}
                      formatter={(val: number, key: string) => {
                        if (key === "bws2024") return [val.toFixed(1), "2024 BWS"];
                        if (key === "bws2030") return [val.toFixed(1), "2030 BWS (BAU)"];
                        return [val, key];
                      }}
                    />
                    <ReferenceLine
                      x={3.5}
                      stroke="#c83c35"
                      strokeDasharray="3 3"
                      label={{
                        value: "High",
                        position: "top",
                        fill: "#c83c35",
                        fontSize: 10,
                      }}
                    />
                    <ReferenceLine
                      x={4.2}
                      stroke="#7c1d1d"
                      strokeDasharray="3 3"
                      label={{
                        value: "Extreme",
                        position: "top",
                        fill: "#7c1d1d",
                        fontSize: 10,
                      }}
                    />
                    <Bar
                      dataKey="bws2024"
                      radius={[0, 6, 6, 0]}
                      barSize={14}
                      fill="#b8d3e0"
                      isAnimationActive
                      animationDuration={650}
                    />
                    <Bar
                      dataKey="bws2030"
                      radius={[0, 6, 6, 0]}
                      barSize={14}
                      isAnimationActive
                      animationDuration={650}
                    >
                      {sortedChartData.map((d, i) => (
                        <Cell key={i} fill={SEV_COLOR(d.bws2030)} />
                      ))}
                    </Bar>
                  </>
                )}

                {view === "delta" && (
                  <>
                    <Tooltip
                      contentStyle={tooltipStyle}
                      content={({ active, payload }) => {
                        if (!active || !payload?.length) return null;
                        const p = payload[0].payload as {
                          region: string;
                          country: string;
                          delta: number;
                          bws2024: number;
                          bws2030: number;
                        };
                        return (
                          <div
                            className="bg-white border border-grid rounded-xl px-3 py-2 text-xs shadow-soft"
                            style={{ minWidth: 200 }}
                          >
                            <div className="font-bold text-navy">{p.region}</div>
                            <div className="text-slate2/70">{p.country}</div>
                            <div className="mt-1 num-tabular">
                              Δ BWS{" "}
                              <strong className="text-navy">+{p.delta.toFixed(2)}</strong>{" "}
                              ({p.bws2024.toFixed(1)} → {p.bws2030.toFixed(1)})
                            </div>
                          </div>
                        );
                      }}
                    />
                    <Bar
                      dataKey="delta"
                      radius={[0, 6, 6, 0]}
                      barSize={18}
                      isAnimationActive
                      animationDuration={650}
                    >
                      {sortedChartData.map((d, i) => {
                        const delta = d.delta;
                        const col =
                          delta >= 0.8
                            ? "#7c1d1d"
                            : delta >= 0.5
                            ? "#c83c35"
                            : delta >= 0.3
                            ? "#f2b039"
                            : "#eadc6b";
                        return <Cell key={i} fill={col} />;
                      })}
                    </Bar>
                  </>
                )}

                {view === "weighted" && (
                  <>
                    <Tooltip
                      contentStyle={tooltipStyle}
                      content={({ active, payload }) => {
                        if (!active || !payload?.length) return null;
                        const p = payload[0].payload as {
                          region: string;
                          country: string;
                          exposure2024: number;
                          exposure2030: number;
                          bws2024: number;
                          bws2030: number;
                          revenue: number;
                        };
                        return (
                          <div
                            className="bg-white border border-grid rounded-xl px-3 py-2 text-xs shadow-soft"
                            style={{ minWidth: 220 }}
                          >
                            <div className="font-bold text-navy">{p.region}</div>
                            <div className="text-slate2/70">{p.country}</div>
                            <div className="mt-1 num-tabular">
                              Revenue share <strong>{p.revenue}%</strong>
                            </div>
                            <div className="num-tabular">
                              2024 exposure {p.exposure2024.toFixed(1)} ·
                              2030 exposure{" "}
                              <strong className="text-navy">
                                {p.exposure2030.toFixed(1)}
                              </strong>
                            </div>
                            <div className="text-[10px] text-slate2/60 mt-1 italic">
                              (BWS × revenue share, ×100 for legibility)
                            </div>
                          </div>
                        );
                      }}
                    />
                    <Bar
                      dataKey="exposure2024"
                      radius={[0, 6, 6, 0]}
                      barSize={14}
                      fill="#b8d3e0"
                      isAnimationActive
                      animationDuration={650}
                    />
                    <Bar
                      dataKey="exposure2030"
                      radius={[0, 6, 6, 0]}
                      barSize={14}
                      isAnimationActive
                      animationDuration={650}
                    >
                      {sortedChartData.map((d, i) => (
                        <Cell key={i} fill={SEV_COLOR(d.bws2030)} />
                      ))}
                    </Bar>
                  </>
                )}
              </BarChart>
            </ResponsiveContainer>
            <LegendRow view={view} />
          </motion.div>

          {/* Right column — context cards */}
          <div className="lg:col-span-4 space-y-4">
            <motion.div
              initial={{ opacity: 0, y: 12 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="card p-6"
            >
              <div className="flex items-center gap-2 mb-2">
                <Flame className="w-4 h-4 text-badred" />
                <span className="kicker text-badred">Highest exposure</span>
              </div>
              <div className="font-display text-navy text-2xl leading-tight">
                {topStress.region_label}
              </div>
              <div className="text-sm text-slate2/70 mt-1">{topStress.country}</div>

              <div className="grid grid-cols-2 gap-3 mt-5">
                <div className="rounded-xl bg-grid/50 px-3 py-3">
                  <div className="text-[11px] uppercase tracking-wider text-slate2/60">
                    2024 BWS
                  </div>
                  <div className="num-tabular text-2xl font-bold text-navy">
                    {topStress.bws_score_2024.toFixed(1)}
                  </div>
                  <div className="text-[11px] text-slate2/60">
                    {topStress.bws_category_2024}
                  </div>
                </div>
                <div
                  className="rounded-xl px-3 py-3 text-white"
                  style={{ background: SEV_COLOR(topStress.bws_score_2030_BAU) }}
                >
                  <div className="text-[11px] uppercase tracking-wider opacity-80">
                    2030 BAU
                  </div>
                  <div className="num-tabular text-2xl font-bold">
                    {topStress.bws_score_2030_BAU.toFixed(1)}
                  </div>
                  <div className="text-[11px] opacity-90">
                    {topStress.bws_category_2030_BAU}
                  </div>
                </div>
              </div>

              <div className="mt-4 text-sm text-slate2 italic">
                “{topStress.concession_note}”
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 12 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.1 }}
              className="card p-6"
            >
              <div className="flex items-center gap-2 mb-3">
                <Droplets className="w-4 h-4 text-aqua" />
                <span className="kicker text-aqua">Revenue-weighted risk</span>
              </div>
              <div className="space-y-2">
                {rows.slice(0, 6).map((r) => (
                  <div
                    key={r.region_label}
                    className="flex items-center gap-2 text-sm"
                  >
                    <span
                      className="w-2.5 h-2.5 rounded-full flex-shrink-0"
                      style={{ background: SEV_COLOR(r.bws_score_2030_BAU) }}
                    />
                    <span className="flex-1 text-navy truncate">
                      {r.region_label}
                    </span>
                    <span className="num-tabular font-bold text-navy">
                      {r.revenue_share_pct}%
                    </span>
                  </div>
                ))}
              </div>
              <div className="mt-3 text-xs text-slate2/60">
                % of group revenue · 2024 baseline
              </div>
            </motion.div>
          </div>
        </div>
      </div>
    </section>
  );
}

const tooltipStyle: React.CSSProperties = {
  background: "white",
  border: "1px solid #e6e8eb",
  borderRadius: 12,
  fontSize: 12,
};

function LegendRow({ view }: { view: ViewMode }) {
  if (view === "scores") {
    return (
      <div className="flex flex-wrap items-center gap-4 text-xs text-slate2/70 mt-2 px-2">
        <span className="inline-flex items-center gap-1.5">
          <span className="w-3 h-3 rounded bg-[#b8d3e0]" /> 2024 BWS
        </span>
        <span className="inline-flex items-center gap-1.5">
          <span className="w-3 h-3 rounded bg-[#c83c35]" /> 2030 BWS (severity colored)
        </span>
      </div>
    );
  }
  if (view === "delta") {
    return (
      <div className="flex flex-wrap items-center gap-3 text-xs text-slate2/70 mt-2 px-2">
        <span>Δ severity:</span>
        <span className="inline-flex items-center gap-1.5">
          <span className="w-3 h-3 rounded bg-[#eadc6b]" /> &lt;0.3
        </span>
        <span className="inline-flex items-center gap-1.5">
          <span className="w-3 h-3 rounded bg-[#f2b039]" /> 0.3–0.5
        </span>
        <span className="inline-flex items-center gap-1.5">
          <span className="w-3 h-3 rounded bg-[#c83c35]" /> 0.5–0.8
        </span>
        <span className="inline-flex items-center gap-1.5">
          <span className="w-3 h-3 rounded bg-[#7c1d1d]" /> ≥0.8
        </span>
      </div>
    );
  }
  return (
    <div className="flex flex-wrap items-center gap-4 text-xs text-slate2/70 mt-2 px-2">
      <span className="inline-flex items-center gap-1.5">
        <span className="w-3 h-3 rounded bg-[#b8d3e0]" /> 2024 exposure (BWS × rev%)
      </span>
      <span className="inline-flex items-center gap-1.5">
        <span className="w-3 h-3 rounded bg-[#c83c35]" /> 2030 exposure (severity colored)
      </span>
    </div>
  );
}
