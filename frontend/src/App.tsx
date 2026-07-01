import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Navbar } from './components/layout/Navbar';
import { AnimatedBackground } from './components/layout/AnimatedBackground';
import { Footer } from './components/layout/Footer';
import { Home } from './pages/Home';
import { Analyze } from './pages/Analyze';
import { Report } from './pages/Report';

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen flex flex-col">
        <AnimatedBackground />
        <Navbar />
        <main className="relative z-10 pt-20 flex-grow">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/analyze" element={<Analyze />} />
            <Route path="/report" element={<Report />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </BrowserRouter>
  );
}

export default App;
