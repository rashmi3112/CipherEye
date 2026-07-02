import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { ShieldCheck, Server, Search, FileKey, CheckCircle2 } from 'lucide-react';
import { cn } from '../../utils/cn';

interface Step {
  id: string;
  label: string;
  icon: React.ReactNode;
}

const steps: Step[] = [
  { id: 'init', label: 'Initializing Orchestrator...', icon: <Server className="w-5 h-5" /> },
  { id: 'pii', label: 'Scanning for PII...', icon: <FileKey className="w-5 h-5" /> },
  { id: 'content', label: 'Content Agent analyzing...', icon: <Search className="w-5 h-5" /> },
  { id: 'threat', label: 'Threat Agent assigning score...', icon: <ShieldCheck className="w-5 h-5" /> },
  { id: 'report', label: 'Report Agent generating findings...', icon: <CheckCircle2 className="w-5 h-5" /> }
];

export const AgentWorkflowVisualizer: React.FC = () => {
  const [currentStepIndex, setCurrentStepIndex] = useState(0);

  // Simulate the workflow progression
  useEffect(() => {
    if (currentStepIndex < steps.length - 1) {
      const timer = setTimeout(() => {
        setCurrentStepIndex(prev => prev + 1);
      }, 900); // Progress every 900ms to complete within the 4s UX budget
      return () => clearTimeout(timer);
    }
  }, [currentStepIndex]);

  return (
    <div className="flex flex-col items-center max-w-lg mx-auto w-full">
      
      {/* Central Pulsing Brain/Node */}
      <div className="relative flex items-center justify-center mb-12">
        <motion.div
          animate={{ scale: [1, 1.2, 1], opacity: [0.3, 0.6, 0.3] }}
          transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
          className="absolute w-32 h-32 bg-emerald-500/20 rounded-full blur-xl"
        />
        <div className="relative z-10 w-16 h-16 bg-obsidian border border-emerald-500/50 rounded-xl flex items-center justify-center glow-safe">
          <Server className="w-8 h-8 text-emerald-400" />
        </div>
      </div>

      {/* Step List */}
      <div className="w-full space-y-4">
        {steps.map((step, index) => {
          const isActive = index === currentStepIndex;
          const isCompleted = index < currentStepIndex;
          const isPending = index > currentStepIndex;

          return (
            <motion.div
              key={step.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ 
                opacity: isPending ? 0.3 : 1, 
                x: 0,
                scale: isActive ? 1.02 : 1 
              }}
              className={cn(
                "flex items-center gap-4 p-4 rounded-lg border transition-colors duration-300",
                isActive ? "bg-emerald-500/10 border-emerald-500/30" : 
                isCompleted ? "bg-white/5 border-white/10" : "bg-transparent border-transparent"
              )}
            >
              <div className={cn(
                "w-8 h-8 rounded-full flex items-center justify-center",
                isActive ? "bg-emerald-500/20 text-emerald-400" :
                isCompleted ? "bg-slate-800 text-slate-400" : "bg-transparent text-slate-600"
              )}>
                {step.icon}
              </div>
              
              <span className={cn(
                "font-medium",
                isActive ? "text-emerald-400" :
                isCompleted ? "text-slate-300" : "text-slate-500"
              )}>
                {step.label}
              </span>
              
              {isActive && (
                <motion.div className="ml-auto flex gap-1">
                  <motion.span animate={{ opacity: [0,1,0] }} transition={{ duration: 1, repeat: Infinity, delay: 0 }} className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
                  <motion.span animate={{ opacity: [0,1,0] }} transition={{ duration: 1, repeat: Infinity, delay: 0.2 }} className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
                  <motion.span animate={{ opacity: [0,1,0] }} transition={{ duration: 1, repeat: Infinity, delay: 0.4 }} className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
                </motion.div>
              )}
            </motion.div>
          );
        })}
      </div>
    </div>
  );
};
