import { motion } from "framer-motion";
import { ROADMAP } from "../content/topics";
import SectionHeader from "./SectionHeader";
import { CheckCircle2 } from "lucide-react";

export default function Roadmap() {
  return (
    <section id="roadmap" className="relative py-28 bg-[#f4f8fb]">
      <div className="wrap">
        <SectionHeader
          kicker="Execution roadmap"
          title={
            <>
              Four years.{" "}
              <span className="text-aqua">Four irrevocable gates.</span>
            </>
          }
          lede="We're not promising 2035 aspirations. We're committing to decisions Aqualia can physically take between 2027 and 2030."
        />

        <div className="relative mt-16">
          {/* Horizontal line */}
          <div className="hidden md:block absolute top-[72px] left-0 right-0 h-[2px] bg-gradient-to-r from-aqua via-t1 to-aqua/30" />

          <div className="grid md:grid-cols-4 gap-6 relative">
            {ROADMAP.map((r, i) => (
              <motion.div
                key={r.year}
                initial={{ opacity: 0, y: 18 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: "-60px" }}
                transition={{ duration: 0.5, delay: i * 0.1 }}
                className="relative"
              >
                {/* Year pill */}
                <div className="hidden md:flex items-center justify-center h-[72px] pb-6">
                  <div className="w-16 h-16 rounded-full bg-white border-[3px] border-aqua shadow-soft flex items-center justify-center font-extrabold text-navy">
                    {r.year}
                  </div>
                </div>

                <div className="card p-6 h-full">
                  <div className="md:hidden kicker text-aqua mb-2">{r.year}</div>
                  <h3 className="font-display text-navy text-xl mb-4">
                    {r.title}
                  </h3>
                  <ul className="space-y-2.5 text-sm text-slate2">
                    {r.bullets.map((b) => (
                      <li key={b} className="flex gap-2 items-start">
                        <CheckCircle2 className="w-4 h-4 text-aqua flex-shrink-0 mt-0.5" />
                        <span>{b}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
