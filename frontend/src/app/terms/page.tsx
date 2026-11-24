'use client';

import React from 'react';
import { Navbar } from '@/components/layout/Navbar';
import { Footer } from '@/components/layout/Footer';
import { Card } from '@/components/ui/Card';

export default function TermsPage() {
  return (
    <div className="min-h-screen flex flex-col bg-[#0A0C10]">
      <Navbar />
      <main className="flex-1 max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 pt-32 pb-20 space-y-8 text-xs leading-relaxed text-slate-300">
        <h1 className="text-2xl font-bold text-white">Terms of Academic Use & Model Licensing</h1>

        <Card className="p-6 border-[#1E2433] bg-[#0E121B] space-y-4">
          <h2 className="text-sm font-bold text-white">1. Academic & Research Scope</h2>
          <p>
            GenStudio AI is an original M.Sc. IT Major Project designed for academic evaluation, empirical benchmarks, and viva defense demonstrations.
            Users agree to abide by ethical AI generative practices and applicable model licenses (Apache-2.0, OpenRAIL++).
          </p>
        </Card>

        <Card className="p-6 border-[#1E2433] bg-[#0E121B] space-y-4">
          <h2 className="text-sm font-bold text-white">2. Permissible Content</h2>
          <p>
            Users may not submit prompts intended to generate defamatory, abusive, or harmful material. Requests are subject to provider-level moderation filters.
          </p>
        </Card>
      </main>
      <Footer />
    </div>
  );
}
