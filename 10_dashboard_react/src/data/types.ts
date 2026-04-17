export type McRow = {
  topic: string;
  impact_mean: number;
  impact_p5: number;
  impact_p50: number;
  impact_p95: number;
  financial_mean: number;
  financial_p5: number;
  financial_p50: number;
  financial_p95: number;
  ellipse_width: number;
  ellipse_height: number;
  ellipse_angle: number;
  in_target_zone: boolean;
};

export type AqueductRow = {
  country: string;
  iso3: string;
  region_label: string;
  bws_category_2024: string;
  bws_score_2024: number;
  bws_category_2030_BAU: string;
  bws_score_2030_BAU: number;
  revenue_share_pct: number;
  satisfaction_2024: number | "";
  concession_note: string;
};

export type CoverageBand = "dark_red" | "red" | "amber" | "green";

export type CoverageRow = {
  dp_id: string;
  standard: string;
  family: string;
  disclosure_requirement: string;
  description: string;
  datapoint_type: string;
  coverage_score: number;
  band: CoverageBand;
  top_chunk_source: string;
  top_chunk_page: number | string;
  top_chunk_text: string;
};

export type TornadoRow = {
  topic: string;
  axis: "Impact" | "Financial";
  input: string;
  base: number;
  swing: number;
  low: number;
  high: number;
  abs_swing: number;
};

export type RobustnessRow = {
  scheme: string;
  topic: string;
  impact_mean: number;
  financial_mean: number;
  in_target_zone: boolean;
};

export type DashboardData = {
  mc: McRow[];
  aqueduct: AqueductRow[];
  coverage: CoverageRow[];
  tornado: TornadoRow[];
  robustness: RobustnessRow[];
};

declare global {
  interface Window {
    DATA: DashboardData;
  }
}
