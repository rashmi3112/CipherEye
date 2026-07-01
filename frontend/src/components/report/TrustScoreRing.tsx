import React from 'react';
import { motion } from 'framer-motion';
import { cn } from '../../utils/cn';

interface TrustScoreRingProps {
  score: number;
}

export const TrustScoreRing: React.FC<TrustScoreRingProps> = ({ score }) => {
  // Determine color based on score (0-100 where 100 is safe)
  let colorClass = "text-rose-500";
  let glowClass = "drop-shadow-[0_0_15px_rgba(244,63,94,0.5)]";
  
  if (score >= 80) {
    colorClass = "text-emerald-500";
    glowClass = "drop-shadow-[0_0_15px_rgba(16,185,129,0.5)]";
  } else if (score >= 40) {
    colorClass = "text-amber-500";
    glowClass = "drop-shadow-[0_0_15px_rgba(245,158,11,0.5)]";
  }

  const radius = 90;
  const circumference = 2 * Math.PI * radius;
  // Score is 0-100, we map it to stroke-dashoffset
  const strokeDashoffset = circumference - (score / 100) * circumference;

  return (
    <div className="relative flex items-center justify-center w-64 h-64 mx-auto">
      <svg className="w-full h-full transform -rotate-90" viewBox="0 0 200 200">
        {/* Background Track */}
        <circle
          cx="100"
          cy="100"
          r={radius}
          fill="transparent"
          stroke="currentColor"
          strokeWidth="8"
          className="text-slate-800"
        />
        {/* Animated Progress Ring */}
        <motion.circle
          cx="100"
          cy="100"
          r={radius}
          fill="transparent"
          stroke="currentColor"
          strokeWidth="8"
          strokeLinecap="round"
          className={cn(colorClass, glowClass)}
          initial={{ strokeDashoffset: circumference }}
          animate={{ strokeDashoffset }}
          transition={{ duration: 1.5, ease: "easeOut" }}
          style={{ strokeDasharray: circumference }}
        />
      </svg>
      
      {/* Center Content */}
      <div className="absolute flex flex-col items-center justify-center">
        <motion.span 
          initial={{ opacity: 0, scale: 0.5 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.5, duration: 0.5 }}
          className={cn("text-6xl font-bold tracking-tighter", colorClass, glowClass)}
        >
          {score}
        </motion.span>
        <span className="text-sm uppercase tracking-widest text-slate-400 font-medium mt-1">
          Trust Score
        </span>
      </div>
    </div>
  );
};
