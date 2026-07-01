import React from 'react';
import { useLocation, Navigate, useNavigate } from 'react-router-dom';
import { AlertTriangle, CheckCircle, ShieldAlert, Shield, ArrowLeft, Search } from 'lucide-react';
import type { InvestigationReport } from '../services/api';
import { GlassPanel } from '../components/core/GlassPanel';
import { Button } from '../components/core/Button';
import { TrustScoreRing } from '../components/report/TrustScoreRing';
import { cn } from '../utils/cn';

export const Report: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const report: InvestigationReport = location.state?.report;

  if (!report) {
    return <Navigate to="/" replace />;
  }

  const isSafe = report.risk_level === 'low';
  const RiskIcon = isSafe ? Shield : ShieldAlert;

  const riskColors = {
    low: 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20 glow-safe',
    medium: 'text-amber-400 bg-amber-500/10 border-amber-500/20 glow-warning',
    high: 'text-rose-400 bg-rose-500/10 border-rose-500/20 glow-critical',
    critical: 'text-rose-500 bg-rose-500/10 border-rose-500/30 glow-critical animate-pulse',
    unknown: 'text-slate-400 bg-slate-500/10 border-slate-500/20',
  };

  return (
    <div className="min-h-[calc(100vh-80px)] pt-24 pb-20 px-4 max-w-6xl mx-auto">
      
      <div className="mb-8">
        <Button variant="ghost" size="sm" onClick={() => navigate('/')}>
          <ArrowLeft className="w-4 h-4 mr-2" />
          New Investigation
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        
        {/* Left Column: Trust Score & Risk Level */}
        <div className="md:col-span-1 space-y-6">
          <GlassPanel className="flex flex-col items-center justify-center p-8">
            <TrustScoreRing score={report.trust_score} />
            
            <div className={cn(
              "mt-8 flex items-center gap-3 px-6 py-3 rounded-full border",
              riskColors[report.risk_level]
            )}>
              <RiskIcon className="w-6 h-6" />
              <span className="text-lg font-bold uppercase tracking-wider">
                {report.risk_level} RISK
              </span>
            </div>
          </GlassPanel>

          {/* Threat Categories */}
          <GlassPanel>
            <h3 className="text-sm uppercase tracking-widest text-slate-400 mb-4 font-semibold">Threat Categories</h3>
            <div className="flex flex-wrap gap-2">
              {report.threat_categories.map((threat, idx) => (
                <span key={idx} className="px-3 py-1 rounded-md bg-slate-800 text-slate-300 text-sm border border-slate-700 capitalize">
                  {threat}
                </span>
              ))}
            </div>
          </GlassPanel>
        </div>

        {/* Right Column: Details & Evidence */}
        <div className="md:col-span-2 space-y-6">
          <GlassPanel>
            <h3 className="text-xl font-bold text-slate-100 mb-2">Executive Summary</h3>
            <p className="text-slate-300 leading-relaxed">
              {report.summary}
            </p>
          </GlassPanel>

          <GlassPanel>
            <h3 className="text-lg font-bold text-slate-100 mb-4 flex items-center gap-2">
              <Search className="w-5 h-5 text-slate-400" />
              Findings & Evidence
            </h3>
            <ul className="space-y-3">
              {report.findings.map((finding, idx) => (
                <li key={idx} className="flex items-start gap-3 p-3 rounded-lg bg-white/5 border border-white/5">
                  <div className="mt-1 flex-shrink-0 w-1.5 h-1.5 rounded-full bg-slate-500" />
                  <span className="text-slate-300">{finding}</span>
                </li>
              ))}
            </ul>
          </GlassPanel>

          <GlassPanel className="border-l-4 border-l-blue-500">
            <h3 className="text-lg font-bold text-slate-100 mb-4 flex items-center gap-2">
              <CheckCircle className="w-5 h-5 text-blue-400" />
              Recommendations
            </h3>
            <ul className="space-y-2">
              {report.recommendations.map((rec, idx) => (
                <li key={idx} className="flex items-center gap-3 text-slate-300">
                  <span className="text-blue-400 font-bold opacity-50">{idx + 1}.</span>
                  {rec}
                </li>
              ))}
            </ul>
          </GlassPanel>

          {report.detected_pii && report.detected_pii.length > 0 && (
            <GlassPanel className="border-amber-500/30 bg-amber-500/5">
              <h3 className="text-lg font-bold text-amber-400 mb-4 flex items-center gap-2">
                <AlertTriangle className="w-5 h-5" />
                PII Protected
              </h3>
              <p className="text-slate-300 text-sm mb-4">
                Sensitive information was detected in your submission. It was automatically redacted before further analysis to protect your privacy.
              </p>
              <div className="flex flex-wrap gap-2">
                {report.detected_pii.map((pii, idx) => (
                  <span key={idx} className="px-2 py-1 rounded bg-amber-500/20 text-amber-300 text-xs font-mono">
                    {pii.entity_type}
                  </span>
                ))}
              </div>
            </GlassPanel>
          )}

        </div>
      </div>
    </div>
  );
};
