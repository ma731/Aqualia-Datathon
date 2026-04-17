import { motion } from "framer-motion";

type Props = {
  kicker: string;
  title: React.ReactNode;
  lede?: React.ReactNode;
  align?: "left" | "center";
};

export default function SectionHeader({ kicker, title, lede, align = "left" }: Props) {
  return (
    <div className={align === "center" ? "text-center max-w-3xl mx-auto" : "max-w-3xl"}>
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true, margin: "-60px" }}
        transition={{ duration: 0.5 }}
        className="kicker mb-3"
      >
        {kicker}
      </motion.div>
      <motion.h2
        initial={{ opacity: 0, y: 14 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true, margin: "-60px" }}
        transition={{ duration: 0.6, delay: 0.05 }}
        className="font-display text-navy tracking-tight text-4xl md:text-5xl leading-[1.05]"
      >
        {title}
      </motion.h2>
      {lede && (
        <motion.p
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true, margin: "-60px" }}
          transition={{ duration: 0.6, delay: 0.15 }}
          className="text-slate2 text-lg mt-5 leading-relaxed"
        >
          {lede}
        </motion.p>
      )}
    </div>
  );
}
