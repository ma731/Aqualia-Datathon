import type { DashboardData } from "./types";

const fallback: DashboardData = {
  mc: [],
  aqueduct: [],
  coverage: [],
  tornado: [],
  robustness: [],
};

export const DATA: DashboardData =
  typeof window !== "undefined" && window.DATA ? window.DATA : fallback;

export * from "./types";
