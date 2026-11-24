'use client';

import React, { useState, useEffect } from 'react';
import { apiFetch } from '@/lib/api';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import { Library, Star, Download, Trash2, Image, Video, Eye, X, CheckCircle2 } from 'lucide-react';

export default function LibraryPage() {
  const [assets, setAssets] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [filterType, setFilterType] = useState<string>('all');
  const [favoritesOnly, setFavoritesOnly] = useState(false);
  const [activeAsset, setActiveAsset] = useState<any | null>(null);

  const fetchAssets = async () => {
    try {
      let url = '/library/?';
      if (filterType !== 'all') url += `media_type=${filterType}&`;
      if (favoritesOnly) url += 'favorites_only=true';
      const data = await apiFetch<any[]>(url);
      setAssets(data);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAssets();
  }, [filterType, favoritesOnly]);

  const toggleFavorite = async (id: string, e?: React.MouseEvent) => {
    e?.stopPropagation();
    await apiFetch(`/library/${id}/favorite`, { method: 'PUT' });
    if (activeAsset && activeAsset.id === id) {
      setActiveAsset({ ...activeAsset, is_favorite: !activeAsset.is_favorite });
    }
    fetchAssets();
  };

  const deleteAsset = async (id: string, e?: React.MouseEvent) => {
    e?.stopPropagation();
    if (!confirm('Are you sure you want to delete this media asset permanently?')) return;
    await apiFetch(`/library/${id}`, { method: 'DELETE' });
    if (activeAsset && activeAsset.id === id) {
      setActiveAsset(null);
    }
    fetchAssets();
  };

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-[#1E2433] pb-4">
        <div>
          <h2 className="text-xl font-bold text-white">Media Asset Library</h2>
          <p className="text-xs text-slate-400">All verified synthesized images and videos stored in object storage</p>
        </div>

        <div className="flex flex-wrap items-center gap-3 text-xs">
          <select
            value={filterType}
            onChange={(e) => setFilterType(e.target.value)}
            className="p-2 bg-[#0C0E15] border border-[#1E2433] rounded-lg text-slate-200"
          >
            <option value="all">All Media</option>
            <option value="image">Images Only</option>
            <option value="video">Videos Only</option>
          </select>

          <button
            onClick={() => setFavoritesOnly(!favoritesOnly)}
            className={`px-3 py-2 rounded-lg border flex items-center gap-1.5 transition-colors touch-target ${favoritesOnly ? 'bg-amber-950/60 border-amber-500 text-amber-400' : 'border-[#1E2433] text-slate-400'}`}
          >
            <Star className="w-3.5 h-3.5 fill-current" /> Favorites
          </button>
        </div>
      </div>

      {loading ? (
        <div className="text-xs font-mono text-slate-500 p-12 text-center">Loading media library...</div>
      ) : assets.length === 0 ? (
        <Card className="p-16 text-center border-[#1E2433] text-slate-500">
          <Library className="w-10 h-10 mx-auto mb-3 text-slate-600" />
          <p className="text-sm font-medium text-slate-400">No media assets found</p>
          <p className="text-xs mt-1">Generated images and videos will automatically appear in your library.</p>
        </Card>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          {assets.map((asset) => (
            <Card
              key={asset.id}
              onClick={() => setActiveAsset(asset)}
              className="p-2.5 border-[#1E2433] group relative overflow-hidden bg-[#0C0E15] hover:border-emerald-500/40 transition-all cursor-pointer flex flex-col justify-between"
            >
              <div className="aspect-square rounded-lg overflow-hidden relative bg-black flex items-center justify-center">
                {asset.media_type === 'video' ? (
                  <video src={asset.public_url} className="w-full h-full object-cover" muted playsInline />
                ) : (
                  <img src={asset.public_url} alt="Media" className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300" />
                )}

                {/* Desktop hover overlay */}
                <div className="hidden sm:flex absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity items-center justify-center gap-2">
                  <button
                    onClick={(e) => toggleFavorite(asset.id, e)}
                    aria-label="Toggle favorite"
                    className={`p-2 rounded-full ${asset.is_favorite ? 'bg-amber-500 text-black' : 'bg-white/20 text-white hover:bg-amber-500 hover:text-black'}`}
                  >
                    <Star className="w-3.5 h-3.5 fill-current" />
                  </button>
                  <a
                    href={asset.public_url}
                    download={`asset_${asset.id.slice(0, 8)}`}
                    onClick={(e) => e.stopPropagation()}
                    aria-label="Download asset"
                    className="p-2 rounded-full bg-white/20 text-white hover:bg-emerald-600"
                  >
                    <Download className="w-3.5 h-3.5" />
                  </a>
                  <button
                    onClick={(e) => deleteAsset(asset.id, e)}
                    aria-label="Delete asset"
                    className="p-2 rounded-full bg-white/20 text-white hover:bg-rose-600"
                  >
                    <Trash2 className="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>

              {/* Card Footer with Mobile Touch Friendly Controls */}
              <div className="pt-2 px-1 flex items-center justify-between text-[11px] font-mono text-slate-400">
                <span className="font-semibold text-slate-300">{asset.media_type.toUpperCase()}</span>
                <span>{(asset.file_size_bytes / 1024).toFixed(0)} KB</span>

                {/* Mobile action buttons (always visible on touch devices) */}
                <div className="flex sm:hidden items-center gap-1">
                  <button
                    onClick={(e) => toggleFavorite(asset.id, e)}
                    className={`p-1.5 rounded ${asset.is_favorite ? 'text-amber-400' : 'text-slate-400'}`}
                  >
                    <Star className="w-3.5 h-3.5 fill-current" />
                  </button>
                  <a
                    href={asset.public_url}
                    download={`asset_${asset.id.slice(0, 8)}`}
                    onClick={(e) => e.stopPropagation()}
                    className="p-1.5 text-slate-400 hover:text-emerald-400"
                  >
                    <Download className="w-3.5 h-3.5" />
                  </a>
                </div>
              </div>
            </Card>
          ))}
        </div>
      )}

      {/* Asset Inspection Modal */}
      {activeAsset && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-in fade-in duration-200">
          <div className="relative w-full max-w-3xl bg-[#0E121B] border border-[#1E2433] rounded-2xl p-6 shadow-2xl max-h-[90vh] overflow-y-auto space-y-4">
            <div className="flex items-center justify-between border-b border-[#1E2433] pb-3">
              <div className="flex items-center gap-2">
                <Badge variant={activeAsset.media_type === 'video' ? 'teal' : 'emerald'}>
                  {activeAsset.media_type.toUpperCase()}
                </Badge>
                <span className="text-xs font-mono text-slate-400">ID: {activeAsset.id.slice(0, 8)}</span>
              </div>
              <button
                onClick={() => setActiveAsset(null)}
                className="p-1 rounded-lg text-slate-400 hover:text-white hover:bg-[#1E2433]"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="flex items-center justify-center bg-black/50 rounded-xl overflow-hidden min-h-[300px] border border-[#1E2433]">
              {activeAsset.media_type === 'video' ? (
                <video src={activeAsset.public_url} controls playsInline autoPlay className="max-h-[500px] w-auto" />
              ) : (
                <img src={activeAsset.public_url} alt="Full view" className="max-h-[500px] w-auto object-contain" />
              )}
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs font-mono p-3 bg-[#0A0C10] rounded-xl border border-[#1E2433] text-slate-400">
              <div>Type: <strong className="text-slate-200">{activeAsset.mime_type}</strong></div>
              <div>Size: <strong className="text-slate-200">{(activeAsset.file_size_bytes / 1024).toFixed(1)} KB</strong></div>
              <div>SHA-256: <strong className="text-slate-200">{activeAsset.checksum_sha256.slice(0, 8)}...</strong></div>
              <div>Date: <strong className="text-slate-200">{new Date(activeAsset.created_at).toLocaleDateString()}</strong></div>
            </div>

            <div className="flex flex-wrap items-center justify-end gap-3 pt-2">
              <Button
                size="sm"
                variant="secondary"
                onClick={() => toggleFavorite(activeAsset.id)}
              >
                <Star className={`w-3.5 h-3.5 mr-1.5 ${activeAsset.is_favorite ? 'fill-amber-400 text-amber-400' : ''}`} />
                {activeAsset.is_favorite ? 'Favorited' : 'Favorite'}
              </Button>
              <a href={activeAsset.public_url} download={`asset_${activeAsset.id.slice(0, 8)}`}>
                <Button size="sm" variant="primary">
                  <Download className="w-3.5 h-3.5 mr-1.5" /> Download Media
                </Button>
              </a>
              <Button
                size="sm"
                variant="danger"
                onClick={() => deleteAsset(activeAsset.id)}
              >
                <Trash2 className="w-3.5 h-3.5 mr-1.5" /> Delete
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
