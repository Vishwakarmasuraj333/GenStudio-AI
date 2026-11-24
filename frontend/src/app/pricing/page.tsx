'use client';

import React from 'react';
import { Navbar } from '@/components/layout/Navbar';
import { Footer } from '@/components/layout/Footer';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';

export default function PricingPage() {
  const tiers = [
    {
      name: 'FLUX.1 [schnell]',
      task: 'Text-to-Image',
      cost: '$0.003',
      unit: 'per 1024x1024 output',
      specs: ['4 Inference Steps', 'Apache 2.0 License', 'P50 Latency: ~1.2s', 'Serverless Warm Endpoint']
    },
    {
      name: 'SDXL 1.0 Base',
      task: 'Text-to-Image',
      cost: '$0.006',
      unit: 'per 1024x1024 output',
      specs: ['30 Inference Steps', 'OpenRAIL++ License', 'P50 Latency: ~3.2s', 'Negative Prompt Support']
    },
    {
      name: 'InstructPix2Pix',
      task: 'Image Editing',
      cost: '$0.005',
      unit: 'per 512x512 edit',
      specs: ['Image Transformation', 'Controllable Strength', 'Semantic Instruction', 'Fast Turnaround']
    },
    {
      name: 'LTX-Video (DiT)',
      task: 'Text & Img to Video',
      cost: '$0.045',
      unit: 'per 5-second 24fps MP4',
      specs: ['Diffusion Transformer', '24 Frames Per Second', 'Async Background Worker', 'Verified MP4 Container']
    },
    {
      name: 'Wan2.1 14B Video',
      task: 'High-Fidelity Video',
      cost: '$0.080',
      unit: 'per 5-second 16fps MP4',
      specs: ['14B Parameters', 'High Temporal Coherence', 'Requires Dedicated Worker', 'Long-running Job']
    },
    {
      name: 'Gemini 2.0 Flash',
      task: 'Prompt Refinement',
      cost: '$0.0001',
      unit: 'per prompt expansion',
      specs: ['1000 Token Context', 'Negative Prompt Extraction', 'Style Descriptors', 'Sub-second Latency']
    }
  ];

  return (
    <div className="min-h-screen flex flex-col bg-[#0A0C10]">
      <Navbar />
      <main className="flex-1 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-32 pb-20">
        <div className="text-center mb-12">
          <Badge variant="emerald" className="mb-3">Inference Cost Accounting</Badge>
          <h1 className="text-3xl font-extrabold text-white">Transparent Provider Rate Cards</h1>
          <p className="text-sm text-slate-400 mt-2 max-w-xl mx-auto">
            GenStudio AI passes through exact serverless inference costs with zero hidden markups.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {tiers.map((t) => (
            <Card key={t.name} className="p-6 border-[#1E2433] bg-[#11141D] flex flex-col justify-between">
              <div>
                <Badge variant="teal" className="mb-3">{t.task}</Badge>
                <h3 className="text-lg font-bold text-white mb-2">{t.name}</h3>
                <div className="flex items-baseline gap-1 mb-4">
                  <span className="text-3xl font-extrabold font-mono text-emerald-400">{t.cost}</span>
                  <span className="text-xs text-slate-500 font-mono">{t.unit}</span>
                </div>
                <ul className="space-y-2 border-t border-[#1E2433] pt-4 text-xs text-slate-300">
                  {t.specs.map((s, idx) => (
                    <li key={idx} className="flex items-center gap-2">
                      <span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
                      <span>{s}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </Card>
          ))}
        </div>
      </main>
      <Footer />
    </div>
  );
}
