export type Topic = {
  code: "T1" | "T2" | "T3";
  title: string;
  color: string;
  accent: string;
  kicker: string;
  headline: string;
  summary: string;
  esrs: string[];
  financialEur: string;
  tag: "Core" | "Differentiator" | "Enabler";
  impact: number;
  financial: number;
  keyLevers: string[];
};

export const TOPICS: Topic[] = [
  {
    code: "T1",
    title: "Water Resilience & Equitable Access",
    color: "#1f77b4",
    accent: "from-[#1f77b4] to-[#5db9d9]",
    kicker: "Sector-core",
    headline: "€180–240M revenue at risk by 2030 if Segura reserves fail.",
    summary:
      "Physical climate + regulatory tightening collapse into a single line item: the basin-level cost of water. Aqualia already has the operational muscle — reuse & desalination — but capital allocation must be reframed.",
    esrs: ["E1", "E3", "S3", "S4"],
    financialEur: "€180–240M",
    tag: "Core",
    impact: 3.98,
    financial: 3.07,
    keyLevers: [
      "Desalination vs reuse real-option",
      "Leak-reduction CAPEX (ProMiNE)",
      "Tariff adaptation for vulnerable households",
    ],
  },
  {
    code: "T2",
    title: "Digital & Cyber Infrastructure",
    color: "#ff7f0e",
    accent: "from-[#ff7f0e] to-[#f2b039]",
    kicker: "Blind-spot differentiator",
    headline: "Unaddressed NIS2 exposure: €35–90M regulatory penalty envelope.",
    summary:
      "SCADA, customer data, AI-enabled operations — the attack surface is expanding faster than the disclosure. This is where we carve a differentiation wedge that peers haven't drawn yet.",
    esrs: ["G1", "S4"],
    financialEur: "€35–90M",
    tag: "Differentiator",
    impact: 3.08,
    financial: 2.75,
    keyLevers: [
      "NIS2 resilience program",
      "AI governance for operations",
      "Customer data trust index",
    ],
  },
  {
    code: "T3",
    title: "Green Finance & Integrity",
    color: "#2ca02c",
    accent: "from-[#2ca02c] to-[#5db9d9]",
    kicker: "Strategic enabler",
    headline: "€500M green bond programme → €40–60M PV coupon savings.",
    summary:
      "Unlocks the CAPEX envelope that topics 1 and 2 demand, while demonstrating EU Taxonomy alignment and Article 9 investor-ready disclosures — the cheapest risk mitigant we control.",
    esrs: ["G1", "E1", "E3"],
    financialEur: "€40–60M PV savings",
    tag: "Enabler",
    impact: 3.24,
    financial: 2.42,
    keyLevers: [
      "EU Taxonomy alignment proof",
      "ICMA-compliant use-of-proceeds",
      "Second-party opinion pipeline",
    ],
  },
];

export const HERO_KPIS = [
  { label: "Material topics", value: "3", hint: "distilled from 16 candidates" },
  { label: "Monte Carlo draws", value: "10,000", hint: "per topic per scheme" },
  { label: "Financial envelope", value: "€500M", hint: "green bond programme" },
  { label: "PV savings", value: "€40–60M", hint: "vs. conventional debt" },
];

export const FINDINGS = [
  {
    code: "F1",
    title: "Water is a single, re-priced risk — not a climate sub-topic",
    body: "E1 (climate) and E3 (water) co-move. Collapsing them into 'Water Resilience & Equitable Access' recovers decision-usefulness and exposes the true CAPEX call: desal vs reuse, under 2030 stress.",
    tag: "Methodological",
  },
  {
    code: "F2",
    title: "Cyber is Aqualia's cheapest materiality upgrade",
    body: "Zero incremental data cost, maximum differentiation. NIS2 exposure is already on the balance sheet — disclosing it is a pure trust premium for bond investors.",
    tag: "Strategic",
  },
  {
    code: "F3",
    title: "Green finance is the pivot, not the conclusion",
    body: "T3 looks 'less material' by severity, but it gates the CAPEX needed to solve T1 and T2. Treating it as an enabler is what the matrix alone can't show.",
    tag: "Capital allocation",
  },
  {
    code: "F4",
    title: "Biodiversity stayed off the short-list — consciously",
    body: "Aqueduct + sector peer review show the topic is material to nature but immaterial to 5Y P&L. It belongs in the monitoring ring, not the priority ring.",
    tag: "Scope discipline",
  },
];

export const CAPITAL_PIPELINE = [
  {
    label: "Water reuse + leak reduction (T1)",
    eur: 220,
    color: "#1f77b4",
    type: "CAPEX",
    timing: "2027–2029",
  },
  {
    label: "Desalination optionality (T1)",
    eur: 140,
    color: "#5db9d9",
    type: "Real option",
    timing: "Trigger 2029 if BWS > 4.5",
  },
  {
    label: "Cyber & NIS2 resilience (T2)",
    eur: 60,
    color: "#ff7f0e",
    type: "CAPEX/OPEX",
    timing: "2027–2028",
  },
  {
    label: "EU Taxonomy + SPO (T3)",
    eur: 10,
    color: "#2ca02c",
    type: "OPEX",
    timing: "2027",
  },
  {
    label: "Contingency buffer",
    eur: 70,
    color: "#d6cdb7",
    type: "Reserve",
    timing: "Rolling",
  },
];

export const ROADMAP = [
  {
    year: "2027",
    title: "Issue & anchor",
    bullets: [
      "Launch €500M green bond programme (SLB-linked tranches optional)",
      "Publish inaugural CSRD-aligned DMA report",
      "NIS2 gap closure milestone #1",
    ],
  },
  {
    year: "2028",
    title: "Deploy & validate",
    bullets: [
      "Commission water reuse & leak CAPEX tranche 1",
      "First SPO progress report",
      "Customer trust index launch (T2)",
    ],
  },
  {
    year: "2029",
    title: "Decide & scale",
    bullets: [
      "Real-option trigger review on desalination",
      "Second tranche of bond programme (if rating holds)",
      "Supplier NIS2 cascade complete",
    ],
  },
  {
    year: "2030",
    title: "Prove & refinance",
    bullets: [
      "Full transition-plan conformance under ESRS E1/E3",
      "Refinance maturities at tightened Taxonomy spread",
      "3M+ vulnerable households served under adaptive tariff",
    ],
  },
];

export const PEERS = [
  { name: "Veolia", impact: 4.1, financial: 3.2, dma: 0.9, label: "Scale leader" },
  { name: "Suez", impact: 3.9, financial: 3.0, dma: 0.85, label: "Peer benchmark" },
  { name: "Aqualia — today", impact: 3.5, financial: 2.6, dma: 0.62, label: "Current" },
  {
    name: "Aqualia — 2027 plan",
    impact: 3.98,
    financial: 3.07,
    dma: 0.92,
    label: "Target (our plan)",
  },
  { name: "Acciona Agua", impact: 3.6, financial: 2.8, dma: 0.7, label: "Regional" },
  { name: "Severn Trent", impact: 3.7, financial: 2.9, dma: 0.83, label: "UK water" },
];
