import Nav from "./components/Nav";
import Hero from "./components/Hero";
import Topics from "./components/Topics";
import Matrix from "./components/Matrix";
import Findings from "./components/Findings";
import Capital from "./components/Capital";
import Heatmap from "./components/Heatmap";
import WaterStress from "./components/WaterStress";
import Roadmap from "./components/Roadmap";
import Peers from "./components/Peers";
import Footer from "./components/Footer";

export default function App() {
  return (
    <div className="relative">
      <Nav />
      <main>
        <Hero />
        <Topics />
        <Matrix />
        <Findings />
        <Capital />
        <Heatmap />
        <WaterStress />
        <Roadmap />
        <Peers />
      </main>
      <Footer />
    </div>
  );
}
