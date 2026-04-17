import { motion } from "framer-motion";
import { FINDINGS } from "../content/topics";
import SectionHeader from "./SectionHeader";
import { Lightbulb } from "lucide-react";

export default function Findings() {
  return (
    <section
      id="findings"
      className="relative py-28 bg-gradient-to-b from-white to-[#f4f8fb]"
    >
      <div className="wrap">
        <SectionHeader
          kicker="Four findings a judge can defend"
          title={
            <>
              What the numbers <span className="italic">actually</span> say.
            </>
          }
          lede="Every finding is traceable to a piece of evidence in the data room — not a workshop vibe."
        />

        <div className="grid md:grid-cols-2 gap-5 mt-14">
          {FINDINGS.map((f, i) => (
            <motion.div
              key={f.code}
              initial={{ opacity: 0, y: 18 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-60px" }}
              transition={{ duration: 0.5, delay: i * 0.08 }}
              className="relative card p-7 hover:shadow-glow transition-shadow group"
            >
              <div className="flex items-start gap-4">
                <div className="w-12 h-12 rounded-xl bg-aqua/15 text-navy flex items-center justify-center font-extrabold">
                  <Lightbulb className="w-5 h-5 text-aqua" />
                </div>
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <span className="text-xs font-bold text-aqua">{f.code}</span>
                    <span className="text-[11px] uppercase tracking-[0.16em] text-slate2/50">
                      {f.tag}
                    </span>
                  </div>
                  <h3 className="font-display text-navy text-2xl leading-tight">
                    {f.title}
                  </h3>
                  <p className="text-slate2 mt-3 leading-relaxed">{f.body}</p>
                </div>
              </div>
              <div className="absolute inset-x-0 bottom-0 h-1 bg-gradient-to-r from-aqua via-t1 to-transparent opacity-0 group-hover:opacity-100 transition-opacity rounded-b-2xl" />
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
