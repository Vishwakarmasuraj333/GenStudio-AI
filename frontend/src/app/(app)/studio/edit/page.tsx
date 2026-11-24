'use client';

import React, { useState, useEffect } from 'react';
import { apiFetch, ApiError } from '@/lib/api';
import { Button } from '@/components/ui/Button';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Wand2, Upload, Download, AlertCircle, CheckCircle2, KeyRound, Info, Copy } from 'lucide-react';

export default function EditStudioPage() {
  const [prompt, setPrompt] = useState('Change the background to a futuristic neon cyberpunk metropolis');
  const [strength, setStrength] = useState(0.75);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
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
    if (!currentJob || currentJob.status === 'completed' || currentJob.status === 'failed') return;
    const interval = setInterval(async () => {
      try {
        const updated = await apiFetch<any>(`/studio/jobs/${currentJob.id}`);
        setCurrentJob(updated);
        if (updated.status === 'completed' || updated.status === 'failed') {
          setLoading(false);
          if (updated.status === 'failed') {
            setError(updated.error_message || 'Transformation failed.');
          }
        }
      } catch (e) {
        clearInterval(interval);
        setLoading(false);
      }
    }, 1500);
    return () => clearInterval(interval);
  }, [currentJob]);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setSelectedFile(file);
    setPreviewUrl(URL.createObjectURL(file));
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

  const handleTransform = async () => {
    if (isGenerationBlocked) {
      setError('Live transformation is disabled: Hugging Face API token (HF_API_TOKEN) is not configured.');
      return;
    }
    if (!uploadedAssetId) {
      setError('Please upload a source image first.');
      return;
    }
    setLoading(true);
    setError(null);

    try {
      const job = await apiFetch<any>('/studio/edit', {
        method: 'POST',
        body: JSON.stringify({
          base_image_id: uploadedAssetId,
          prompt,
          strength,
          model_id: 'timbrooks/instruct-pix2pix'
        })
      });
      setCurrentJob(job);
    } catch (err: any) {
      setError(err instanceof ApiError ? err.message : 'Transformation failed.');
      setLoading(false);
    }
  };

  const completedAsset = currentJob?.assets?.[0];
  const isOfflinePreview = completedAsset?.metadata_json?.is_offline_preview || health?.provider_mode === 'offline-preview';

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-[#1E2433] pb-4">
        <div>
          <h2 className="text-xl font-bold text-white">Image-to-Image Transformation</h2>
          <p className="text-xs text-slate-400">Instruct-Pix2Pix guided semantic modification with transformation strength controls</p>
        </div>
        <div className="flex items-center gap-2">
          {health?.provider_mode === 'offline-preview' ? (
            <Badge variant="teal">Offline Preview Mode</Badge>
          ) : isHfConfigured ? (
            <Badge variant="emerald">InstructPix2Pix Ready</Badge>
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
                Live image editing requires a valid <code className="bg-amber-900/60 px-1 py-0.5 rounded text-amber-100 font-mono">HF_API_TOKEN</code> in your server environment (<code className="font-mono">.env</code>). Action is paused to avoid returning dummy outputs.
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
            <strong>Offline Preview Active</strong>: Transformed outputs use synthetic evaluation fixtures.
          </span>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="space-y-4 lg:col-span-1">
          <Card className="p-5 border-[#1E2433] space-y-4">
            <div>
              <label className="text-xs font-semibold text-slate-200 mb-1.5 block">Source Image</label>
              <div className="border-2 border-dashed border-[#1E2433] hover:border-emerald-500/50 rounded-lg p-4 text-center cursor-pointer transition-colors bg-[#0C0E15]">
                <input
                  type="file"
                  accept="image/png, image/jpeg, image/webp"
                  onChange={handleFileUpload}
                  className="hidden"
                  id="source-img-upload"
                />
                <label htmlFor="source-img-upload" className="cursor-pointer block space-y-2">
                  {previewUrl ? (
                    <img src={previewUrl} alt="Source Preview" className="h-28 mx-auto object-contain rounded" />
                  ) : (
                    <Upload className="w-6 h-6 mx-auto text-slate-500" />
                  )}
                  <p className="text-xs text-slate-300">{selectedFile ? selectedFile.name : 'Upload Base Image'}</p>
                  <p className="text-[10px] text-slate-500 font-mono">PNG, JPG, WebP</p>
                </label>
              </div>
              {uploading && <p className="text-[10px] font-mono text-teal-400 mt-1">Verifying image signature...</p>}
              {uploadedAssetId && <p className="text-[10px] font-mono text-emerald-400 mt-1 flex items-center gap-1"><CheckCircle2 className="w-3 h-3" /> Image verified & persisted</p>}
            </div>

            <div>
              <label className="text-xs font-semibold text-slate-200 mb-1.5 block">Editing Instruction</label>
              <textarea
                rows={3}
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                className="w-full p-3 bg-[#0C0E15] border border-[#1E2433] rounded-lg text-xs text-slate-200 focus:outline-none focus:border-emerald-500"
                placeholder="What should be changed?"
              />
            </div>

            <div>
              <div className="flex justify-between text-xs font-semibold text-slate-200 mb-1.5">
                <span>Transformation Strength</span>
                <span className="font-mono text-emerald-400">{strength}</span>
              </div>
              <input
                type="range"
                min={0.1}
                max={1.0}
                step={0.05}
                value={strength}
                onChange={(e) => setStrength(parseFloat(e.target.value))}
                className="w-full accent-emerald-500"
              />
            </div>

            <Button
              type="button"
              variant={isGenerationBlocked ? 'secondary' : 'primary'}
              loading={loading}
              disabled={isGenerationBlocked || !uploadedAssetId}
              onClick={handleTransform}
              className="w-full py-3"
            >
              <Wand2 className="w-4 h-4 mr-1.5" />
              {isGenerationBlocked ? 'HF Token Required' : loading ? 'Transforming...' : 'Apply Transformation'}
            </Button>
          </Card>
        </div>

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
            {loading && <div className="text-xs font-mono text-slate-400">Processing image transformation...</div>}
            {!loading && !completedAsset && !error && (
              <p className="text-xs text-slate-500">Transformed output will render here once processed.</p>
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
                  alt="Transformed output"
                  className="max-h-[440px] rounded-lg border border-[#1E2433] shadow-2xl object-contain"
                />
              </div>
            )}
          </Card>

          {completedAsset && (
            <div className="p-4 rounded-xl bg-[#11141D] border border-[#1E2433] flex flex-wrap items-center justify-between gap-3 text-xs">
              <div className="flex items-center gap-3 font-mono text-slate-400">
                <span>Latency: <strong className="text-slate-200">{currentJob?.latency_ms ? `${Math.round(currentJob.latency_ms)}ms` : '—'}</strong></span>
                <span>•</span>
                <span>Cost: <strong className="text-emerald-400">${currentJob?.cost_usd?.toFixed(4) || '0.0000'}</strong></span>
              </div>
              <a href={completedAsset.public_url} download={`transformed_${completedAsset.id.slice(0, 8)}.png`}>
                <Button size="sm" variant="primary">
                  <Download className="w-3.5 h-3.5 mr-1" /> Download Result
                </Button>
              </a>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
