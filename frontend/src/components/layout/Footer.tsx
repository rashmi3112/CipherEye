import React from 'react';

export const Footer: React.FC = () => {
  return (
    <footer className="border-t border-white/5 bg-obsidian/40 py-6 mt-16 backdrop-blur-sm relative z-25">
      <div className="max-w-7xl mx-auto px-6 text-center">
        <p className="text-xs text-slate-500 font-medium">
          CipherEye @2026. All rights reserved.
        </p>
      </div>
    </footer>
  );
};
