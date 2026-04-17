import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Github, Menu, X } from "lucide-react";

const LINKS = [
  { href: "#topics", label: "Topics" },
  { href: "#matrix", label: "Matrix" },
  { href: "#findings", label: "Findings" },
  { href: "#capital", label: "Capital" },
  { href: "#heatmap", label: "ESRS" },
  { href: "#water", label: "Water stress" },
  { href: "#roadmap", label: "Roadmap" },
  { href: "#peers", label: "Peers" },
];

export default function Nav() {
  const [scrolled, setScrolled] = useState(false);
  const [open, setOpen] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 20);
    onScroll();
    window.addEventListener("scroll", onScroll);
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <header
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        scrolled
          ? "bg-white/90 backdrop-blur-md shadow-[0_1px_0_0_rgba(0,47,95,0.08)]"
          : "bg-white/70 backdrop-blur"
      }`}
    >
      <div className="wrap h-24 flex items-center justify-between">
        <a href="#top" className="flex items-center gap-3 min-w-0">
          <img
            src="/aqualia_logo@2x.png"
            alt="Aqualia"
            className="h-20 md:h-24 w-auto object-contain select-none flex-shrink-0 -my-2"
            draggable={false}
          />
          <span className="hidden md:inline text-slate2/30 text-2xl font-light">
            |
          </span>
          <span className="hidden md:inline font-semibold text-navy text-[15px] tracking-tight truncate">
            Double Materiality 2027&nbsp;–&nbsp;2030
          </span>
        </a>

        <nav className="hidden lg:flex gap-7">
          {LINKS.map((l) => (
            <a key={l.href} href={l.href} className="nav-link">
              {l.label}
            </a>
          ))}
        </nav>

        <div className="flex items-center gap-3">
          <a
            href="https://github.com/ma731/Aqualia-Datathon"
            target="_blank"
            rel="noreferrer"
            className="hidden md:inline-flex items-center gap-2 text-sm font-semibold text-navy hover:text-deep border border-grid rounded-xl px-4 py-2 hover:bg-grid/60 transition"
          >
            <Github className="w-4 h-4" /> Source
          </a>
          <button
            className="lg:hidden p-2 rounded-lg hover:bg-grid/60"
            onClick={() => setOpen((v) => !v)}
            aria-label="Menu"
          >
            {open ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>
      </div>

      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="lg:hidden overflow-hidden border-t border-grid bg-white"
          >
            <div className="wrap py-4 flex flex-col gap-3">
              {LINKS.map((l) => (
                <a
                  key={l.href}
                  href={l.href}
                  onClick={() => setOpen(false)}
                  className="py-2 font-semibold text-navy"
                >
                  {l.label}
                </a>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </header>
  );
}
