'use client';

import React from 'react';
import { Navbar } from '@/components/layout/Navbar';
import { Footer } from '@/components/layout/Footer';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';

export default function ModelsPublicPage() {
  const models = [
    {
      name: 'FLUX.1 [schnell]',
      id: 'black-forest-labs/FLUX.1-schnell',
      provider: 'Hugging Face',
      type: 'Text-to-Image',
      steps: 4,
      cost: '$0.003 / generation',
      resolution: '1024x1024',
      license: 'Apache-2.0',
      description: 'Next-generation 12-billion parameter rectified flow diffusion model by Black Forest Labs.'
    },
    {
      name: 'Stable Diffusion XL 1.0',
      id: 'stabilityai/stable-diffusion-xl-base-1.0',
      provider: 'Hugging Face',
      type: 'Text-to-Image',
      steps: 30,
      cost: '$0.006 / generation',
      resolution: '1024x1024',
      license: 'OpenRAIL++',
      description: 'Production-tested latent diffusion model with multi-aspect ratio rendering.'
    },
    {
      name: 'LTX-Video (DiT)',
      id: 'Lightricks/LTX-Video',
      provider: 'Hugging Face',
      type: 'Text & Image to Video',
      steps: '25-50',
      cost: '$0.045 / generation',
      resolution: '1280x720',
      license: 'Apache-2.0',
      description: 'Lightricks real-time video diffusion transformer producing temporal motion sequences.'
    },
    {
      name: 'InstructPix2Pix',
      id: 'timbrooks/instruct-pix2pix',
      provider: 'Hugging Face',
      type: 'Image-to-Image',
      steps: 20,
      cost: '$0.005 / generation',
      resolution: '512x512',
      license: 'CreativeML OpenRAIL-M',
      description: 'Language-guided image editing with controllable transformation strength.'
    },
    {
      name: 'Gemini 2.0 Flash',
      id: 'gemini-2.0-flash',
      provider: 'Google AI Studio',
      type: 'Prompt Refinement',
      steps: 'N/A',
      cost: '$0.0001 / query',
      resolution: 'N/A',
      license: 'Commercial API',
      description: 'Automated prompt expansion and negative prompt generation.'
    }
  ];

  return (
    <div className="min-h-screen flex flex-col bg-[#0A0C10]">
      <Navbar />
      <main className="flex-1 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-32 pb-20">
        <div className="text-center mb-12">
          <Badge variant="emerald" className="mb-3">Verified Model Registry</Badge>
          <h1 className="text-3xl font-extrabold text-white">AI Model Rate Card & Specifications</h1>
          <p className="text-sm text-slate-400 mt-2 max-w-xl mx-auto">
            Honest specifications, verifiable pricing rate cards, and exact task capabilities.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {models.map((m) => (
            <Card key={m.id} className="p-6 border-[#1E2433] bg-[#11141D] flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between mb-3">
                  <Badge variant="teal">{m.type}</Badge>
                  <span className="text-xs font-mono text-emerald-400">{m.cost}</span>
                </div>
                <h3 className="text-base font-bold text-white mb-1">{m.name}</h3>
                <p className="text-[11px] font-mono text-slate-500 mb-3">{m.id}</p>
                <p className="text-xs text-slate-400 leading-relaxed mb-4">{m.description}</p>
              </div>

              <div className="border-t border-[#1E2433] pt-3 text-[11px] font-mono text-slate-400 space-y-1">
                <div className="flex justify-between"><span>Provider:</span><span className="text-slate-200">{m.provider}</span></div>
                <div className="flex justify-between"><span>Max Resolution:</span><span className="text-slate-200">{m.resolution}</span></div>
                <div className="flex justify-between"><span>License:</span><span className="text-slate-200">{m.license}</span></div>
              </div>
            </Card>
          ))}
        </div>
      </main>
      <Footer />
    </div>
  );
}
