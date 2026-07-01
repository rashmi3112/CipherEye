import React from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { InputSelector } from '../components/input/InputSelector';
import type { InputType } from '../components/input/InputSelector';
import { Shield, Eye, Lock, FileText, Globe, AlertTriangle, Layers } from 'lucide-react';

export const Home: React.FC = () => {
  const navigate = useNavigate();

  const handleInvestigationSubmit = (type: InputType, payload: string | File) => {
    // Transition to the Analyze page, passing the payload via state.
    navigate('/analyze', { state: { type, payload } });
  };

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: { staggerChildren: 0.1 }
    }
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.6, ease: "easeOut" } }
  };

  const agentCards = [
    {
      icon: <Lock className="w-5 h-5 text-emerald-400" />,
      title: "PII Protection Agent",
      description: "Our privacy shield. Scans inputs offline using Presidio to detect and redact sensitive data (SSNs, cards, phones) before anything is sent to LLMs."
    },
    {
      icon: <FileText className="w-5 h-5 text-cyan-400" />,
      title: "Text & Email Agent",
      description: "Analyzes message contents, emails, and SMS for patterns of social engineering, urgent time pressure, typosquatting, and phishing indicators."
    },
    {
      icon: <Globe className="w-5 h-5 text-blue-400" />,
      title: "URL Scanner Agent",
      description: "Inspects links and domains for redirection tricks, typosquatting patterns, blacklisted hosts, and domain registration age threats."
    },
    {
      icon: <AlertTriangle className="w-5 h-5 text-amber-400" />,
      title: "Threat Assessor Agent",
      description: "Aggregates findings from all individual scanners, calculates safety ratings, consolidated risk vectors, and assigns the final Trust Score."
    },
    {
      icon: <Layers className="w-5 h-5 text-purple-400" />,
      title: "Report Generator Agent",
      description: "Synthesizes raw threat telemetry into readable executive summaries and actionable security recommendations for the end user."
    }
  ];

  return (
    <div className="flex flex-col items-center px-4 relative w-full">
      
      {/* First Fold: Hero & Input */}
      <div className="min-h-[calc(100vh-80px)] flex flex-col items-center justify-center w-full max-w-4xl py-12">
        <motion.div 
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: "easeOut" }}
          className="text-center mb-12 max-w-2xl"
        >
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-sm font-medium mb-6">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
            </span>
            Agents Online
          </div>
          
          <h2 className="text-5xl md:text-7xl font-bold tracking-tight text-white mb-6">
            Verify Before <br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-cyan-400">
              You Trust.
            </span>
          </h2>
          
          <p className="text-lg text-slate-400 leading-relaxed">
            CipherEye utilizes an orchestrated fleet of specialized AI Agents to analyze links, messages, and files for cyber threats before you interact with them.
          </p>
        </motion.div>

        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.2, ease: "easeOut" }}
          className="w-full"
        >
          <InputSelector onSubmit={handleInvestigationSubmit} />
        </motion.div>
      </div>

      {/* Second Fold: About Section */}
      <div className="w-full max-w-5xl py-20 border-t border-white/5">
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center mb-16"
        >
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-sm font-medium mb-6">
            About CipherEye
          </div>
          <h3 className="text-3xl md:text-4xl font-bold tracking-tight text-white mb-6">
            Multi-Agent Threat Intelligence
          </h3>
          <p className="text-base text-slate-400 leading-relaxed max-w-3xl mx-auto">
            CipherEye protects you from modern digital scams by running orchestrated analysis swarms. It intercepts suspect links, documents, and messages and processes them through customized scanners.
          </p>
        </motion.div>

        {/* Feature Highlights */}
        <motion.div 
          variants={containerVariants}
          initial="hidden"
          animate="visible"
          className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-20"
        >
          <motion.div 
            variants={itemVariants}
            className="p-8 rounded-2xl bg-white/[0.02] border border-white/5 flex gap-4 hover:border-emerald-500/20 transition-all duration-300 group"
          >
            <div className="p-3 h-fit rounded-lg bg-emerald-500/10 text-emerald-400 group-hover:bg-emerald-500/20 transition-colors">
              <Shield className="w-6 h-6" />
            </div>
            <div>
              <h4 className="text-lg font-semibold text-slate-100 mb-2">Privacy-First Architecture</h4>
              <p className="text-sm text-slate-400 leading-relaxed">
                Your credentials and sensitive details remain private. Scanners run on redacted content masks to protect personal data before external processing.
              </p>
            </div>
          </motion.div>

          <motion.div 
            variants={itemVariants}
            className="p-8 rounded-2xl bg-white/[0.02] border border-white/5 flex gap-4 hover:border-cyan-500/20 transition-all duration-300 group"
          >
            <div className="p-3 h-fit rounded-lg bg-cyan-500/10 text-cyan-400 group-hover:bg-cyan-500/20 transition-colors">
              <Eye className="w-6 h-6" />
            </div>
            <div>
              <h4 className="text-lg font-semibold text-slate-100 mb-2">Orchestration & Swarms</h4>
              <p className="text-sm text-slate-400 leading-relaxed">
                Rather than treating all threats with the same logic, specialized sub-agents coordinate analysis to target malicious indicators in every distinct text type.
              </p>
            </div>
          </motion.div>
        </motion.div>

        {/* Meet the Swarm */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.8 }}
        >
          <h4 className="text-xl font-bold tracking-tight text-white mb-8 text-center flex items-center justify-center gap-3">
            Meet the Swarm
          </h4>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {agentCards.map((agent, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 15 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                className="p-6 rounded-2xl bg-white/[0.01] border border-white/5 flex flex-col gap-4 hover:border-white/10 hover:bg-white/[0.02] transition-all duration-300"
              >
                <div className="p-2.5 w-fit rounded-lg bg-white/[0.03]">
                  {agent.icon}
                </div>
                <div>
                  <h5 className="text-sm font-bold text-slate-100 mb-1">{agent.title}</h5>
                  <p className="text-xs text-slate-400 leading-relaxed">{agent.description}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>

    </div>
  );
};
