'use client';

import React, { useEffect, useState } from 'react';
import { usePathname } from 'next/navigation';
import { Menu, ShieldCheck, Activity, KeyRound, Server } from 'lucide-react';
import { apiFetch } from '@/lib/api';

interface HeaderProps {
  onOpenMobileNav?: () => void;
}

export function Header({ onOpenMobileNav }: HeaderProps) {
  const pathname = usePathname();
  const [health, setHealth] = useState<any>(null);

  useEffect(() => {
    apiFetch<any>('/health')
      .then(setHealth)
      .catch(() => setHealth({ status: 'offline' }));
  }, []);

  const getBreadcrumbTitle = (path: string) => {
    if (path === '/dashboard') return 'Studio Overview';
    if (path.startsWith('/studio/image')) return 'Text-to-Image Generation';
    if (path.startsWith('/studio/video')) return 'Video Generation';
    if (path.startsWith('/studio/edit')) return 'Image-to-Image Transformation';
    if (path.startsWith('/projects')) return 'Project Workspace';
    if (path.startsWith('/library')) return 'Media Library';
    if (path.startsWith('/history')) return 'Generation History';
    if (path.startsWith('/experiments')) return 'Controlled Research Benchmarks';
    if (path.startsWith('/usage')) return 'Usage & Cost Telemetry';
    if (path.startsWith('/settings')) return 'Preferences & Security';
    if (path.startsWith('/admin')) return 'Administration & Governance';
    return 'Studio';
  };

  const isHfActive = health?.providers_configured?.huggingface;
  const providerMode = health?.provider_mode || 'live';

  const getProviderBadge = () => {
    if (providerMode === 'offline-preview') {
      return (
        <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-teal-950/60 border border-teal-700/50 text-teal-300">
          <span className="h-2 w-2 rounded-full bg-teal-400"></span>
          <span>Offline Preview</span>
        </div>
      );
    }
    if (providerMode === 'test') {
      return (
        <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-slate-900 border border-slate-700 text-slate-300">
          <span className="h-2 w-2 rounded-full bg-slate-400"></span>
          <span>Test Fixtures</span>
        </div>
      );
    }
    // Live mode
    return (
      <div className={`flex items-center gap-2 px-2.5 py-1 rounded-lg border ${
        isHfActive ? 'bg-emerald-950/40 border-emerald-800/40 text-emerald-300' : 'bg-amber-950/40 border-amber-800/40 text-amber-300'
      }`}>
        <span className="relative flex h-2 w-2">
          <span className={`animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 ${isHfActive ? 'bg-emerald-400' : 'bg-amber-400'}`}></span>
          <span className={`relative inline-flex rounded-full h-2 w-2 ${isHfActive ? 'bg-emerald-500' : 'bg-amber-500'}`}></span>
        </span>
        <span className="hidden sm:inline">
          {isHfActive ? 'HF Live Serverless' : 'HF Token Required'}
        </span>
        <span className="sm:hidden">
          {isHfActive ? 'Live' : 'No Key'}
        </span>
      </div>
    );
  };

  return (
    <header className="h-16 border-b border-[#1E2433] bg-[#0A0C10]/90 backdrop-blur-md px-4 sm:px-6 flex items-center justify-between sticky top-0 z-30 lg:ml-64">
      <div className="flex items-center gap-3">
        {onOpenMobileNav && (
          <button
            type="button"
            onClick={onOpenMobileNav}
            aria-label="Open sidebar"
            className="lg:hidden p-2 text-slate-400 hover:text-white rounded-lg hover:bg-[#161B26] focus:outline-none focus:ring-2 focus:ring-emerald-500"
          >
            <Menu className="w-5 h-5" />
          </button>
        )}
        <h1 className="text-sm sm:text-base font-semibold text-slate-100 truncate max-w-[200px] sm:max-w-none">
          {getBreadcrumbTitle(pathname)}
        </h1>
        <span className="hidden sm:inline-block text-[11px] px-2 py-0.5 rounded-full bg-slate-800/80 text-slate-400 font-mono">
          v1.0.0
        </span>
      </div>

      <div className="flex items-center gap-3 text-xs font-mono">
        {/* Provider Live Telemetry Pill */}
        {getProviderBadge()}

        <div className="hidden md:flex items-center gap-1.5 text-slate-400">
          <Server className="w-3.5 h-3.5 text-emerald-400" />
          <span>FastAPI + SQLite/PG</span>
        </div>
      </div>
    </header>
  );
}
