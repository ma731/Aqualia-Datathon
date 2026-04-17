import { motion } from "framer-motion";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  LabelList,
  Cell,
} from "recharts";
import { CAPITAL_PIPELINE } from "../content/topics";
import SectionHeader from "./SectionHeader";
import { Banknote, Gauge, PiggyBank, TrendingDown } from "lucide-react";

export default function Capital() {
  const total = CAPITAL_PIPELINE.reduce((a, b) => a + b.eur, 0);

  return (
    <section id="capital" className="relative py-28 bg-white border-t border-grid">
      <div className="wrap">
        <SectionHeader
          kicker="€500M capital programme"
          title={
            <>
              The financial thesis:{" "}
              <span className="text-aqua">cheaper debt buys faster resilience.</span>
            </>
          }
          lede="A green bond programme priced 25–40bps inside conventional issuance translates into €40–60M in PV coupon savings over the 2027–2030 tenor — more than funding the T2 cyber program by itself."
        />

        <div className="grid lg:grid-cols-12 gap-6 mt-14">
          {/* Left: narrative KPIs */}
          <div className="lg:col-span-5 space-y-4">
            <Kpi
              icon={<Banknote className="w-5 h-5" />}
              label="Programme size"
              value="€500M"
              accent="#1f77b4"
              sub="Multi-tranche 2027–2030"
            />
            <Kpi
              icon={<TrendingDown className="w-5 h-5" />}
              label="Spread vs conventional"
              value="−25 to −40 bps"
              accent="#5db9d9"
              sub="Investor greenium, Taxonomy-eligible"
            />
            <Kpi
              icon={<PiggyBank className="w-5 h-5" />}
              label="PV coupon savings"
              value="€40–60M"
              accent="#2ca02c"
              sub="Discounted at WACC 5.5%"
            />
            <Kpi
              icon={<Gauge className="w-5 h-5" />}
              label="Funding coverage"
              value={`${Math.round((total / 500) * 100)}%`}
              accent="#ff7f0e"
              sub={`€${total}M pipeline against €500M envelope`}
            />
          </div>

          {/* Right: pipeline bars */}
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="lg:col-span-7 card p-6"
          >
            <div className="flex items-baseline justify-between mb-4">
              <div>
                <div className="kicker text-aqua">Use of proceeds</div>
                <div className="font-display text-navy text-2xl mt-1">
                  Capital pipeline · €{total}M committed
                </div>
              </div>
            </div>

            <ResponsiveContainer width="100%" height={360}>
              <BarChart
                data={CAPITAL_PIPELINE}
                layout="vertical"
                margin={{ top: 10, right: 40, left: 20, bottom: 10 }}
              >
                <XAxis
                  type="number"
                  hide
                  domain={[0, Math.max(...CAPITAL_PIPELINE.map((d) => d.eur)) * 1.15]}
                />
                <YAxis
                  dataKey="label"
                  type="category"
                  width={230}
                  tick={{ fill: "#002f5f", fontWeight: 600, fontSize: 12 }}
                  axisLine={false}
                  tickLine={false}
                />
                <Tooltip
                  cursor={{ fill: "rgba(93,185,217,0.08)" }}
                  contentStyle={{
                    background: "white",
                    border: "1px solid #e6e8eb",
                    borderRadius: 12,
                    fontSize: 12,
                  }}
                  formatter={(v: number) => [`€${v}M`, "CAPEX/OPEX"]}
                />
                <Bar dataKey="eur" radius={[0, 8, 8, 0]}>
                  {CAPITAL_PIPELINE.map((d, i) => (
                    <Cell key={i} fill={d.color} />
                  ))}
                  <LabelList
                    dataKey="eur"
                    position="right"
                    formatter={(v: number) => `€${v}M`}
                    style={{ fill: "#002f5f", fontWeight: 700, fontSize: 12 }}
                  />
                </Bar>
              </BarChart>
            </ResponsiveContainer>

            <div className="flex flex-wrap gap-2 mt-2 text-xs text-slate2/70">
              {CAPITAL_PIPELINE.map((d) => (
                <span
                  key={d.label}
                  className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-grid/50"
                >
                  <span
                    className="w-2 h-2 rounded-full"
                    style={{ background: d.color }}
                  />
                  {d.type} · {d.timing}
                </span>
              ))}
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
}

function Kpi({
  icon,
  label,
  value,
  sub,
  accent,
}: {
  icon: React.ReactNode;
  label: string;
  value: string;
  sub: string;
  accent: string;
}) {
  return (
    <motion.div
      initial={{ opacity: 0, x: -14 }}
      whileInView={{ opacity: 1, x: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.45 }}
      className="relative card p-5 flex items-center gap-5"
    >
      <span className="accent-bar" style={{ background: accent }} />
      <div
        className="w-12 h-12 rounded-xl flex items-center justify-center text-white"
        style={{ background: accent }}
      >
        {icon}
      </div>
      <div className="flex-1 min-w-0">
        <div className="kicker text-slate2/60">{label}</div>
        <div className="font-display text-navy text-3xl num-tabular leading-none mt-1">
          {value}
        </div>
        <div className="text-sm text-slate2/70 mt-1">{sub}</div>
      </div>
    </motion.div>
  );
}
