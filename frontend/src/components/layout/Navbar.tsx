import React from 'react';
import { Shield } from 'lucide-react';
import { Link } from 'react-router-dom';

export const Navbar: React.FC = () => {
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 border-b border-white/5 bg-obsidian/80 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-3 group">
          <div className="relative">
            <div className="absolute inset-0 bg-emerald-500/20 rounded-full blur-md group-hover:bg-emerald-500/40 transition-colors" />
            <Shield className="w-8 h-8 text-emerald-400 relative z-10" />
          </div>
          <div>
            <h1 className="text-xl font-bold tracking-tight text-slate-100">CipherEye</h1>
            <p className="text-[10px] uppercase tracking-[0.2em] text-emerald-500/80 font-semibold">Verify Before You Trust</p>
          </div>
        </Link>
        
        <div className="flex items-center gap-6">
          <Link to="/" className="text-sm font-medium text-slate-400 hover:text-emerald-400 transition-colors">
            New Investigation
          </Link>
        </div>
      </div>
    </nav>
  );
};
