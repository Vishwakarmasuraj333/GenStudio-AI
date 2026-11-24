'use client';

import React, { useState, useEffect } from 'react';
import { apiFetch, API_BASE, ApiError } from '@/lib/api';
import { Button } from '@/components/ui/Button';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import {
  FlaskConical, GitBranch, Play, Download,
  BarChart2, Zap, DollarSign, CheckCircle2, AlertCircle, Info
} from 'lucide-react';

export default function ExperimentsPage() {
  const [runs, setRuns] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [running, setRunning] = useState(false);
  const [experimentName, setExperimentName] = useState('Benchmark Study: Latency & Cost Optimization');
  const [category, setCategory] = useState('all');
  const [sampleSize, setSampleSize] = useState(3);
  const [executionMode, setExecutionMode] = useState<'offline-preview' | 'live'>('offline-preview');
  const [runError, setRunError] = useState<string | null>(null);

  // Intelligent Router Sandbox state
  const [routingPrompt, setRoutingPrompt] = useState('Hyper-detailed macro portrait of a jewelry artisan');
  const [priority, setPriority] = useState('balanced');
  const [routingDecision, setRoutingDecision] = useState<any>(null);
  const [evaluatingRouter, setEvaluatingRouter] = useState(false);

  const fetchRuns = async () => {
    try {
      const data = await apiFetch<any[]>('/experiments/runs');
      setRuns(data);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRuns();
  }, []);

  const handleRunExperiment = async () => {
    setRunning(true);
    setRunError(null);
    try {
      await apiFetch('/experiments/run', {
        method: 'POST',
        body: JSON.stringify({
          name: experimentName,
          target_models: [
            'black-forest-labs/FLUX.1-schnell',
            'stabilityai/stable-diffusion-xl-base-1.0'
          ],
          prompt_category: category,
          sample_size: sampleSize,
          execution_mode: executionMode
        })
      });
      fetchRuns();
    } catch (err: any) {
      setRunError(err instanceof ApiError ? err.message : 'Benchmark execution failed.');
    } finally {
      setRunning(false);
    }
  };

  const handleEvaluateRouter = async () => {
    setEvaluatingRouter(true);
    try {
      const res = await apiFetch('/experiments/route', {
        method: 'POST',
        body: JSON.stringify({
          task_type: 'text-to-image',
          prompt: routingPrompt,
          priority
        })
      });
      setRoutingDecision(res);
    } finally {
      setEvaluatingRouter(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-[#1E2433] pb-4">
        <div>
          <h2 className="text-xl font-bold text-white">Comparative Research & Intelligent Routing</h2>
          <p className="text-xs text-slate-400">Standardized benchmark harness and multi-objective routing policy</p>
        </div>
        <div className="flex items-center gap-2">
          <Badge variant="emerald">Academic Eval Suite</Badge>
          <Badge variant={executionMode === 'live' ? 'rose' : 'teal'}>
            {executionMode === 'live' ? 'Live Provider Inference' : 'Deterministic Fixtures'}
          </Badge>
        </div>
      </div>

      {/* Intelligent Router Sandbox */}
      <Card className="p-6 border-[#1E2433] bg-[#0E121B]">
        <div className="flex items-center gap-2 mb-2 text-emerald-400">
          <GitBranch className="w-5 h-5" />
          <h3 className="font-bold text-sm text-white">Multi-Objective Intelligent Model Router</h3>
        </div>
        <p className="text-xs text-slate-400 mb-5 leading-relaxed">
          Optimizes task dispatch based on budget, latency constraints, and empirical model performance. Compares against static baseline.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
          <div className="md:col-span-2">
            <label className="text-xs text-slate-300 block mb-1">Evaluation Prompt</label>
            <input
              type="text"
              value={routingPrompt}
              onChange={(e) => setRoutingPrompt(e.target.value)}
              className="w-full p-2.5 bg-[#0A0C10] border border-[#1E2433] rounded-lg text-xs text-slate-200"
            />
          </div>

          <div>
            <label className="text-xs text-slate-300 block mb-1">Optimization Policy</label>
            <select
              value={priority}
              onChange={(e) => setPriority(e.target.value)}
              className="w-full p-2.5 bg-[#0A0C10] border border-[#1E2433] rounded-lg text-xs text-slate-200"
            >
              <option value="balanced">Balanced (Cost 30%, Speed 30%, Quality 25%)</option>
              <option value="cost">Cost Minimization (60% weight)</option>
              <option value="speed">Low Latency (65% weight)</option>
              <option value="quality">Aesthetic Quality (70% weight)</option>
            </select>
          </div>
        </div>

        <Button size="sm" variant="primary" loading={evaluatingRouter} onClick={handleEvaluateRouter}>
          <Zap className="w-3.5 h-3.5 mr-1" /> Compute Optimal Route
        </Button>

        {routingDecision && (
          <div className="mt-5 p-4 rounded-xl bg-[#090C12] border border-emerald-500/30 text-xs font-mono space-y-2">
            <div className="flex flex-col sm:flex-row sm:justify-between text-emerald-400 font-bold gap-1">
              <span>Selected Model: {routingDecision.selected_model_id}</span>
              <span>Confidence: {(routingDecision.confidence_score * 100).toFixed(1)}%</span>
            </div>
            <p className="text-slate-300 font-sans">{routingDecision.reason}</p>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-2 pt-2 text-[11px] text-slate-400 border-t border-[#1E2433]">
              <div>Cost: <strong className="text-slate-200">${routingDecision.estimated_cost_usd}</strong></div>
              <div>Est. Latency: <strong className="text-slate-200">{routingDecision.estimated_latency_ms}ms</strong></div>
              <div>Cost Savings vs Static: <strong className="text-emerald-400">{routingDecision.policy_comparison.cost_savings_vs_baseline_pct}%</strong></div>
              <div>Pareto Optimal: <strong className="text-teal-400">Yes</strong></div>
            </div>
          </div>
        )}
      </Card>

      {/* Controlled Benchmark Runner */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1">
          <Card className="p-5 border-[#1E2433] space-y-4">
            <h3 className="text-sm font-semibold text-white">Execute Controlled Run</h3>

            {runError && (
              <div className="p-3 rounded-lg bg-rose-950/40 border border-rose-800/40 text-rose-300 text-xs flex items-start gap-2">
                <AlertCircle className="w-4 h-4 flex-shrink-0 mt-0.5" />
                <span>{runError}</span>
              </div>
            )}

            <div>
              <label className="text-xs text-slate-300 block mb-1">Execution Mode</label>
              <select
                value={executionMode}
                onChange={(e) => setExecutionMode(e.target.value as any)}
                className="w-full p-2 bg-[#0C0E15] border border-[#1E2433] rounded-lg text-xs text-slate-200"
              >
                <option value="offline-preview">Offline Preview (Deterministic Fixtures)</option>
                <option value="live">Live Provider Inference (Requires HF_API_TOKEN)</option>
              </select>
              <p className="text-[11px] text-slate-500 mt-1">
                {executionMode === 'live'
                  ? 'Executes real external API calls against Hugging Face. Requires valid token.'
                  : 'Uses standardized deterministic research dataset for repeatable local evaluation.'}
              </p>
            </div>

            <div>
              <label className="text-xs text-slate-300 block mb-1">Run Name</label>
              <input
                type="text"
                value={experimentName}
                onChange={(e) => setExperimentName(e.target.value)}
                className="w-full p-2 bg-[#0C0E15] border border-[#1E2433] rounded-lg text-xs text-slate-200"
              />
            </div>

            <div>
              <label className="text-xs text-slate-300 block mb-1">Prompt Domain Category</label>
              <select
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                className="w-full p-2 bg-[#0C0E15] border border-[#1E2433] rounded-lg text-xs text-slate-200"
              >
                <option value="all">All Domains (6 categories)</option>
                <option value="photorealism">Photorealism</option>
                <option value="cinematic">Cinematic</option>
                <option value="typography">Typography & Text</option>
                <option value="spatial_composition">Spatial Relations</option>
              </select>
            </div>

            <div>
              <label className="text-xs text-slate-300 block mb-1">Samples per Model</label>
              <input
                type="number"
                min={1}
                max={10}
                value={sampleSize}
                onChange={(e) => setSampleSize(parseInt(e.target.value) || 1)}
                className="w-full p-2 bg-[#0C0E15] border border-[#1E2433] rounded-lg text-xs text-slate-200 font-mono"
              />
            </div>

            <Button variant="primary" loading={running} onClick={handleRunExperiment} className="w-full">
              <Play className="w-3.5 h-3.5 mr-1" /> Run Benchmark
            </Button>
          </Card>
        </div>

        {/* Previous Runs List */}
        <div className="lg:col-span-2 space-y-4">
          <h3 className="text-sm font-semibold text-white">Recorded Benchmark Runs</h3>
          {loading ? (
            <div className="text-xs font-mono text-slate-500 p-8 text-center">Loading benchmark data...</div>
          ) : runs.length === 0 ? (
            <Card className="p-8 text-center border-[#1E2433] text-slate-500 text-xs">
              No benchmark runs recorded. Click Run Benchmark to execute controlled experiments.
            </Card>
          ) : (
            <div className="space-y-4">
              {runs.map((run) => (
                <Card key={run.id} className="p-5 border-[#1E2433]">
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-3">
                    <div>
                      <div className="flex items-center gap-2">
                        <h4 className="font-bold text-sm text-white">{run.name}</h4>
                        {run.name.includes('[Offline Preview') && (
                          <Badge variant="teal">Offline Preview</Badge>
                        )}
                      </div>
                      <p className="text-[11px] font-mono text-slate-500 mt-0.5">
                        Dataset: {run.dataset_name} • {run.prompt_count} observations • {new Date(run.created_at).toLocaleDateString()}
                      </p>
                    </div>
                    <div className="flex items-center gap-2 flex-wrap">
                      <a href={`${API_BASE}/experiments/runs/${run.id}/export/csv`} download target="_blank" rel="noopener noreferrer">
                        <Button size="sm" variant="secondary">
                          <Download className="w-3 h-3 mr-1" /> Export CSV
                        </Button>
                      </a>
                      <a href={`${API_BASE}/experiments/runs/${run.id}/export/json`} download target="_blank" rel="noopener noreferrer">
                        <Button size="sm" variant="secondary">
                          <Download className="w-3 h-3 mr-1" /> JSON
                        </Button>
                      </a>
                    </div>
                  </div>

                  {run.summary_metrics && (
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-3 border-t border-[#1E2433] text-xs font-mono">
                      {Object.entries(run.summary_metrics).map(([mId, stats]: [string, any]) => (
                        <div key={mId} className="p-3 rounded-lg bg-[#0C0E15] border border-[#1A2030]">
                          <div className="font-semibold text-slate-200 truncate mb-1">{mId.split('/')[1] || mId}</div>
                          <div className="text-[11px] text-slate-400 space-y-0.5">
                            <div>Median Latency: <strong className="text-slate-200">{stats.median_latency_ms}ms</strong></div>
                            <div>P95 Latency: <strong className="text-slate-200">{stats.p95_latency_ms}ms</strong></div>
                            <div>Cost / Success: <strong className="text-emerald-400">${stats.cost_per_success_usd}</strong></div>
                            <div>Success Rate: <strong className="text-teal-400">{(stats.success_rate * 100).toFixed(0)}%</strong></div>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </Card>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
