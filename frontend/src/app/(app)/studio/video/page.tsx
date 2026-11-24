'use client';

import React, { useState, useEffect } from 'react';
import { apiFetch, ApiError } from '@/lib/api';
import { Button } from '@/components/ui/Button';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import {
  Video, Upload, Sparkles, Download, Clock,
  CheckCircle2, AlertCircle, Play, Film, KeyRound, Info
} from 'lucide-react';

export default function VideoStudioPage() {
  const [tab, setTab] = useState<'t2v' | 'i2v'>('t2v');
  const [prompt, setPrompt] = useState('Cinematic aerial drone shot slowly drifting over misty fjord mountains at sunset, 24fps');
  const [modelId, setModelId] = useState('Lightricks/LTX-Video');
  const [durationSec, setDurationSec] = useState(5.0);
  const [fps, setFps] = useState(24);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploadedAssetId, setUploadedAssetId] = useState<string | null>(null);
  const [uploading, setUploading] = useState(false);
  const [loading, setLoading] = useState(false);
  const [currentJob, setCurrentJob] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [health, setHealth] = useState<any>(null);

  useEffect(() => {
    apiFetch<any>('/health')
      .then(setHealth)
      .catch(() => setHealth({ provider_mode: 'live', providers_configured: {} }));
  }, []);

  const isLiveMode = health?.provider_mode === 'live' || !health?.provider_mode;
  const isHfConfigured = Boolean(health?.providers_configured?.huggingface);
  const isGenerationBlocked = isLiveMode && !isHfConfigured;

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
            setError(updated.error_message || 'Video generation failed.');
          }
        }
      } catch (e) {
        clearInterval(interval);
        setLoading(false);
      }
    }, 2000);

    return () => clearInterval(interval);
  }, [currentJob]);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setSelectedFile(file);
    setUploading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const asset = await apiFetch<any>('/studio/upload', {
        method: 'POST',
        body: formData,
      });
      setUploadedAssetId(asset.id);
    } catch (err: any) {
      setError(err instanceof ApiError ? err.message : 'Upload failed.');
    } finally {
      setUploading(false);
    }
  };

  const handleGenerate = async () => {
    if (isGenerationBlocked) {
      setError('Live generation is disabled: Hugging Face API token (HF_API_TOKEN) is not configured.');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      let job;
      if (tab === 't2v') {
        job = await apiFetch<any>('/studio/video', {
          method: 'POST',
          body: JSON.stringify({
            prompt,
            model_id: modelId,
            duration_sec: durationSec,
            fps
          })
        });
      } else {
        if (!uploadedAssetId) {
          setError('Please upload a reference image first.');
          setLoading(false);
          return;
        }
        job = await apiFetch<any>('/studio/image-to-video', {
          method: 'POST',
          body: JSON.stringify({
            reference_image_id: uploadedAssetId,
            prompt,
            model_id: modelId,
            duration_sec: durationSec
          })
        });
      }
      setCurrentJob(job);
    } catch (err: any) {
      setError(err instanceof ApiError ? err.message : 'Video generation failed.');
      setLoading(false);
    }
  };

  const completedAsset = currentJob?.assets?.[0];
  const isOfflinePreview = completedAsset?.metadata_json?.is_offline_preview || health?.provider_mode === 'offline-preview';

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-[#1E2433] pb-4">
        <div>
          <h2 className="text-xl font-bold text-white">Video Generation Studio</h2>
          <p className="text-xs text-slate-400">Synthesize temporal video sequences with LTX-Video Diffusion Transformer</p>
        </div>
        <div className="flex items-center gap-2">
          {health?.provider_mode === 'offline-preview' ? (
            <Badge variant="teal">Offline Preview Mode</Badge>
          ) : isHfConfigured ? (
            <Badge variant="teal">LTX-Video 24 FPS Ready</Badge>
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
                Live video synthesis requires a valid <code className="bg-amber-900/60 px-1 py-0.5 rounded text-amber-100 font-mono">HF_API_TOKEN</code> in your server environment (<code className="font-mono">.env</code>). Video generation is paused to avoid delivering fake media.
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
            <strong>Offline Preview Active</strong>: Video sequences in this mode use test fixtures for testing. Real GPU compute is not allocated.
          </span>
        </div>
      )}

      {/* Tabs */}
      <div className="flex items-center gap-3 border-b border-[#1E2433] pb-2 text-xs font-semibold">
        <button
          onClick={() => setTab('t2v')}
          className={`px-3 py-1.5 rounded-lg transition-colors touch-target ${tab === 't2v' ? 'bg-teal-950 text-teal-400 border border-teal-700/50 font-bold' : 'text-slate-400 hover:text-white'}`}
        >
          Text to Video
        </button>
        <button
          onClick={() => setTab('i2v')}
          className={`px-3 py-1.5 rounded-lg transition-colors touch-target ${tab === 'i2v' ? 'bg-teal-950 text-teal-400 border border-teal-700/50 font-bold' : 'text-slate-400 hover:text-white'}`}
        >
          Image to Video (Animate)
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Controls */}
        <div className="space-y-5 lg:col-span-1">
          <Card className="p-5 border-[#1E2433] space-y-4">
            {tab === 'i2v' && (
              <div>
                <label className="text-xs font-semibold text-slate-200 mb-1.5 block">Reference Image</label>
                <div className="border-2 border-dashed border-[#1E2433] hover:border-teal-500/50 rounded-lg p-4 text-center cursor-pointer transition-colors bg-[#0C0E15]">
                  <input
                    type="file"
                    accept="image/png, image/jpeg, image/webp"
                    onChange={handleFileUpload}
                    className="hidden"
                    id="ref-img-upload"
                  />
                  <label htmlFor="ref-img-upload" className="cursor-pointer block space-y-2">
                    <Upload className="w-6 h-6 mx-auto text-slate-500" />
                    <p className="text-xs text-slate-300">
                      {selectedFile ? selectedFile.name : 'Click to upload image'}
                    </p>
                    <p className="text-[10px] text-slate-500 font-mono">PNG, JPG, WebP up to 25MB</p>
                  </label>
                </div>
                {uploading && <p className="text-[10px] font-mono text-teal-400 mt-1">Verifying magic bytes...</p>}
                {uploadedAssetId && <p className="text-[10px] font-mono text-emerald-400 mt-1 flex items-center gap-1"><CheckCircle2 className="w-3 h-3" /> Image uploaded and verified</p>}
              </div>
            )}

            <div>
              <label className="text-xs font-semibold text-slate-200 mb-1.5 block">Motion Prompt</label>
              <textarea
                rows={4}
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                className="w-full p-3 bg-[#0C0E15] border border-[#1E2433] rounded-lg text-xs text-slate-200 placeholder-slate-600 focus:outline-none focus:border-teal-500 leading-relaxed"
                placeholder="Describe scene dynamics and camera movement..."
              />
            </div>

            <div>
              <label className="text-xs font-semibold text-slate-200 mb-1.5 block">Model Architecture</label>
              <select
                value={modelId}
                onChange={(e) => setModelId(e.target.value)}
                className="w-full p-2.5 bg-[#0C0E15] border border-[#1E2433] rounded-lg text-xs text-slate-200 font-mono focus:outline-none focus:border-teal-500"
              >
                <option value="Lightricks/LTX-Video">LTX-Video (DiT) • 24fps ($0.045)</option>
                <option value="Wan-AI/Wan2.1-T2V-14B">Wan2.1 14B Video • 16fps ($0.080)</option>
              </select>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="text-xs font-semibold text-slate-200 mb-1.5 block">Duration</label>
                <select
                  value={durationSec}
                  onChange={(e) => setDurationSec(parseFloat(e.target.value))}
                  className="w-full p-2 bg-[#0C0E15] border border-[#1E2433] rounded-lg text-xs text-slate-200 font-mono"
                >
                  <option value={3.0}>3.0 seconds</option>
                  <option value={5.0}>5.0 seconds</option>
                  <option value={8.0}>8.0 seconds</option>
                </select>
              </div>

              <div>
                <label className="text-xs font-semibold text-slate-200 mb-1.5 block">Frame Rate</label>
                <select
                  value={fps}
                  onChange={(e) => setFps(parseInt(e.target.value))}
                  className="w-full p-2 bg-[#0C0E15] border border-[#1E2433] rounded-lg text-xs text-slate-200 font-mono"
                >
                  <option value={16}>16 FPS</option>
                  <option value={24}>24 FPS</option>
                </select>
              </div>
            </div>

            <Button
              type="button"
              variant={isGenerationBlocked ? 'secondary' : 'primary'}
              loading={loading}
              disabled={isGenerationBlocked}
              onClick={handleGenerate}
              className="w-full py-3 bg-teal-600 hover:bg-teal-500 text-sm font-semibold shadow-md shadow-teal-950/40"
            >
              <Film className="w-4 h-4 mr-1.5" />
              {isGenerationBlocked ? 'HF Token Required to Generate' : loading ? 'Synthesizing Video...' : 'Generate Video'}
            </Button>
          </Card>
        </div>

        {/* Video Canvas */}
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
                <div className="w-10 h-10 border-2 border-teal-500 border-t-transparent rounded-full animate-spin"></div>
                <p className="text-xs font-mono text-slate-400">Rendering temporal frames in background queue...</p>
                <span className="text-[10px] text-slate-500 font-mono">Job ID: {currentJob?.id?.slice(0, 8)}</span>
              </div>
            )}

            {!loading && !completedAsset && !error && (
              <div className="text-center text-slate-500 space-y-2">
                <Film className="w-10 h-10 mx-auto text-slate-600" />
                <p className="text-xs">Select options and click Generate Video.</p>
                <p className="text-[10px] font-mono text-slate-600">The video will be verified before rendering in player.</p>
              </div>
            )}

            {completedAsset && (
              <div className="w-full flex flex-col items-center relative">
                {isOfflinePreview && (
                  <div className="absolute top-2 left-2 z-10 px-2 py-1 rounded bg-teal-950/80 border border-teal-700/60 text-[10px] font-mono text-teal-300 backdrop-blur-sm">
                    Offline Preview Fixture
                  </div>
                )}
                <video
                  controls
                  playsInline
                  autoPlay
                  loop
                  src={completedAsset.public_url}
                  className="max-h-[440px] w-auto rounded-lg shadow-2xl border border-[#1E2433]"
                />
              </div>
            )}
          </Card>

          {completedAsset && (
            <div className="p-4 rounded-xl bg-[#11141D] border border-[#1E2433] flex flex-wrap items-center justify-between gap-3 text-xs">
              <div className="flex items-center gap-3 font-mono text-slate-400">
                <span>Latency: <strong className="text-slate-200">{currentJob?.latency_ms ? `${Math.round(currentJob.latency_ms)}ms` : '—'}</strong></span>
                <span>•</span>
                <span>Cost: <strong className="text-teal-400">${currentJob?.cost_usd?.toFixed(4) || '0.0000'}</strong></span>
                <span>•</span>
                <span>Format: <strong className="text-slate-200">MP4 (Verified)</strong></span>
              </div>

              <a href={completedAsset.public_url} download={`genstudio_video_${completedAsset.id.slice(0, 8)}.mp4`}>
                <Button size="sm" variant="primary" className="bg-teal-600 hover:bg-teal-500">
                  <Download className="w-3.5 h-3.5 mr-1" /> Download MP4
                </Button>
              </a>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
