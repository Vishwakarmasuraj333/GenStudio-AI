'use client';

import React from 'react';
import { Navbar } from '@/components/layout/Navbar';
import { Footer } from '@/components/layout/Footer';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { BookOpen, FileText, CheckCircle2, GitBranch, BarChart3, Database } from 'lucide-react';

export default function ResearchPublicPage() {
  return (
    <div className="min-h-screen flex flex-col bg-[#0A0C10]">
      <Navbar />
      <main className="flex-1 max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 pt-32 pb-20 space-y-12">
        {/* Header */}
        <div className="text-center space-y-3">
          <Badge variant="emerald">M.Sc. Information Technology Major Project Thesis</Badge>
          <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight leading-tight">
            Comparative Evaluation and Intelligent Routing of Hosted Generative AI Models for Text-to-Image and Image-to-Video Synthesis
          </h1>
          <p className="text-xs font-mono text-slate-400">
            Candidate: Suraj | Academic Evaluation • Defense Version 1.0.0
          </p>
        </div>

        {/* Abstract */}
        <Card className="p-8 border-[#1E2433] bg-[#0E121B] space-y-4">
          <h2 className="text-base font-bold text-white flex items-center gap-2">
            <BookOpen className="w-4 h-4 text-emerald-400" /> Executive Abstract
          </h2>
          <p className="text-xs sm:text-sm text-slate-300 leading-relaxed font-serif">
            Recent breakthroughs in rectified flow transformers (FLUX.1) and temporal diffusion transformers (LTX-Video)
            have significantly advanced synthetic visual fidelity. However, deploying multi-modal creative workflows
            on standard non-GPU client workstations presents substantial cost, latency, and consistency challenges.
            This project designs and implements <strong>GenStudio AI</strong>, a full-stack research platform integrating
            hosted serverless inference APIs, reproducible benchmarking harnesses, and a multi-objective intelligent model routing policy.
          </p>
        </Card>

        {/* Core Methodological Contributions */}
        <div className="space-y-4">
          <h3 className="text-lg font-bold text-white">Research Methodology & Systematic Protocol</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Card className="p-5 border-[#1E2433]">
              <div className="text-emerald-400 font-bold text-sm mb-2">1. Fixed Benchmark Dataset</div>
              <p className="text-xs text-slate-400 leading-relaxed">
                Standardized 6-domain prompt suite (photorealism, spatial composition, typography, cinematic aesthetics, artistic rendering, motion dynamics).
              </p>
            </Card>

            <Card className="p-5 border-[#1E2433]">
              <div className="text-teal-400 font-bold text-sm mb-2">2. Statistical Metrics</div>
              <p className="text-xs text-slate-400 leading-relaxed">
                Rigorous percentile latency (median, p90, p95), cost per successful generation (CPS), normalized semantic alignment, and optical-flow temporal consistency.
              </p>
            </Card>

            <Card className="p-5 border-[#1E2433]">
              <div className="text-cyan-400 font-bold text-sm mb-2">3. Intelligent Model Router</div>
              <p className="text-xs text-slate-400 leading-relaxed">
                Pareto-optimal multi-objective decision policy balancing hard budget constraints, latency thresholds, and historical success telemetry.
              </p>
            </Card>
          </div>
        </div>

        {/* Benchmarking Dataset Specification */}
        <Card className="p-6 border-[#1E2433] space-y-4">
          <h3 className="text-base font-bold text-white">Prompt Benchmark Domains</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs font-mono">
              <thead className="border-b border-[#1E2433] text-slate-400">
                <tr>
                  <th className="pb-3">Domain Category</th>
                  <th className="pb-3">Challenge Evaluated</th>
                  <th className="pb-3">Target Difficulty</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#1E2433] text-slate-300">
                <tr><td className="py-2.5 text-emerald-400">Photorealism</td><td>Micro-texture, skin porosity, volumetric lighting</td><td>Medium</td></tr>
                <tr><td className="py-2.5 text-teal-400">Spatial Composition</td><td>Occlusion, left/right positional adherence</td><td>High</td></tr>
                <tr><td className="py-2.5 text-cyan-400">Typography & Text</td><td>Spelling accuracy, letter spacing, font rendering</td><td>Very High</td></tr>
                <tr><td className="py-2.5 text-amber-400">Cinematic Aesthetics</td><td>Anamorphic lenses, depth of field, color grading</td><td>Medium</td></tr>
                <tr><td className="py-2.5 text-rose-400">Motion Dynamics</td><td>Camera pan coherence, fluid droplet motion in video</td><td>High</td></tr>
              </tbody>
            </table>
          </div>
        </Card>

        {/* Reproducibility and Honesty Statement */}
        <div className="p-6 rounded-xl border border-emerald-500/20 bg-emerald-950/20 text-xs text-slate-300 space-y-2">
          <div className="flex items-center gap-2 font-bold text-emerald-400">
            <CheckCircle2 className="w-4 h-4" /> Academic Honesty & Verification Standard
          </div>
          <p className="leading-relaxed">
            All experimental numbers presented in this platform are generated strictly from recorded empirical database records.
            When live provider credentials are unconfigured, tests run in deterministic test fixture mode and are explicitly flagged
            in the database metadata as simulated runs. No benchmark values, training claims, or accuracy results are fabricated.
          </p>
        </div>
      </main>
      <Footer />
    </div>
  );
}
