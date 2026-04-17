import { motion } from "framer-motion";
import { TOPICS } from "../content/topics";
import SectionHeader from "./SectionHeader";
import { ArrowUpRight, CircleDollarSign, Layers, Scale } from "lucide-react";

export default function Topics() {
  return (
    <section id="topics" className="relative py-28 bg-grid-subtle">
      <div className="wrap">
        <SectionHeader
          kicker="Three material topics"
          title={
            <>
              From <span className="text-aqua">16 candidates</span> to a{" "}
              <span className="italic">decision-ready</span> short-list
            </>
          }
          lede="The matrix is only as honest as the selection rule that produced it. Ours is a 0–100 composite gate combining impact, financial materiality, stakeholder salience, regulatory pressure, and differentiation — locked before Monte Carlo runs."
        />

        <div className="grid lg:grid-cols-3 gap-6 mt-14">
          {TOPICS.map((t, i) => (
            <motion.article
              key={t.code}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-80px" }}
              transition={{ duration: 0.55, delay: i * 0.1 }}
              whileHover={{ y: -8 }}
              className="group relative card p-8 overflow-hidden hover:shadow-glow transition-shadow"
            >
              <span
                className="accent-bar"
                style={{ background: `linear-gradient(180deg, ${t.color}, ${t.color}99)` }}
              />

              <div className="flex items-start justify-between mb-6">
                <div>
                  <div className="kicker" style={{ color: t.color }}>
                    {t.code} · {t.kicker}
                  </div>
                  <h3 className="font-display text-navy text-[28px] leading-tight mt-2 max-w-[22ch]">
                    {t.title}
                  </h3>
                </div>
                <div
                  className="w-12 h-12 rounded-full flex items-center justify-center text-white shadow-soft"
                  style={{ background: t.color }}
                >
                  <Layers className="w-5 h-5" />
                </div>
              </div>

              <p className="text-slate2 leading-relaxed">{t.summary}</p>

              <div
                className="mt-6 pl-4 border-l-2"
                style={{ borderColor: t.color }}
              >
                <div className="text-xs uppercase tracking-[0.2em] text-slate2/60">
                  Headline
                </div>
                <div className="font-semibold text-navy mt-1">{t.headline}</div>
              </div>

              <div className="grid grid-cols-2 gap-3 mt-6">
                <Metric
                  icon={<Scale className="w-4 h-4" />}
                  label="Impact (mean)"
                  value={t.impact.toFixed(2)}
                  color={t.color}
                />
                <Metric
                  icon={<CircleDollarSign className="w-4 h-4" />}
                  label="Financial (mean)"
                  value={t.financial.toFixed(2)}
                  color={t.color}
                />
              </div>

              <div className="mt-6">
                <div className="text-xs uppercase tracking-[0.18em] text-slate2/60 mb-2">
                  Key levers
                </div>
                <ul className="space-y-1.5 text-sm text-slate2">
                  {t.keyLevers.map((k) => (
                    <li key={k} className="flex gap-2 items-start">
                      <span
                        className="mt-1 w-1.5 h-1.5 rounded-full flex-shrink-0"
                        style={{ background: t.color }}
                      />
                      <span>{k}</span>
                    </li>
                  ))}
                </ul>
              </div>

              <div className="mt-6 flex flex-wrap gap-1.5">
                {t.esrs.map((e) => (
                  <span
                    key={e}
                    className="chip bg-grid text-navy text-[11px] px-2.5 py-1"
                  >
                    {e}
                  </span>
                ))}
              </div>

              <div className="absolute bottom-6 right-6 opacity-0 group-hover:opacity-100 transition-opacity">
                <ArrowUpRight className="w-5 h-5" style={{ color: t.color }} />
              </div>
            </motion.article>
          ))}
        </div>
      </div>
    </section>
  );
}

function Metric({
  icon,
  label,
  value,
  color,
}: {
  icon: React.ReactNode;
  label: string;
  value: string;
  color: string;
}) {
  return (
    <div className="rounded-xl bg-grid/50 px-3 py-3">
      <div className="flex items-center gap-1.5 text-[11px] uppercase tracking-[0.14em] text-slate2/60">
        <span style={{ color }}>{icon}</span>
        {label}
      </div>
      <div
        className="num-tabular text-2xl font-extrabold mt-1"
        style={{ color }}
      >
        {value}
      </div>
    </div>
  );
}
