'use client';

import React from 'react';
import { Navbar } from '@/components/layout/Navbar';
import { Footer } from '@/components/layout/Footer';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Sparkles, Image, Video, Wand2, GitBranch, BarChart2, ShieldCheck, Cpu } from 'lucide-react';

export default function FeaturesPage() {
  const features = [
    {
      title: 'FLUX.1 Text-to-Image',
      desc: '12B rectified flow transformer with 4-step rapid synthesis and leading typographical adherence.',
      icon: Image
    },
    {
      title: 'LTX-Video Synthesis',
      desc: '24fps temporal diffusion transformer supporting both text prompts and reference image animation.',
      icon: Video
    },
    {
      title: 'Image-to-Image Transformation',
      desc: 'Language-guided semantic modification via Instruct-Pix2Pix with tunable transformation strength.',
      icon: Wand2
    },
    {
      title: 'Gemini Prompt Enhancement',
      desc: 'Automated prompt expansion with camera, lighting, and negative prompt guardrail engineering.',
      icon: Sparkles
    },
    {
      title: 'Intelligent Model Router',
      desc: 'Multi-objective utility engine optimizing trade-offs between cost, latency, quality, and reliability.',
      icon: GitBranch
    },
    {
      title: 'Reproducible Benchmarks',
      desc: 'Standardized 6-domain prompt suite with percentile latency metrics and downloadable CSV/JSON reports.',
      icon: BarChart2
    }
  ];

  return (
    <div className="min-h-screen flex flex-col bg-[#0A0C10]">
      <Navbar />
      <main className="flex-1 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-32 pb-20">
        <div className="text-center mb-14">
          <Badge variant="emerald" className="mb-3">Platform Capabilities</Badge>
          <h1 className="text-3xl font-extrabold text-white">Engineered for Creative Research</h1>
          <p className="text-sm text-slate-400 mt-2 max-w-xl mx-auto">
            A comprehensive unified studio bridging state-of-the-art hosted generative models with empirical evaluation tools.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((f) => {
            const Icon = f.icon;
            return (
              <Card key={f.title} className="p-6 border-[#1E2433] bg-[#11141D]">
                <div className="w-9 h-9 rounded-lg bg-emerald-950/60 border border-emerald-800/40 flex items-center justify-center text-emerald-400 mb-4">
                  <Icon className="w-5 h-5" />
                </div>
                <h3 className="text-base font-bold text-white mb-2">{f.title}</h3>
                <p className="text-xs text-slate-400 leading-relaxed">{f.desc}</p>
              </Card>
            );
          })}
        </div>
      </main>
      <Footer />
    </div>
  );
}
