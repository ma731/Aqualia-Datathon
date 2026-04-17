import { useMemo, useState } from "react";
import { motion } from "framer-motion";
import { DATA } from "../data";
import type { CoverageBand } from "../data";
import SectionHeader from "./SectionHeader";

const BAND_COLOR: Record<CoverageBand, string> = {
  dark_red: "#7c1d1d",
  red: "#c83c35",
  amber: "#f2b039",
  green: "#1b7f3b",
};

const BAND_LABEL: Record<CoverageBand, string> = {
  dark_red: "Critical gap",
  red: "Gap",
  amber: "Partial",
  green: "Covered",
};

export default function Heatmap() {
  const [selected, setSelected] = useState<string | null>(null);

  const { standards, grouped, counts } = useMemo(() => {
    const byStd: Record<string, typeof DATA.coverage> = {};
    DATA.coverage.forEach((c) => {
      (byStd[c.standard] ||= []).push(c);
    });
    const stds = Object.keys(byStd).sort();
    const countsLocal: Record<CoverageBand, number> = {
      dark_red: 0,
      red: 0,
      amber: 0,
      green: 0,
    };
    DATA.coverage.forEach((c) => (countsLocal[c.band] += 1));
    return { standards: stds, grouped: byStd, counts: countsLocal };
  }, []);

  const total = DATA.coverage.length;
  const selectedRow = selected
    ? DATA.coverage.find((c) => c.dp_id === selected) ?? null
    : null;

  return (
    <section id="heatmap" className="relative py-28 bg-[#f4f8fb]">
      <div className="wrap">
        <SectionHeader
          kicker="ESRS datapoint coverage"
          title={
            <>
              {total} datapoints. <span className="text-aqua">Nothing hidden.</span>
            </>
          }
          lede="A semantic coverage score for every required disclosure. Click a cell to see the evidence snippet and where we found it in Aqualia's 2025 report pack."
        />

        <div className="grid md:grid-cols-4 gap-3 mt-10">
          {(Object.keys(BAND_LABEL) as CoverageBand[]).map((b) => (
            <div key={b} className="card p-4 flex items-center gap-3">
              <span
                className="w-4 h-4 rounded"
                style={{ background: BAND_COLOR[b] }}
              />
              <div>
                <div className="text-[11px] uppercase tracking-[0.14em] text-slate2/60">
                  {BAND_LABEL[b]}
                </div>
                <div className="font-bold text-navy num-tabular">
                  {counts[b]}{" "}
                  <span className="text-slate2/50 text-xs">
                    / {total} · {Math.round((counts[b] / total) * 100)}%
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="mt-10 grid lg:grid-cols-12 gap-6">
          <div className="lg:col-span-8 card p-6">
            <div className="kicker text-aqua mb-3">By ESRS standard</div>
            <div className="space-y-3">
              {standards.map((std) => (
                <div key={std} className="flex items-start gap-4">
                  <div className="w-14 pt-0.5">
                    <div className="font-extrabold text-navy">{std}</div>
                    <div className="text-[10px] text-slate2/60 uppercase tracking-wider">
                      {grouped[std][0].family}
                    </div>
                  </div>
                  <div className="flex flex-wrap gap-1.5 flex-1">
                    {grouped[std].map((c) => (
                      <motion.button
                        key={c.dp_id}
                        whileHover={{ scale: 1.25, zIndex: 10 }}
                        onClick={() => setSelected(c.dp_id)}
                        title={`${c.dp_id} · ${c.disclosure_requirement} · ${(c.coverage_score * 100).toFixed(0)}%`}
                        className={`w-5 h-5 rounded-[4px] transition-shadow ${
                          selected === c.dp_id
                            ? "ring-2 ring-navy shadow-glow"
                            : ""
                        }`}
                        style={{ background: BAND_COLOR[c.band] }}
                      />
                    ))}
                  </div>
                </div>
              ))}
            </div>
            <div className="mt-4 text-xs text-slate2/60">
              Each square = one ESRS datapoint · hover to reveal ID · click for evidence
            </div>
          </div>

          {/* Detail panel */}
          <motion.div
            key={selectedRow?.dp_id ?? "empty"}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="lg:col-span-4 card p-6 h-fit sticky top-28"
          >
            {selectedRow ? (
              <>
                <div className="flex items-center gap-2 mb-3">
                  <span
                    className="chip px-2.5 py-1 text-white text-[11px]"
                    style={{ background: BAND_COLOR[selectedRow.band] }}
                  >
                    {BAND_LABEL[selectedRow.band]}
                  </span>
                  <span className="text-xs text-slate2/60">
                    {(selectedRow.coverage_score * 100).toFixed(0)}% coverage
                  </span>
                </div>
                <div className="kicker text-aqua">
                  {selectedRow.dp_id} · {selectedRow.standard}
                </div>
                <h4 className="font-display text-navy text-xl mt-1">
                  {selectedRow.disclosure_requirement}
                </h4>
                <p className="text-sm text-slate2 mt-3 leading-relaxed">
                  {selectedRow.description}
                </p>
                <div className="mt-5 rounded-xl bg-grid/50 p-4">
                  <div className="text-[11px] uppercase tracking-wider text-slate2/60 mb-1">
                    Top evidence ·{" "}
                    <span className="text-navy font-bold">
                      p.{selectedRow.top_chunk_page}
                    </span>
                  </div>
                  <div className="text-xs font-semibold text-navy truncate mb-2">
                    {selectedRow.top_chunk_source}
                  </div>
                  <p className="text-xs text-slate2/80 leading-relaxed line-clamp-5">
                    {selectedRow.top_chunk_text}
                  </p>
                </div>
              </>
            ) : (
              <div className="text-center text-slate2/60 py-14">
                <div className="text-5xl mb-3">◈</div>
                <div className="text-sm">
                  Select any square on the heatmap to inspect evidence
                </div>
              </div>
            )}
          </motion.div>
        </div>
      </div>
    </section>
  );
}
