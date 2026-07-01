import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Link2, FileText, UploadCloud, Search } from 'lucide-react';
import { GlassPanel } from '../core/GlassPanel';
import { Button } from '../core/Button';
import { Input } from '../core/Input';
import { cn } from '../../utils/cn';

export type InputType = 'url' | 'text' | 'file';

interface InputSelectorProps {
  onSubmit: (type: InputType, payload: string | File) => void;
  isLoading?: boolean;
}

export const InputSelector: React.FC<InputSelectorProps> = ({ onSubmit, isLoading }) => {
  const [activeTab, setActiveTab] = useState<InputType>('url');
  const [urlValue, setUrlValue] = useState('');
  const [textValue, setTextValue] = useState('');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (activeTab === 'url' && urlValue) onSubmit('url', urlValue);
    if (activeTab === 'text' && textValue) onSubmit('text', textValue);
    if (activeTab === 'file' && selectedFile) onSubmit('file', selectedFile);
  };

  const tabs = [
    { id: 'url', label: 'URL / Link', icon: <Link2 className="w-4 h-4" /> },
    { id: 'text', label: 'Text / Email', icon: <FileText className="w-4 h-4" /> },
    { id: 'file', label: 'Document / Media', icon: <UploadCloud className="w-4 h-4" /> },
  ];

  return (
    <GlassPanel className="w-full max-w-3xl mx-auto p-2">
      {/* Tab Navigation */}
      <div className="flex gap-2 p-2 bg-black/20 rounded-lg mb-6">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            type="button"
            onClick={() => setActiveTab(tab.id as InputType)}
            className={cn(
              "flex-1 flex items-center justify-center gap-2 py-3 px-4 rounded-md text-sm font-medium transition-all relative",
              activeTab === tab.id ? "text-emerald-400" : "text-slate-400 hover:text-slate-200"
            )}
          >
            {activeTab === tab.id && (
              <motion.div
                layoutId="active-tab"
                className="absolute inset-0 bg-emerald-500/10 border border-emerald-500/20 rounded-md"
                transition={{ type: "spring", bounce: 0.2, duration: 0.6 }}
              />
            )}
            <span className="relative z-10 flex items-center gap-2">
              {tab.icon}
              {tab.label}
            </span>
          </button>
        ))}
      </div>

      {/* Input Area */}
      <form onSubmit={handleSubmit} className="px-4 pb-4">
        <AnimatePresence mode="wait">
          {activeTab === 'url' && (
            <motion.div
              key="url"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="flex flex-col gap-4"
            >
              <Input
                type="url"
                placeholder="Enter a suspicious URL (e.g., https://secure-login-update.com)"
                value={urlValue}
                onChange={(e) => setUrlValue(e.target.value)}
                icon={<Link2 className="w-5 h-5" />}
                required
              />
            </motion.div>
          )}

          {activeTab === 'text' && (
            <motion.div
              key="text"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="flex flex-col gap-4"
            >
              <textarea
                placeholder="Paste the suspicious email, message, or text here..."
                value={textValue}
                onChange={(e) => setTextValue(e.target.value)}
                required
                className="w-full h-32 bg-slate-900/50 border border-white/10 rounded-lg p-4 text-slate-200 placeholder:text-slate-500 focus:outline-none focus:border-emerald-500/50 focus:ring-1 focus:ring-emerald-500/50 transition-all resize-none"
              />
            </motion.div>
          )}

          {activeTab === 'file' && (
            <motion.div
              key="file"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="flex flex-col items-center justify-center h-32 border-2 border-dashed border-white/10 rounded-lg hover:border-emerald-500/50 hover:bg-emerald-500/5 transition-all cursor-pointer relative"
            >
              <input
                type="file"
                className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                onChange={(e) => setSelectedFile(e.target.files?.[0] || null)}
              />
              <UploadCloud className="w-8 h-8 text-slate-400 mb-2" />
              <p className="text-sm text-slate-300">
                {selectedFile ? selectedFile.name : "Drag & drop a file, or click to browse"}
              </p>
              <p className="text-xs text-slate-500 mt-1">Supports Images, PDFs, Audio, Video</p>
            </motion.div>
          )}
        </AnimatePresence>

        <div className="mt-8 flex justify-end">
          <Button type="submit" size="lg" isLoading={isLoading} className="w-full sm:w-auto min-w-[200px]">
            <Search className="w-5 h-5 mr-2" />
            Start Investigation
          </Button>
        </div>
      </form>
    </GlassPanel>
  );
};
