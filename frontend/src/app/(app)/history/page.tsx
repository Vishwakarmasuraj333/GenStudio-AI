'use client';

import React, { useState, useEffect } from 'react';
import { apiFetch, ApiError } from '@/lib/api';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import { History, RefreshCw, AlertCircle, CheckCircle2, Filter } from 'lucide-react';

export default function HistoryPage() {
  const [jobs, setJobs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedTask, setSelectedTask] = useState<string>('all');
  const [error, setError] = useState<string | null>(null);

  const fetchJobs = async () => {
    try {
      const data = await apiFetch<any[]>('/history/?limit=50');
      setJobs(data);
    } catch (err: any) {
      setError(err instanceof ApiError ? err.message : 'Failed to fetch history.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchJobs();
  }, []);

  const handleRetry = async (jobId: string) => {
    try {
      await apiFetch(`/studio/jobs/${jobId}/retry`, { method: 'POST' });
      fetchJobs();
    } catch (err: any) {
      alert(err instanceof ApiError ? err.message : 'Retry failed');
    }
  };

  const filteredJobs = selectedTask === 'all'
    ? jobs
    : jobs.filter((j) => j.task_type === selectedTask);

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-[#1E2433] pb-4">
        <div>
          <h2 className="text-xl font-bold text-white">Generation History</h2>
          <p className="text-xs text-slate-400">Complete audit ledger of all requested image and video synthesis tasks</p>
        </div>
        <div className="flex items-center gap-3">
          <Button size="sm" variant="secondary" onClick={fetchJobs}>
            <RefreshCw className="w-3.5 h-3.5 mr-1.5" /> Refresh
          </Button>
        </div>
      </div>

      {error && (
        <div className="p-3.5 rounded-xl bg-rose-950/40 border border-rose-800/40 text-rose-300 text-xs flex items-center gap-2">
          <AlertCircle className="w-4 h-4 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Task Filters */}
      <div className="flex items-center gap-2 overflow-x-auto pb-1 text-xs">
        <span className="text-slate-500 flex items-center gap-1 font-mono text-[11px] mr-1">
          <Filter className="w-3 h-3" /> Filter:
        </span>
        {['all', 'text-to-image', 'text-to-video', 'image-to-video', 'image-to-image'].map((t) => (
          <button
            key={t}
            onClick={() => setSelectedTask(t)}
            className={`px-3 py-1.5 rounded-lg font-mono text-xs whitespace-nowrap transition-colors ${
              selectedTask === t
                ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40'
                : 'bg-[#121622] text-slate-400 border border-[#1E2433] hover:text-slate-200'
            }`}
          >
            {t === 'all' ? 'All Tasks' : t}
          </button>
        ))}
      </div>

      <Card className="p-0 border-[#1E2433] overflow-hidden">
        {loading ? (
          <div className="p-12 text-center text-xs font-mono text-slate-500">Loading history records...</div>
        ) : filteredJobs.length === 0 ? (
          <div className="p-12 text-center text-xs text-slate-500">
            {jobs.length === 0 ? 'No generation history recorded yet.' : 'No jobs matching selected filter.'}
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs min-w-[700px]">
              <thead className="bg-[#0C0E15] border-b border-[#1E2433] text-slate-400 font-mono">
                <tr>
                  <th className="p-4">Task & Model</th>
                  <th className="p-4">Prompt</th>
                  <th className="p-4">Status</th>
                  <th className="p-4">Latency</th>
                  <th className="p-4">Cost</th>
                  <th className="p-4">Timestamp</th>
                  <th className="p-4 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#1E2433]">
                {filteredJobs.map((job) => (
                  <tr key={job.id} className="hover:bg-[#161B26]/40 transition-colors">
                    <td className="p-4 font-mono">
                      <div className="font-semibold text-slate-200">{job.task_type}</div>
                      <div className="text-[10px] text-slate-500 truncate max-w-[150px]">{job.model_id}</div>
                    </td>
                    <td className="p-4 max-w-xs truncate text-slate-300">
                      {job.prompt}
                      {job.error_message && (
                        <div className="text-[10px] text-rose-400 truncate mt-0.5">{job.error_message}</div>
                      )}
                    </td>
                    <td className="p-4">
                      <Badge variant={job.status === 'completed' ? 'emerald' : job.status === 'failed' ? 'rose' : 'amber'}>
                        {job.status}
                      </Badge>
                    </td>
                    <td className="p-4 font-mono text-slate-400">
                      {job.latency_ms ? `${Math.round(job.latency_ms)}ms` : '—'}
                    </td>
                    <td className="p-4 font-mono text-emerald-400">
                      ${job.cost_usd?.toFixed(4) || '0.0000'}
                    </td>
                    <td className="p-4 font-mono text-slate-500 text-[11px] whitespace-nowrap">
                      {new Date(job.created_at).toLocaleString()}
                    </td>
                    <td className="p-4 text-right whitespace-nowrap">
                      {job.status === 'failed' && (
                        <Button size="sm" variant="ghost" onClick={() => handleRetry(job.id)}>
                          Retry
                        </Button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Card>
    </div>
  );
}
