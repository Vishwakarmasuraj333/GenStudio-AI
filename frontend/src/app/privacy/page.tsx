'use client';

import React from 'react';
import { Navbar } from '@/components/layout/Navbar';
import { Footer } from '@/components/layout/Footer';
import { Card } from '@/components/ui/Card';

export default function PrivacyPage() {
  return (
    <div className="min-h-screen flex flex-col bg-[#0A0C10]">
      <Navbar />
      <main className="flex-1 max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 pt-32 pb-20 space-y-8 text-xs leading-relaxed text-slate-300">
        <h1 className="text-2xl font-bold text-white">Privacy Disclosures & Data Handling Policy</h1>

        <Card className="p-6 border-[#1E2433] bg-[#0E121B] space-y-4">
          <h2 className="text-sm font-bold text-white">1. External Inference Provider Disclosure</h2>
          <p>
            GenStudio AI utilizes hosted third-party inference endpoints (such as Hugging Face Inference Providers and Google AI Studio).
            When you submit an image or video generation request, your text prompt and any uploaded reference image files are transmitted
            to the designated model provider for compute execution.
          </p>
        </Card>

        <Card className="p-6 border-[#1E2433] bg-[#0E121B] space-y-4">
          <h2 className="text-sm font-bold text-white">2. Secret and Credential Isolation</h2>
          <p>
            API keys and tokens for AI providers are stored strictly in server-side environment variables and are never transmitted to client
            browser sessions, embedded in web bundles, or logged in client audit files.
          </p>
        </Card>

        <Card className="p-6 border-[#1E2433] bg-[#0E121B] space-y-4">
          <h2 className="text-sm font-bold text-white">3. Media Asset Storage & Retention</h2>
          <p>
            Generated images and videos are persisted in secure local object storage with SHA256 integrity checksums. Users maintain full ownership
            and deletion privileges over their generated assets. Deleting an asset removes both the database reference and physical disk bytes.
          </p>
        </Card>
      </main>
      <Footer />
    </div>
  );
}
