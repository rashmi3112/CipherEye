import React, { useEffect } from 'react';
import { useLocation, useNavigate, Navigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { AgentWorkflowVisualizer } from '../components/loading/AgentWorkflowVisualizer';
import { GlassPanel } from '../components/core/GlassPanel';

import { analyzeContent } from '../services/api';
import type { InvestigationReport } from '../services/api';

export const Analyze: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const payloadData = location.state;

  useEffect(() => {
    if (!payloadData) return;

    const runInvestigation = async () => {
      try {
        // Enforce a minimum display time for the visualizer (UX)
        const minTimePromise = new Promise(resolve => setTimeout(resolve, 4000));
        
        let report: InvestigationReport;
        
        try {
           const apiPromise = analyzeContent(payloadData.type, payloadData.payload);
           const [apiReport] = await Promise.all([apiPromise, minTimePromise]);
           report = apiReport;
        } catch (apiError) {
           console.warn("Backend API unavailable, using fallback mock for demonstration.", apiError);
           await minTimePromise;
           report = {
              trust_score: 15,
              risk_level: 'critical',
              threat_categories: ['phishing', 'scam'],
              summary: 'The submitted content exhibits strong indicators of a cyber threat (Fallback Mock Data).',
              findings: ['Backend API connection failed.', 'Showing fallback visual data.'],
              recommendations: ['Ensure the FastAPI backend is running on localhost:8000'],
              confidence: 0.98,
              detected_pii: []
           };
        }
        
        navigate('/report', { state: { report } });
      } catch (error) {
        console.error("Investigation failed", error);
      }
    };

    runInvestigation();
  }, [payloadData, navigate]);

  if (!payloadData) {
    return <Navigate to="/" replace />;
  }

  return (
    <div className="min-h-[calc(100vh-80px)] pt-20 flex flex-col items-center justify-center px-4">
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="w-full max-w-2xl"
      >
        <GlassPanel className="p-10">
          <div className="text-center mb-10">
            <h2 className="text-2xl font-bold text-slate-100 mb-2">Investigation in Progress</h2>
            <p className="text-slate-400">CipherEye is orchestrating AI agents to analyze your submission.</p>
          </div>
          
          <AgentWorkflowVisualizer />
        </GlassPanel>
      </motion.div>
    </div>
  );
};
