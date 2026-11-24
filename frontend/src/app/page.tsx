'use client';

import React from 'react';
import Link from 'next/link';
import { Navbar } from '@/components/layout/Navbar';
import { Footer } from '@/components/layout/Footer';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import {
  Sparkles, Video, Image, Cpu, ArrowRight, CheckCircle2,
  BarChart2, ShieldCheck, Zap, Database, GitBranch
} from 'lucide-react';

export default function LandingPage() {
  return (
    <div className="min-h-screen flex flex-col bg-[#0A0C10]">
      <Navbar />

      {/* Hero Section */}
      <section className="relative pt-32 pb-20 md:pt-40 md:pb-28 overflow-hidden studio-grid border-b border-[#1E2433]">
        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-[#0A0C10]/60 to-[#0A0C10]"></div>

        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-emerald-500/30 bg-emerald-950/40 text-emerald-400 text-xs font-mono mb-6">
            <Sparkles className="w-3.5 h-3.5" />
            <span>M.Sc. IT Major Project • Research Evaluation Platform</span>
          </div>

          <h1 className="text-4xl sm:text-6xl font-extrabold text-white tracking-tight leading-tight max-w-4xl mx-auto mb-6">
            Unified Generative AI Studio & <br className="hidden sm:inline" />
            <span className="bg-gradient-to-r from-emerald-400 via-teal-300 to-cyan-400 bg-clip-text text-transparent">
              Empirical Research Engine
            </span>
          </h1>

          <p className="text-lg sm:text-xl text-slate-400 max-w-2xl mx-auto mb-10 leading-relaxed font-normal">
            Synthesize high-fidelity images and temporal videos with FLUX.1 and LTX-Video.
            Conduct reproducible benchmarks with Pareto-optimal intelligent model routing.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-16">
            <Link href="/register">
              <Button size="lg" variant="primary" className="w-full sm:w-auto text-base shadow-lg shadow-emerald-950/60">
                Launch Creative Studio <ArrowRight className="w-4 h-4 ml-1" />
              </Button>
            </Link>
            <Link href="/research">
              <Button size="lg" variant="secondary" className="w-full sm:w-auto text-base">
                Explore Thesis Benchmarks
              </Button>
            </Link>
          </div>

          {/* Interactive Feature Highlights */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 max-w-4xl mx-auto text-left">
            <div className="p-4 rounded-xl bg-[#121622]/80 border border-[#1E2538]">
              <div className="flex items-center gap-2 mb-2 text-emerald-400">
                <Image className="w-4 h-4" />
                <span className="font-semibold text-sm text-slate-200">Text-to-Image</span>
              </div>
              <p className="text-xs text-slate-400">FLUX.1 [schnell] & SDXL Base at 1024px with seed control.</p>
            </div>

            <div className="p-4 rounded-xl bg-[#121622]/80 border border-[#1E2538]">
              <div className="flex items-center gap-2 mb-2 text-teal-400">
                <Video className="w-4 h-4" />
                <span className="font-semibold text-sm text-slate-200">Text & Img-to-Video</span>
              </div>
              <p className="text-xs text-slate-400">LTX-Video Diffusion Transformer with verified MP4 delivery.</p>
            </div>

            <div className="p-4 rounded-xl bg-[#121622]/80 border border-[#1E2538]">
              <div className="flex items-center gap-2 mb-2 text-cyan-400">
                <GitBranch className="w-4 h-4" />
                <span className="font-semibold text-sm text-slate-200">Intelligent Router</span>
              </div>
              <p className="text-xs text-slate-400">Multi-objective utility engine balancing cost, latency, and quality.</p>
            </div>

            <div className="p-4 rounded-xl bg-[#121622]/80 border border-[#1E2538]">
              <div className="flex items-center gap-2 mb-2 text-amber-400">
                <BarChart2 className="w-4 h-4" />
                <span className="font-semibold text-sm text-slate-200">Reproducible Tests</span>
              </div>
              <p className="text-xs text-slate-400">6-domain prompt benchmark dataset with CSV/JSON exports.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Model Capabilities & Rate Card Section */}
      <section className="py-20 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-14">
          <Badge variant="emerald" className="mb-3">Hosted Inference Architecture</Badge>
          <h2 className="text-3xl font-bold text-white tracking-tight">Verified Production AI Models</h2>
          <p className="text-slate-400 text-sm max-w-xl mx-auto mt-2">
            No local GPU requirements. Hosted serverless inference APIs with transparent telemetry.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="p-6 rounded-xl bg-[#11141D] border border-[#1E2433] hover:border-emerald-500/40 transition-all">
            <div className="flex items-center justify-between mb-4">
              <span className="text-xs font-mono text-emerald-400 bg-emerald-950/60 px-2 py-0.5 rounded border border-emerald-800/40">IMAGE GENERATION</span>
              <span className="text-xs text-slate-400 font-mono">$0.003 / gen</span>
            </div>
            <h3 className="text-lg font-bold text-white mb-2">FLUX.1 [schnell]</h3>
            <p className="text-xs text-slate-400 mb-5 leading-relaxed">
              Black Forest Labs 12B parameter rectified flow transformer. 4-step ultra-fast synthesis with extraordinary text typography adherence.
            </p>
            <div className="border-t border-[#1E2433] pt-4 text-xs font-mono text-slate-400 space-y-1.5">
              <div className="flex justify-between"><span>Max Resolution:</span><span className="text-slate-200">1024x1024</span></div>
              <div className="flex justify-between"><span>License:</span><span className="text-slate-200">Apache 2.0</span></div>
              <div className="flex justify-between"><span>P90 Latency:</span><span className="text-emerald-400">1.4s</span></div>
            </div>
          </div>

          <div className="p-6 rounded-xl bg-[#11141D] border border-[#1E2433] hover:border-teal-500/40 transition-all">
            <div className="flex items-center justify-between mb-4">
              <span className="text-xs font-mono text-teal-400 bg-teal-950/60 px-2 py-0.5 rounded border border-teal-800/40">VIDEO SYNTHESIS</span>
              <span className="text-xs text-slate-400 font-mono">$0.045 / gen</span>
            </div>
            <h3 className="text-lg font-bold text-white mb-2">LTX-Video (DiT)</h3>
            <p className="text-xs text-slate-400 mb-5 leading-relaxed">
              Lightricks real-time video latent diffusion transformer. Produces 24fps high-coherence cinematic sequences from text and reference images.
            </p>
            <div className="border-t border-[#1E2433] pt-4 text-xs font-mono text-slate-400 space-y-1.5">
              <div className="flex justify-between"><span>Frame Rate:</span><span className="text-slate-200">24 FPS</span></div>
              <div className="flex justify-between"><span>Max Duration:</span><span className="text-slate-200">10.0 Seconds</span></div>
              <div className="flex justify-between"><span>Async Queue:</span><span className="text-teal-400">Enabled</span></div>
            </div>
          </div>

          <div className="p-6 rounded-xl bg-[#11141D] border border-[#1E2433] hover:border-cyan-500/40 transition-all">
            <div className="flex items-center justify-between mb-4">
              <span className="text-xs font-mono text-cyan-400 bg-cyan-950/60 px-2 py-0.5 rounded border border-cyan-800/40">PROMPT REFINEMENT</span>
              <span className="text-xs text-slate-400 font-mono">$0.0001 / call</span>
            </div>
            <h3 className="text-lg font-bold text-white mb-2">Gemini 2.0 Flash</h3>
            <p className="text-xs text-slate-400 mb-5 leading-relaxed">
              Domain-adapted visual descriptor engineering. Expands lighting, lens dynamics, and constructs automatic negative guardrails.
            </p>
            <div className="border-t border-[#1E2433] pt-4 text-xs font-mono text-slate-400 space-y-1.5">
              <div className="flex justify-between"><span>Context Budget:</span><span className="text-slate-200">1000 Tokens</span></div>
              <div className="flex justify-between"><span>Latency:</span><span className="text-emerald-400">&lt; 350ms</span></div>
              <div className="flex justify-between"><span>Fallback:</span><span className="text-slate-200">Heuristic Engine</span></div>
            </div>
          </div>
        </div>
      </section>

      {/* Academic Methodology Callout */}
      <section className="py-16 bg-[#0E1119] border-y border-[#1E2433]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row items-center justify-between gap-8">
          <div>
            <h3 className="text-2xl font-bold text-white mb-2">Academic Research Contribution</h3>
            <p className="text-sm text-slate-400 max-w-2xl leading-relaxed">
              Major Project Thesis: &quot;Comparative Evaluation and Intelligent Routing of Hosted Generative AI Models
              for Text-to-Image and Image-to-Video Synthesis.&quot; Includes empirical validation datasets and viva defense materials.
            </p>
          </div>
          <Link href="/research">
            <Button variant="outline" size="lg" className="whitespace-nowrap">
              Review Evaluation Protocol
            </Button>
          </Link>
        </div>
      </section>

      <Footer />
    </div>
  );
}
