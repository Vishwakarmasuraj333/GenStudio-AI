import React from 'react';
import Link from 'next/link';
import { Sparkles, BookOpen, ShieldCheck } from 'lucide-react';

export function Footer() {
  return (
    <footer className="border-t border-[#1E2433] bg-[#07090D] text-slate-400 text-sm py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-10">
          <div className="space-y-3">
            <div className="flex items-center gap-2.5">
              <div className="w-7 h-7 rounded-md bg-emerald-600 flex items-center justify-center text-white">
                <Sparkles className="w-4 h-4" />
              </div>
              <span className="font-bold text-white tracking-tight">GenStudio AI</span>
            </div>
            <p className="text-xs text-slate-500 leading-relaxed">
              Advanced generative AI research studio for image and video synthesis.
              Built as an academic major project for verifiable benchmark evaluation.
            </p>
          </div>

          <div>
            <h4 className="text-xs font-semibold text-slate-200 uppercase tracking-wider mb-3">Capabilities</h4>
            <ul className="space-y-2 text-xs">
              <li><Link href="/studio/image" className="hover:text-emerald-400 transition-colors">FLUX.1 Text-to-Image</Link></li>
              <li><Link href="/studio/video" className="hover:text-emerald-400 transition-colors">LTX-Video Text-to-Video</Link></li>
              <li><Link href="/studio/edit" className="hover:text-emerald-400 transition-colors">InstructPix2Pix Image Edit</Link></li>
              <li><Link href="/models" className="hover:text-emerald-400 transition-colors">Curated Model Registry</Link></li>
            </ul>
          </div>

          <div>
            <h4 className="text-xs font-semibold text-slate-200 uppercase tracking-wider mb-3">Academic Research</h4>
            <ul className="space-y-2 text-xs">
              <li><Link href="/research" className="hover:text-emerald-400 transition-colors">Thesis Methodology</Link></li>
              <li><Link href="/experiments" className="hover:text-emerald-400 transition-colors">Standard Prompt Benchmark</Link></li>
              <li><Link href="/pricing" className="hover:text-emerald-400 transition-colors">Inference Cost Rate Card</Link></li>
              <li><a href="/docs/VIVA_QUESTIONS_AND_ANSWERS.md" className="hover:text-emerald-400 transition-colors">Viva Defense Guide</a></li>
            </ul>
          </div>

          <div>
            <h4 className="text-xs font-semibold text-slate-200 uppercase tracking-wider mb-3">Governance</h4>
            <ul className="space-y-2 text-xs">
              <li><Link href="/privacy" className="hover:text-emerald-400 transition-colors">Privacy & Data Disclosures</Link></li>
              <li><Link href="/terms" className="hover:text-emerald-400 transition-colors">Terms of Academic Use</Link></li>
              <li><span className="text-slate-500">M.Sc. IT Major Project Evaluation</span></li>
            </ul>
          </div>
        </div>

        <div className="border-t border-[#1E2433] pt-6 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-500">
          <p>© 2026 GenStudio AI. All research metrics generated from recorded empirical observations.</p>
          <div className="flex items-center gap-4 mt-3 sm:mt-0 font-mono">
            <span>Next.js 14</span>
            <span>•</span>
            <span>FastAPI</span>
            <span>•</span>
            <span>Hugging Face</span>
          </div>
        </div>
      </div>
    </footer>
  );
}
