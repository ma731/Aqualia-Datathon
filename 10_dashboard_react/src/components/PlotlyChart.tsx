import Plotly from "plotly.js-dist-min";
import factoryNS from "react-plotly.js/factory";

// react-plotly.js/factory is CJS; Vite may wrap it as { default: fn }.
// Defensive unwrap to tolerate both shapes.
// eslint-disable-next-line @typescript-eslint/no-explicit-any
const createPlotlyComponent: (p: unknown) => any =
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  typeof factoryNS === "function" ? (factoryNS as any) : (factoryNS as any).default;

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const Plot = createPlotlyComponent(Plotly as any);

export default Plot;
