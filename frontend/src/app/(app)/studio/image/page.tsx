'use client';

import React, { useState, useEffect } from 'react';
import { apiFetch, ApiError } from '@/lib/api';
import { Button } from '@/components/ui/Button';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import {
  Sparkles, Download, RefreshCw, Wand2, Sliders,
  CheckCircle2, AlertCircle, Copy, Bookmark, Eye, KeyRound, Info
} from 'lucide-react';

export default function ImageStudioPage() {
  const [prompt, setPrompt] = useState('An ethereal glass observatory on an emerald cliff at golden hour, 85mm architectural photography, high fidelity');
  const [negativePrompt, setNegativePrompt] = useState('');
  const [modelId, setModelId] = useState('black-forest-labs/FLUX.1-schnell');
  const [aspectRatio, setAspectRatio] = useState('16:9');
  const [seed, setSeed] = useState<number | undefined>(undefined);
  const [stylePreset, setStylePreset] = useState('photorealistic');
  const [enableEnhancement, setEnableEnhancement] = useState(false);
  const [loading, setLoading] = useState(false);
  const [enhancing, setEnhancing] = useState(false);
  const [currentJob, setCurrentJob] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);
  const [health, setHealth] = useState<any>(null);

  // Check health and provider configuration on mount
  useEffect(() => {
    apiFetch<any>('/health')
      .then(setHealth)
      .catch(() => setHealth({ provider_mode: 'live', providers_configured: {} }));
  }, []);

  const isLiveMode = health?.provider_mode === 'live' || !health?.provider_mode;
  const isHfConfigured = Boolean(health?.providers_configured?.huggingface);
  const isGenerationBlocked = isLiveMode && !isHfConfigured;

  // Poll job status until completed/failed
  useEffect(() => {
    if (!currentJob || currentJob.status === 'completed' || currentJob.status === 'failed' || currentJob.status === 'cancelled') {
      return;
    }

    const interval = setInterval(async () => {
      try {
        const updated = await apiFetch<any>(`/studio/jobs/${currentJob.id}`);
        setCurrentJob(updated);
        if (updated.status === 'completed' || updated.status === 'failed' || updated.status === 'cancelled') {
          setLoading(false);
          if (updated.status === 'failed') {
            setError(updated.error_message || 'Generation failed.');
          }
        }
      } catch (e) {
        clearInterval(interval);
        setLoading(false);
      }
    }, 1500);

    return () => clearInterval(interval);
  }, [currentJob]);

  const handleGenerate = async () => {
    if (isGenerationBlocked) {
      setError('Live generation is disabled: Hugging Face API token (HF_API_TOKEN) is not configured in the server environment.');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const job = await apiFetch<any>('/studio/image', {
        method: 'POST',
        body: JSON.stringify({
          prompt,
          negative_prompt: negativePrompt || undefined,
          model_id: modelId,
          aspect_ratio: aspectRatio,
          seed: seed || undefined,
          style_preset: stylePreset,
          enable_prompt_enhancement: enableEnhancement
        })
      });
      setCurrentJob(job);
    } catch (err: any) {
      setError(err instanceof ApiError ? err.message : 'Generation request failed.');
      setLoading(false);
    }
  };

  const handleEnhancePrompt = async () => {
    setEnhancing(true);
    try {
      const res = await apiFetch<any>('/studio/enhance-prompt', {
        method: 'POST',
        body: JSON.stringify({ prompt, style: stylePreset })
      });
      setPrompt(res.enhanced_prompt);
      if (res.suggested_negative_prompt && !negativePrompt) {
        setNegativePrompt(res.suggested_negative_prompt);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setEnhancing(false);
    }
  };

  const copyPrompt = () => {
    navigator.clipboard.writeText(prompt);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const completedAsset = currentJob?.assets?.[0];
  const isOfflinePreview = completedAsset?.metadata_json?.is_offline_preview || health?.provider_mode === 'offline-preview';

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-[#1E2433] pb-4">
        <div>
          <h2 className="text-xl font-bold text-white">Text-to-Image Generation</h2>
          <p className="text-xs text-slate-400">Direct serverless inference with prompt enhancement & seed reproducibility</p>
        </div>
        <div className="flex items-center gap-2">
          {health?.provider_mode === 'offline-preview' ? (
            <Badge variant="teal">Offline Preview Mode</Badge>
          ) : isHfConfigured ? (
            <Badge variant="emerald">Live Provider Ready</Badge>
          ) : (
            <Badge variant="amber">HF Token Required</Badge>
          )}
        </div>
      </div>

      {/* Honest Provider Status Banner */}
      {isGenerationBlocked && (
        <div className="p-4 rounded-xl bg-amber-950/40 border border-amber-800/50 flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs">
          <div className="flex items-start gap-3">
            <KeyRound className="w-5 h-5 text-amber-400 flex-shrink-0 mt-0.5" />
            <div>
              <p className="font-semibold text-amber-200">Server Inference Credential Required</p>
              <p className="text-amber-300/80 mt-0.5 leading-relaxed">
                Live image generation requires a valid <code className="bg-amber-900/60 px-1 py-0.5 rounded text-amber-100 font-mono">HF_API_TOKEN</code> in your server environment (<code className="font-mono">.env</code>). Generation is paused to prevent generating misleading substitute outputs.
              </p>
            </div>
          </div>
          <div className="flex-shrink-0 text-amber-400 font-mono text-[11px] self-end sm:self-center">
            PROVIDER_MODE=live
          </div>
        </div>
      )}

      {health?.provider_mode === 'offline-preview' && (
        <div className="p-3.5 rounded-xl bg-teal-950/40 border border-teal-800/40 flex items-center gap-3 text-xs text-teal-300">
          <Info className="w-4 h-4 flex-shrink-0" />
          <span>
            <strong>Offline Preview Active</strong>: Generations in this mode use synthetic evaluation fixtures for offline testing. Real API tokens are not consumed.
          </span>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left: Input Controls */}
        <div className="space-y-5 lg:col-span-1">
          <Card className="p-5 border-[#1E2433] space-y-4">
            {/* Prompt Box */}
            <div>
              <div className="flex items-center justify-between mb-1.5">
                <label className="text-xs font-semibold text-slate-200">Prompt</label>
                <button
                  onClick={handleEnhancePrompt}
                  type="button"
                  disabled={enhancing}
                  className="text-[11px] text-emerald-400 hover:text-emerald-300 flex items-center gap-1 font-mono disabled:opacity-50"
                >
                  <Wand2 className="w-3 h-3" /> {enhancing ? 'Enhancing...' : 'Enhance with AI'}
                </button>
              </div>
              <textarea
                rows={4}
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                className="w-full p-3 bg-[#0C0E15] border border-[#1E2433] rounded-lg text-xs text-slate-200 placeholder-slate-600 focus:outline-none focus:border-emerald-500 leading-relaxed"
                placeholder="Describe your visual concept in detail..."
              />
            </div>

            {/* Model Selector */}
            <div>
              <label className="text-xs font-semibold text-slate-200 mb-1.5 block">AI Model</label>
              <select
                value={modelId}
                onChange={(e) => setModelId(e.target.value)}
                className="w-full p-2.5 bg-[#0C0E15] border border-[#1E2433] rounded-lg text-xs text-slate-200 focus:outline-none focus:border-emerald-500 font-mono"
              >
                <option value="black-forest-labs/FLUX.1-schnell">FLUX.1 [schnell] • 4 Steps ($0.003)</option>
                <option value="stabilityai/stable-diffusion-xl-base-1.0">SDXL 1.0 Base • 30 Steps ($0.006)</option>
              </select>
            </div>

            {/* Aspect Ratio */}
            <div>
              <label className="text-xs font-semibold text-slate-200 mb-1.5 block">Aspect Ratio</label>
              <div className="grid grid-cols-4 gap-2 text-center text-xs font-mono">
                {['1:1', '16:9', '9:16', '4:3'].map((ar) => (
                  <button
                    key={ar}
                    type="button"
                    onClick={() => setAspectRatio(ar)}
                    className={`py-1.5 rounded border transition-colors touch-target ${aspectRatio === ar ? 'bg-emerald-950 border-emerald-500 text-emerald-400 font-bold' : 'border-[#1E2433] text-slate-400 hover:bg-slate-800'}`}
                  >
                    {ar}
                  </button>
                ))}
              </div>
            </div>

            {/* Style Preset */}
            <div>
              <label className="text-xs font-semibold text-slate-200 mb-1.5 block">Style Preset</label>
              <select
                value={stylePreset}
                onChange={(e) => setStylePreset(e.target.value)}
                className="w-full p-2.5 bg-[#0C0E15] border border-[#1E2433] rounded-lg text-xs text-slate-200 focus:outline-none focus:border-emerald-500"
              >
                <option value="photorealistic">Photorealistic</option>
                <option value="cinematic">Cinematic 70mm</option>
                <option value="artistic">Digital Concept Art</option>
                <option value="anime">Anime High-Detail</option>
                <option value="3d_render">3D Octane Render</option>
              </select>
            </div>

            {/* Negative Prompt */}
            <div>
              <label className="text-xs font-semibold text-slate-200 mb-1.5 block">Negative Prompt (Optional)</label>
              <input
                type="text"
                value={negativePrompt}
                onChange={(e) => setNegativePrompt(e.target.value)}
                placeholder="blurry, distorted, artifacts, watermark"
                className="w-full p-2.5 bg-[#0C0E15] border border-[#1E2433] rounded-lg text-xs text-slate-200 placeholder-slate-600 focus:outline-none focus:border-emerald-500"
              />
            </div>

            {/* Seed */}
            <div>
              <label className="text-xs font-semibold text-slate-200 mb-1.5 block">Seed (Optional for reproducibility)</label>
              <input
                type="number"
                value={seed !== undefined ? seed : ''}
                onChange={(e) => setSeed(e.target.value ? parseInt(e.target.value) : undefined)}
                placeholder="e.g. 42"
                className="w-full p-2.5 bg-[#0C0E15] border border-[#1E2433] rounded-lg text-xs text-slate-200 placeholder-slate-600 focus:outline-none focus:border-emerald-500 font-mono"
              />
            </div>

            <Button
              type="button"
              variant={isGenerationBlocked ? 'secondary' : 'primary'}
              loading={loading}
              disabled={isGenerationBlocked}
              onClick={handleGenerate}
              className="w-full py-3 text-sm font-semibold shadow-md shadow-emerald-950/40"
            >
              <Sparkles className="w-4 h-4 mr-1.5" />
              {isGenerationBlocked ? 'HF Token Required to Generate' : loading ? 'Synthesizing...' : 'Generate Image'}
            </Button>
          </Card>
        </div>

        {/* Right: Preview Canvas & Actions */}
        <div className="lg:col-span-2 space-y-4">
          <Card className="min-h-[460px] flex flex-col items-center justify-center p-6 border-[#1E2433] bg-[#0C0E15] relative overflow-hidden">
            {error && (
              <div className="p-4 rounded-lg bg-rose-950/40 border border-rose-800/40 text-rose-300 text-xs max-w-md flex items-start gap-2.5 my-4">
                <AlertCircle className="w-4 h-4 flex-shrink-0 mt-0.5" />
                <div className="space-y-1">
                  <p className="font-semibold text-rose-200">Execution Notice</p>
                  <p className="text-rose-300/90 leading-relaxed">{error}</p>
                </div>
              </div>
            )}

            {loading && !completedAsset && (
              <div className="flex flex-col items-center gap-3">
                <div className="w-10 h-10 border-2 border-emerald-500 border-t-transparent rounded-full animate-spin"></div>
                <p className="text-xs font-mono text-slate-400">
                  {currentJob?.status === 'processing' ? 'Processing inference via provider...' : 'Queued for execution...'}
                </p>
                <span className="text-[10px] text-slate-500 font-mono">Job ID: {currentJob?.id?.slice(0, 8)}</span>
              </div>
            )}

            {!loading && !completedAsset && !error && (
              <div className="text-center text-slate-500 space-y-2">
                <Sparkles className="w-10 h-10 mx-auto text-slate-600" />
                <p className="text-xs">Configure parameters and click Generate Image.</p>
                <p className="text-[10px] font-mono text-slate-600">Model outputs will render here with full metadata.</p>
              </div>
            )}

            {completedAsset && (
              <div className="w-full flex flex-col items-center relative">
                {isOfflinePreview && (
                  <div className="absolute top-2 left-2 z-10 px-2 py-1 rounded bg-teal-950/80 border border-teal-700/60 text-[10px] font-mono text-teal-300 backdrop-blur-sm">
                    Offline Preview Fixture
                  </div>
                )}
                <img
                  src={completedAsset.public_url}
                  alt={currentJob?.prompt || 'Generated output'}
                  className="max-h-[460px] w-auto rounded-lg shadow-2xl object-contain border border-[#1E2433]"
                />
              </div>
            )}
          </Card>

          {/* Action Toolbar */}
          {completedAsset && (
            <div className="p-4 rounded-xl bg-[#11141D] border border-[#1E2433] flex flex-wrap items-center justify-between gap-3 text-xs">
              <div className="flex items-center gap-3 font-mono text-slate-400">
                <span>Latency: <strong className="text-slate-200">{currentJob?.latency_ms ? `${Math.round(currentJob.latency_ms)}ms` : '—'}</strong></span>
                <span>•</span>
                <span>Cost: <strong className="text-emerald-400">${currentJob?.cost_usd?.toFixed(4) || '0.0000'}</strong></span>
                <span>•</span>
                <span>SHA-256: <strong className="text-slate-200">{completedAsset.checksum_sha256.slice(0, 8)}...</strong></span>
              </div>

              <div className="flex items-center gap-2">
                <Button size="sm" variant="secondary" onClick={copyPrompt}>
                  <Copy className="w-3.5 h-3.5 mr-1" /> {copied ? 'Copied' : 'Copy Prompt'}
                </Button>
                <a href={completedAsset.public_url} download={`genstudio_${completedAsset.id.slice(0, 8)}.png`}>
                  <Button size="sm" variant="primary">
                    <Download className="w-3.5 h-3.5 mr-1" /> Download PNG
                  </Button>
                </a>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
