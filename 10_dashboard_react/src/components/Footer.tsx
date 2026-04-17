export default function Footer() {
  return (
    <footer className="bg-navy2 text-white/80 pt-16 pb-10 mt-24 relative overflow-hidden">
      <div className="dots" />
      <div className="wrap relative">
        <div className="grid md:grid-cols-3 gap-10">
          <div>
            <div className="inline-flex items-center justify-center bg-white rounded-xl px-4 py-1 mb-4 shadow-soft">
              <img
                src="/aqualia_logo@2x.png"
                alt="Aqualia"
                className="h-16 w-auto object-contain select-none"
                draggable={false}
              />
            </div>
            <p className="text-sm text-white/60 max-w-xs">
              Double Materiality Assessment 2027–2030. Built for the IE Sustainability Datathon
              2026. Data room is fully auditable and reproducible from frozen Python inputs.
            </p>
          </div>
          <div>
            <div className="kicker text-aqua2 mb-4">Deliverables</div>
            <ul className="space-y-2 text-sm">
              <li><a className="hover:text-aqua" href="#matrix">Interactive materiality matrix</a></li>
              <li><a className="hover:text-aqua" href="#heatmap">ESRS datapoint heatmap</a></li>
              <li><a className="hover:text-aqua" href="#capital">€500M capital allocation plan</a></li>
              <li><a className="hover:text-aqua" href="#roadmap">2027–2030 execution roadmap</a></li>
            </ul>
          </div>
          <div>
            <div className="kicker text-aqua2 mb-4">Engineered with</div>
            <ul className="space-y-2 text-sm">
              <li>Python · pandas · scipy · Monte Carlo (10k draws)</li>
              <li>React · TypeScript · Tailwind · Framer Motion</li>
              <li>Plotly · Recharts · Lucide</li>
              <li>Full methodology in <code className="text-aqua">03_analysis/</code></li>
            </ul>
          </div>
        </div>
        <div className="mt-12 pt-8 border-t border-white/10 flex flex-col md:flex-row items-start md:items-center justify-between gap-3 text-xs text-white/50">
          <div>© 2026 · Datathon submission · Not an official Aqualia publication.</div>
          <div>Designed with Aqualia brand colors · navy · aqua · sand</div>
        </div>
      </div>
    </footer>
  );
}
