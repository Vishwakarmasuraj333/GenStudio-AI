'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { apiFetch } from '@/lib/api';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import {
  Sparkles, Image as ImageIcon, Video, FolderKanban,
  CheckCircle2, AlertTriangle, ArrowUpRight, TrendingUp,
  Clock, DollarSign
} from 'lucide-react';

export default function DashboardPage() {
  const [summary, setSummary] = useState<any>(null);
  const [projects, setProjects] = useState<any[]>([]);
  const [recentJobs, setRecentJobs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      apiFetch<any>('/usage/summary').catch(() => null),
      apiFetch<any[]>('/projects/').catch(() => []),
      apiFetch<any[]>('/history/?limit=5').catch(() => [])
    ]).then(([sumData, projData, histData]) => {
      setSummary(sumData);
      setProjects(projData);
      setRecentJobs(histData);
      setLoading(false);
    });
  }, []);

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      {/* Welcome Banner */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-6 rounded-2xl bg-gradient-to-r from-[#121622] via-[#10141F] to-[#0D1017] border border-[#1E2538]">
        <div>
          <h2 className="text-xl font-bold text-white mb-1">Creative Research Studio</h2>
          <p className="text-xs text-slate-400">
            Generate high-resolution media, run benchmark evaluations, and track inference compute costs in real time.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Link href="/studio/image">
            <Button size="sm" variant="primary">
              <ImageIcon className="w-3.5 h-3.5 mr-1.5" /> Text to Image
            </Button>
          </Link>
          <Link href="/studio/video">
            <Button size="sm" variant="secondary">
              <Video className="w-3.5 h-3.5 mr-1.5" /> Text to Video
            </Button>
          </Link>
        </div>
      </div>

      {/* Telemetry Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="p-5 border-[#1E2433]">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-medium">Total Generations</span>
            <Sparkles className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-2xl font-bold text-white font-mono">
            {loading ? '...' : (summary?.total_generations || 0)}
          </div>
          <div className="text-[11px] text-slate-500 mt-1">Real database records</div>
        </Card>

        <Card className="p-5 border-[#1E2433]">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-medium">Successful Jobs</span>
            <CheckCircle2 className="w-4 h-4 text-teal-400" />
          </div>
          <div className="text-2xl font-bold text-teal-300 font-mono">
            {loading ? '...' : (summary?.successful_generations || 0)}
          </div>
          <div className="text-[11px] text-slate-500 mt-1">
            {summary?.total_generations ? `${Math.round((summary.successful_generations / summary.total_generations) * 100)}% success rate` : 'No runs yet'}
          </div>
        </Card>

        <Card className="p-5 border-[#1E2433]">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-medium">Incurred Cost</span>
            <DollarSign className="w-4 h-4 text-amber-400" />
          </div>
          <div className="text-2xl font-bold text-amber-300 font-mono">
            ${loading ? '...' : (summary?.total_cost_usd?.toFixed(4) || '0.0000')}
          </div>
          <div className="text-[11px] text-slate-500 mt-1">Rate card accurate</div>
        </Card>

        <Card className="p-5 border-[#1E2433]">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-medium">Active Projects</span>
            <FolderKanban className="w-4 h-4 text-cyan-400" />
          </div>
          <div className="text-2xl font-bold text-white font-mono">
            {loading ? '...' : projects.length}
          </div>
          <div className="text-[11px] text-slate-500 mt-1">Workspace collections</div>
        </Card>
      </div>

      {/* Recent Generations & Quick Links */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-semibold text-slate-200">Recent Generation Jobs</h3>
            <Link href="/history" className="text-xs text-emerald-400 hover:underline flex items-center">
              View all <ArrowUpRight className="w-3 h-3 ml-0.5" />
            </Link>
          </div>

          <Card className="p-0 overflow-hidden border-[#1E2433]">
            {loading ? (
              <div className="p-8 text-center text-xs text-slate-500 font-mono">Loading telemetry records...</div>
            ) : recentJobs.length === 0 ? (
              <div className="p-10 text-center text-xs text-slate-500">
                <Sparkles className="w-6 h-6 mx-auto mb-2 text-slate-600" />
                No generations recorded yet. Create an image or video to begin telemetry.
              </div>
            ) : (
              <div className="divide-y divide-[#1E2433]">
                {recentJobs.map((job) => (
                  <div key={job.id} className="p-4 flex items-center justify-between hover:bg-[#161B26]/50 transition-colors">
                    <div className="min-w-0 pr-4">
                      <div className="flex items-center gap-2 mb-1">
                        <Badge variant={job.status === 'completed' ? 'emerald' : job.status === 'failed' ? 'rose' : 'amber'}>
                          {job.status}
                        </Badge>
                        <span className="text-[11px] font-mono text-slate-500">{job.model_id}</span>
                      </div>
                      <p className="text-xs text-slate-300 truncate max-w-md">{job.prompt}</p>
                    </div>
                    <div className="text-right font-mono text-[11px] text-slate-400 flex-shrink-0">
                      <div>{job.latency_ms ? `${Math.round(job.latency_ms)}ms` : '—'}</div>
                      <div className="text-emerald-400">${job.cost_usd?.toFixed(4) || '0.000'}</div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </Card>
        </div>

        {/* Research Suite Callout */}
        <div className="space-y-4">
          <h3 className="text-sm font-semibold text-slate-200">Research Benchmarks</h3>
          <Card className="p-5 border-[#1E2433] bg-[#0E121A]">
            <h4 className="text-sm font-bold text-white mb-2">Comparative Evaluation</h4>
            <p className="text-xs text-slate-400 leading-relaxed mb-4">
              Run reproducible experiments across standardized prompts. Calculate p50/p95 latency and compare with the intelligent router policy.
            </p>
            <Link href="/experiments">
              <Button size="sm" variant="outline" className="w-full">
                Open Benchmark Suite
              </Button>
            </Link>
          </Card>
        </div>
      </div>
    </div>
  );
}
