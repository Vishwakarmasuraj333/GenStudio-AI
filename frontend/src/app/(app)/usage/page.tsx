'use client';

import React, { useState, useEffect } from 'react';
import { apiFetch } from '@/lib/api';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { BarChart3, DollarSign, Clock, Layers } from 'lucide-react';

export default function UsagePage() {
  const [summary, setSummary] = useState<any>(null);
  const [records, setRecords] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      apiFetch('/usage/summary'),
      apiFetch('/usage/records')
    ]).then(([sum, recs]: any[]) => {
      setSummary(sum);
      setRecords(recs);
      setLoading(false);
    }).catch(() => setLoading(false));
  }, []);

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      <div className="border-b border-[#1E2433] pb-4">
        <h2 className="text-xl font-bold text-white">Usage & Cost Accounting</h2>
        <p className="text-xs text-slate-400">Verifiable telemetry ledger calculated from hosted provider inference rate cards</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card className="p-5 border-[#1E2433]">
          <div className="text-xs font-medium text-slate-400 mb-1">Total Incurred Cost</div>
          <div className="text-2xl font-bold font-mono text-emerald-400">
            ${summary?.total_cost_usd?.toFixed(4) || '0.0000'}
          </div>
          <div className="text-[11px] text-slate-500 mt-1">Billed at exact provider rate</div>
        </Card>

        <Card className="p-5 border-[#1E2433]">
          <div className="text-xs font-medium text-slate-400 mb-1">Completed Generations</div>
          <div className="text-2xl font-bold font-mono text-white">
            {summary?.successful_generations || 0}
          </div>
          <div className="text-[11px] text-slate-500 mt-1">{summary?.failed_generations || 0} failed requests</div>
        </Card>

        <Card className="p-5 border-[#1E2433]">
          <div className="text-xs font-medium text-slate-400 mb-1">Compute Accounting</div>
          <div className="text-2xl font-bold font-mono text-teal-400">
            {records.reduce((acc, r) => acc + (r.compute_duration_sec || 0), 0).toFixed(1)}s
          </div>
          <div className="text-[11px] text-slate-500 mt-1">Total measured inference time</div>
        </Card>
      </div>

      {/* Usage Ledger */}
      <Card className="p-0 border-[#1E2433] overflow-hidden">
        <div className="p-4 border-b border-[#1E2433] text-xs font-semibold text-white">
          Detailed Telemetry Records
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-[#0C0E15] border-b border-[#1E2433] text-slate-400 font-mono">
              <tr>
                <th className="p-4">Provider & Model</th>
                <th className="p-4">Duration</th>
                <th className="p-4">Cost</th>
                <th className="p-4">Recorded At</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#1E2433]">
              {records.map((r) => (
                <tr key={r.id} className="hover:bg-[#161B26]/30">
                  <td className="p-4 font-mono">
                    <span className="text-slate-200">{r.model_id}</span>
                    <span className="text-slate-500 ml-2 text-[10px]">({r.provider})</span>
                  </td>
                  <td className="p-4 font-mono text-slate-300">{r.compute_duration_sec}s</td>
                  <td className="p-4 font-mono text-emerald-400">${r.estimated_cost_usd?.toFixed(4)}</td>
                  <td className="p-4 font-mono text-slate-500 text-[11px]">{new Date(r.created_at).toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}
