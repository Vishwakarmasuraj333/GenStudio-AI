'use client';

import React, { useState } from 'react';
import { useAuth } from '@/lib/auth';
import { apiFetch, ApiError } from '@/lib/api';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Settings, Shield, KeyRound, User, CheckCircle2, AlertCircle } from 'lucide-react';

export default function SettingsPage() {
  const { user, refreshUser } = useAuth();
  const [fullName, setFullName] = useState(user?.full_name || '');
  const [password, setPassword] = useState('');
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setSaved(false);
    setError(null);

    try {
      await apiFetch('/auth/me', {
        method: 'PUT',
        body: JSON.stringify({
          full_name: fullName,
          password: password || undefined
        })
      });
      await refreshUser();
      setSaved(true);
      setPassword('');
    } catch (err: any) {
      setError(err instanceof ApiError ? err.message : 'Failed to update profile.');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="border-b border-[#1E2433] pb-4">
        <h2 className="text-xl font-bold text-white">Account & Environment Settings</h2>
        <p className="text-xs text-slate-400">Manage user credentials and review server-side secret architecture</p>
      </div>

      {error && (
        <div className="p-3.5 rounded-xl bg-rose-950/40 border border-rose-800/40 text-rose-300 text-xs flex items-center gap-2">
          <AlertCircle className="w-4 h-4 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="p-6 border-[#1E2433]">
          <h3 className="text-sm font-semibold text-white mb-4 flex items-center gap-2">
            <User className="w-4 h-4 text-emerald-400" /> Profile Information
          </h3>

          <form onSubmit={handleUpdate} className="space-y-4 text-xs">
            <div>
              <label className="text-slate-300 block mb-1">Email Address</label>
              <input
                type="text"
                disabled
                value={user?.email || ''}
                className="w-full p-2.5 bg-[#0C0E15] border border-[#1E2433] rounded-lg text-slate-500 font-mono"
              />
            </div>

            <div>
              <label className="text-slate-300 block mb-1">Full Name</label>
              <input
                type="text"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                className="w-full p-2.5 bg-[#0C0E15] border border-[#1E2433] rounded-lg text-slate-200 focus:outline-none focus:border-emerald-500"
              />
            </div>

            <div>
              <label className="text-slate-300 block mb-1">New Password (leave blank to keep current)</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full p-2.5 bg-[#0C0E15] border border-[#1E2433] rounded-lg text-slate-200 focus:outline-none focus:border-emerald-500"
              />
            </div>

            <div className="flex items-center gap-3 pt-2">
              <Button type="submit" variant="primary" loading={saving}>
                Save Profile Changes
              </Button>
              {saved && (
                <span className="text-emerald-400 font-mono text-[11px] flex items-center gap-1">
                  <CheckCircle2 className="w-3.5 h-3.5" /> Saved successfully!
                </span>
              )}
            </div>
          </form>
        </Card>

        <Card className="p-6 border-[#1E2433] bg-[#0E121B] space-y-4">
          <h3 className="text-sm font-semibold text-white flex items-center gap-2">
            <KeyRound className="w-4 h-4 text-cyan-400" /> Server Secret Architecture
          </h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            Per GenStudio security specifications, third-party API keys (Hugging Face, Gemini) are stored strictly on the server in environment variables (<code className="text-slate-200">HF_API_TOKEN</code>, <code className="text-slate-200">GEMINI_API_KEY</code>).
          </p>
          <div className="p-3 rounded-lg bg-[#080A0F] border border-[#1E2433] font-mono text-[11px] text-slate-400 space-y-1">
            <div className="flex justify-between"><span>Password Hashing:</span><span className="text-emerald-400">Argon2id</span></div>
            <div className="flex justify-between"><span>Token Format:</span><span className="text-emerald-400">JWT HS256</span></div>
            <div className="flex justify-between"><span>Browser Key Exposure:</span><span className="text-emerald-400">0% (Zero secrets)</span></div>
          </div>
        </Card>
      </div>
    </div>
  );
}
