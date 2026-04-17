import { useEffect, useRef, useState } from "react";
import { motion } from "framer-motion";
import { ArrowRight, Droplets, ShieldCheck, Sparkles } from "lucide-react";
import { HERO_KPIS } from "../content/topics";
import WaterDroplets from "./WaterDroplets";
import Ripples from "./Ripples";
import AnimatedWave from "./AnimatedWave";

export default function Hero() {
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const [videoReady, setVideoReady] = useState(false);

  // Graceful video support: activates only if the asset exists at /hero-video.mp4
  useEffect(() => {
    const v = videoRef.current;
    if (!v) return;
    const onCanPlay = () => setVideoReady(true);
    const onError = () => setVideoReady(false);
    v.addEventListener("canplay", onCanPlay);
    v.addEventListener("error", onError);
    return () => {
      v.removeEventListener("canplay", onCanPlay);
      v.removeEventListener("error", onError);
    };
  }, []);

  return (
    <section
      id="top"
      className="relative overflow-hidden bg-hero-grad text-white pt-40 pb-48"
    >
      {/* Optional background video — activates if public/hero-video.mp4 exists */}
      <video
        ref={videoRef}
        className={`absolute inset-0 w-full h-full object-cover transition-opacity duration-1000 ${
          videoReady ? "opacity-45" : "opacity-0"
        }`}
        src="/hero-video.mp4"
        autoPlay
        muted
        loop
        playsInline
        preload="metadata"
        aria-hidden
      />
      {/* Dark gradient overlay always on top of video for text legibility */}
      {videoReady && (
        <div
          aria-hidden
          className="absolute inset-0 bg-gradient-to-b from-navy2/80 via-navy/70 to-deep/80"
        />
      )}

      <div className="dots" />

      {/* Falling water droplets */}
      <WaterDroplets count={42} color="#8ed3e6" />

      {/* Floating bubbles */}
      <motion.div
        aria-hidden
        className="absolute -top-10 -left-10 w-80 h-80 rounded-full bg-aqua/30 blur-3xl"
        animate={{ y: [0, 20, 0], x: [0, 10, 0] }}
        transition={{ duration: 12, repeat: Infinity }}
      />
      <motion.div
        aria-hidden
        className="absolute -bottom-16 right-0 w-96 h-96 rounded-full bg-t1/25 blur-3xl"
        animate={{ y: [0, -25, 0], x: [0, -15, 0] }}
        transition={{ duration: 14, repeat: Infinity }}
      />

      <div className="wrap relative z-10 grid lg:grid-cols-12 gap-10 items-center">
        <div className="lg:col-span-7">
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="flex items-center gap-2"
          >
            <span className="chip bg-white/10 text-aqua2 border border-white/15">
              <Sparkles className="w-3.5 h-3.5" /> IE Sustainability Datathon · 2026
            </span>
            <span className="chip bg-white/10 text-white/80 border border-white/15">
              CSRD · ESRS-aligned
            </span>
          </motion.div>

          <motion.h1
            initial={{ opacity: 0, y: 18 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, delay: 0.1 }}
            className="font-display font-light tracking-tight text-5xl md:text-6xl lg:text-[72px] leading-[1.02] mt-8"
          >
            Three topics.
            <br />
            One <span className="italic text-aqua2">€500M</span> capital call.
            <br />
            <span className="text-aqua">Ten years of runway.</span>
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, delay: 0.25 }}
            className="text-white/80 text-lg md:text-xl mt-7 max-w-2xl leading-relaxed"
          >
            A double materiality assessment for Aqualia that is auditable by scipy, legible
            by a board, and pricable by the bond desk. Monte Carlo for uncertainty, real
            options for CAPEX, stakeholder salience for the inside-out.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, delay: 0.4 }}
            className="flex flex-wrap items-center gap-3 mt-10"
          >
            <a href="#matrix" className="btn-primary">
              Open matrix <ArrowRight className="w-4 h-4" />
            </a>
            <a href="#findings" className="btn-ghost">
              <ShieldCheck className="w-4 h-4" /> Read findings
            </a>
            <a
              href="#water"
              className="inline-flex items-center gap-2 text-aqua2 font-semibold hover:text-white ml-1"
            >
              <Droplets className="w-4 h-4" /> Water stress map
            </a>
          </motion.div>

          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.8, delay: 0.55 }}
            className="mt-14 grid grid-cols-2 md:grid-cols-4 gap-3 max-w-3xl"
          >
            {HERO_KPIS.map((k) => (
              <div
                key={k.label}
                className="card-glass rounded-2xl p-4 text-white"
              >
                <div className="num-tabular text-3xl font-bold tracking-tight">
                  {k.value}
                </div>
                <div className="text-xs uppercase tracking-[0.18em] text-aqua2 mt-1">
                  {k.label}
                </div>
                <div className="text-[11px] text-white/60 mt-1">{k.hint}</div>
              </div>
            ))}
          </motion.div>
        </div>

        {/* Right-side decorative illustration */}
        <div className="lg:col-span-5 relative hidden lg:block">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 1, delay: 0.4 }}
            className="relative aspect-square"
          >
            <HeroOrb />
          </motion.div>
        </div>
      </div>

      {/* Splash ripples where droplets meet the wave */}
      <Ripples count={6} color="#8ed3e6" className="z-[1]" />

      {/* Animated wave divider */}
      <AnimatedWave color="#ffffff" height={110} />
    </section>
  );
}

function HeroOrb() {
  return (
    <div className="relative w-full h-full">
      {/* Concentric rings */}
      {[0, 1, 2, 3].map((i) => (
        <motion.div
          key={i}
          className="absolute inset-0 rounded-full border border-aqua/30"
          style={{ margin: `${i * 24}px` }}
          animate={{ rotate: i % 2 === 0 ? 360 : -360 }}
          transition={{ duration: 40 + i * 10, repeat: Infinity, ease: "linear" }}
        />
      ))}

      {/* Core glow */}
      <motion.div
        className="absolute inset-12 rounded-full bg-gradient-to-br from-aqua/40 via-t1/30 to-transparent blur-2xl"
        animate={{ scale: [1, 1.08, 1] }}
        transition={{ duration: 5, repeat: Infinity }}
      />

      {/* Topic dots */}
      {[
        { label: "T1", angle: -30, r: "#5db9d9" },
        { label: "T2", angle: 95, r: "#ff7f0e" },
        { label: "T3", angle: 210, r: "#8ed3e6" },
      ].map(({ label, angle, r }) => {
        const rad = (angle * Math.PI) / 180;
        const x = 50 + 34 * Math.cos(rad);
        const y = 50 + 34 * Math.sin(rad);
        return (
          <motion.div
            key={label}
            className="absolute flex items-center justify-center rounded-full text-navy font-extrabold shadow-glow"
            style={{
              left: `${x}%`,
              top: `${y}%`,
              width: 64,
              height: 64,
              transform: "translate(-50%,-50%)",
              background: r,
            }}
            animate={{ y: [0, -8, 0] }}
            transition={{ duration: 4, repeat: Infinity, delay: angle / 90 }}
          >
            {label}
          </motion.div>
        );
      })}

      {/* Center logo */}
      <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
        <div className="w-44 h-44 rounded-full bg-white flex items-center justify-center shadow-glow px-3 py-1">
          <img
            src="/aqualia_logo@2x.png"
            alt="Aqualia"
            className="w-full h-full object-contain"
            draggable={false}
          />
        </div>
      </div>
    </div>
  );
}
