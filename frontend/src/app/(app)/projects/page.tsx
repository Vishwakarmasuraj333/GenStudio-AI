'use client';

import React, { useState, useEffect } from 'react';
import { apiFetch, ApiError } from '@/lib/api';
import { Button } from '@/components/ui/Button';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { FolderKanban, Plus, Trash2, Calendar, FileText, AlertCircle } from 'lucide-react';

export default function ProjectsPage() {
  const [projects, setProjects] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [creating, setCreating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchProjects = async () => {
    try {
      const data = await apiFetch<any[]>('/projects/');
      setProjects(data);
    } catch (err: any) {
      setError(err instanceof ApiError ? err.message : 'Failed to fetch projects.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProjects();
  }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim()) return;
    setCreating(true);
    setError(null);
    try {
      await apiFetch('/projects/', {
        method: 'POST',
        body: JSON.stringify({ name, description })
      });
      setName('');
      setDescription('');
      fetchProjects();
    } catch (err: any) {
      setError(err instanceof ApiError ? err.message : 'Failed to create project.');
    } finally {
      setCreating(false);
    }
  };

  const handleDelete = async (id: string) => {
    if (!confirm('Are you sure you want to delete this project?')) return;
    try {
      await apiFetch(`/projects/${id}`, { method: 'DELETE' });
      fetchProjects();
    } catch (err: any) {
      setError(err instanceof ApiError ? err.message : 'Failed to delete project.');
    }
  };

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      <div className="flex items-center justify-between border-b border-[#1E2433] pb-4">
        <div>
          <h2 className="text-xl font-bold text-white">Project Workspaces</h2>
          <p className="text-xs text-slate-400">Organize generation experiments and outputs into research collections</p>
        </div>
      </div>

      {error && (
        <div className="p-3.5 rounded-xl bg-rose-950/40 border border-rose-800/40 text-rose-300 text-xs flex items-center gap-2">
          <AlertCircle className="w-4 h-4 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Create Project Form */}
        <div className="lg:col-span-1">
          <Card className="p-5 border-[#1E2433]">
            <h3 className="text-sm font-semibold text-white mb-3">Create New Project</h3>
            <form onSubmit={handleCreate} className="space-y-4">
              <div>
                <label className="text-xs text-slate-300 block mb-1">Project Name</label>
                <input
                  type="text"
                  required
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="e.g. Diffusion Latency Study"
                  className="w-full p-2.5 bg-[#0C0E15] border border-[#1E2433] rounded-lg text-xs text-slate-200 focus:outline-none focus:border-emerald-500"
                />
              </div>

              <div>
                <label className="text-xs text-slate-300 block mb-1">Description (Optional)</label>
                <textarea
                  rows={3}
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  placeholder="Goals, target models, prompt parameters..."
                  className="w-full p-2.5 bg-[#0C0E15] border border-[#1E2433] rounded-lg text-xs text-slate-200 focus:outline-none focus:border-emerald-500"
                />
              </div>

              <Button type="submit" variant="primary" loading={creating} className="w-full">
                <Plus className="w-4 h-4 mr-1.5" /> Create Project
              </Button>
            </form>
          </Card>
        </div>

        {/* Project List */}
        <div className="lg:col-span-2">
          {loading ? (
            <div className="text-xs font-mono text-slate-500 p-8 text-center">Loading project workspaces...</div>
          ) : projects.length === 0 ? (
            <Card className="p-10 text-center border-[#1E2433] text-slate-500">
              <FolderKanban className="w-8 h-8 mx-auto mb-2 text-slate-600" />
              <p className="text-xs">No projects created yet. Start by creating your first workspace.</p>
            </Card>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {projects.map((p) => (
                <Card key={p.id} className="p-5 border-[#1E2433] flex flex-col justify-between hover:border-emerald-500/30 transition-all">
                  <div>
                    <div className="flex items-center justify-between mb-2">
                      <h4 className="font-semibold text-sm text-white">{p.name}</h4>
                      <button
                        onClick={() => handleDelete(p.id)}
                        className="text-slate-500 hover:text-rose-400 p-2 min-h-[36px] min-w-[36px] flex items-center justify-center rounded-lg hover:bg-rose-500/10 transition-colors"
                        title="Delete project"
                        aria-label="Delete project"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                    {p.description && (
                      <p className="text-xs text-slate-400 mb-4 line-clamp-2">{p.description}</p>
                    )}
                  </div>

                  <div className="border-t border-[#1E2433] pt-3 flex items-center justify-between text-[11px] font-mono text-slate-500">
                    <span>{p.job_count} jobs • {p.asset_count} assets</span>
                    <span>{new Date(p.created_at).toLocaleDateString()}</span>
                  </div>
                </Card>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
