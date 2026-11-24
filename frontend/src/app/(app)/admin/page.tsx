'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useAuth } from '@/lib/auth';
import { apiFetch } from '@/lib/api';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { Shield, Users, Database, Activity, CheckCircle2, AlertTriangle, ArrowLeft } from 'lucide-react';

export default function AdminDashboardPage() {
  const { user } = useAuth();
  const [users, setUsers] = useState<any[]>([]);
  const [models, setModels] = useState<any[]>([]);
  const [auditLogs, setAuditLogs] = useState<any[]>([]);
  const [health, setHealth] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [actionMessage, setActionMessage] = useState<string | null>(null);

  useEffect(() => {
    if (!user) return;
    if (user.role !== 'ADMIN' && user.role !== 'OWNER') {
      setLoading(false);
      return;
    }

    Promise.all([
      apiFetch<any[]>('/admin/users').catch(() => []),
      apiFetch<any[]>('/admin/models').catch(() => []),
      apiFetch<any[]>('/admin/audit-logs').catch(() => []),
      apiFetch<any>('/admin/health').catch(() => null)
    ]).then(([uData, mData, lData, hData]) => {
      setUsers(uData);
      setModels(mData);
      setAuditLogs(lData);
      setHealth(hData);
      setLoading(false);
    }).catch((e) => {
      console.error(e);
      setLoading(false);
    });
  }, [user]);

  const toggleModel = async (modelId: string) => {
    try {
      await apiFetch(`/admin/models/${encodeURIComponent(modelId)}/toggle`, { method: 'PUT' });
      const updated = await apiFetch<any[]>('/admin/models');
      setModels(updated);
      setActionMessage(`Toggled model status for ${modelId}`);
      setTimeout(() => setActionMessage(null), 3000);
    } catch (e: any) {
      console.error(e);
    }
  };

  if (!loading && user && user.role !== 'ADMIN' && user.role !== 'OWNER') {
    return (
      <div className="max-w-2xl mx-auto py-16 text-center space-y-4">
        <div className="w-12 h-12 rounded-full bg-rose-950/60 border border-rose-800/50 flex items-center justify-center mx-auto text-rose-400">
          <Shield className="w-6 h-6" />
        </div>
        <h2 className="text-xl font-bold text-white">Administrative Access Required</h2>
        <p className="text-sm text-slate-400">
          Your current account role is <span className="font-mono text-emerald-400">{user.role}</span>. Access to the system governance dashboard requires ADMIN or OWNER privileges.
        </p>
        <Link href="/dashboard">
          <Button variant="secondary" size="md">
            <ArrowLeft className="w-4 h-4 mr-1.5" /> Return to Studio Dashboard
          </Button>
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      <div className="border-b border-[#1E2433] pb-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div>
          <h2 className="text-xl font-bold text-white">Administration & Governance</h2>
          <p className="text-xs text-slate-400">System telemetry, role-based access control, model registry, and verifiable audit trail</p>
        </div>
        <Badge variant="emerald">Admin Authorized</Badge>
      </div>

      {actionMessage && (
        <div className="p-3 bg-emerald-950/50 border border-emerald-800/50 rounded-lg text-xs font-mono text-emerald-300">
          {actionMessage}
        </div>
      )}

      {/* System Health */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <Card className="p-4 border-[#1E2433]">
          <div className="text-slate-400 text-xs font-mono">Service Status</div>
          <div className="text-xl font-bold text-emerald-400 font-mono mt-1">{health?.status || 'Active'}</div>
        </Card>
        <Card className="p-4 border-[#1E2433]">
          <div className="text-slate-400 text-xs font-mono">Total Users</div>
          <div className="text-xl font-bold text-white font-mono mt-1">{users.length}</div>
        </Card>
        <Card className="p-4 border-[#1E2433]">
          <div className="text-slate-400 text-xs font-mono">Registry Models</div>
          <div className="text-xl font-bold text-teal-400 font-mono mt-1">{models.length}</div>
        </Card>
        <Card className="p-4 border-[#1E2433]">
          <div className="text-slate-400 text-xs font-mono">Server Uptime</div>
          <div className="text-xl font-bold text-white font-mono mt-1">{health?.uptime_seconds ? `${Math.round(health.uptime_seconds)}s` : 'Active'}</div>
        </Card>
      </div>

      {/* Registered Users */}
      <Card className="p-0 border-[#1E2433] overflow-hidden">
        <div className="p-4 border-b border-[#1E2433] text-xs font-semibold text-white">
          User Accounts & RBAC Roles ({users.length})
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs min-w-[500px]">
            <thead className="bg-[#0C0E15] border-b border-[#1E2433] text-slate-400 font-mono">
              <tr>
                <th className="p-4">Name & Email</th>
                <th className="p-4">Role</th>
                <th className="p-4">Status</th>
                <th className="p-4">Registered Date</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#1E2433]">
              {users.map((u) => (
                <tr key={u.id} className="hover:bg-[#161B26]/30">
                  <td className="p-4 font-mono">
                    <div className="text-slate-200 font-semibold">{u.full_name || 'Anonymous'}</div>
                    <div className="text-slate-500 text-[10px]">{u.email}</div>
                  </td>
                  <td className="p-4">
                    <Badge variant={u.role === 'OWNER' ? 'amber' : u.role === 'ADMIN' ? 'teal' : 'slate'}>
                      {u.role}
                    </Badge>
                  </td>
                  <td className="p-4">
                    <span className={`text-[11px] font-mono ${u.is_active ? 'text-emerald-400' : 'text-rose-400'}`}>
                      {u.is_active ? 'Active' : 'Disabled'}
                    </span>
                  </td>
                  <td className="p-4 font-mono text-slate-500 text-[11px]">
                    {new Date(u.created_at).toLocaleDateString()}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>

      {/* Model Registry Management */}
      <Card className="p-0 border-[#1E2433] overflow-hidden">
        <div className="p-4 border-b border-[#1E2433] text-xs font-semibold text-white">
          Curated Model Registry ({models.length})
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs min-w-[600px]">
            <thead className="bg-[#0C0E15] border-b border-[#1E2433] text-slate-400 font-mono">
              <tr>
                <th className="p-4">Model & Provider</th>
                <th className="p-4">Task Types</th>
                <th className="p-4">Cost / Gen</th>
                <th className="p-4">Status</th>
                <th className="p-4 text-right">Toggle</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#1E2433]">
              {models.map((m) => (
                <tr key={m.id} className="hover:bg-[#161B26]/30">
                  <td className="p-4 font-mono">
                    <div className="font-semibold text-slate-200">{m.display_name}</div>
                    <div className="text-slate-500 text-[10px]">{m.model_id}</div>
                  </td>
                  <td className="p-4 text-slate-300 font-mono text-[11px]">{m.task_types.join(', ')}</td>
                  <td className="p-4 font-mono text-emerald-400">${m.pricing_json?.cost_per_gen_usd}</td>
                  <td className="p-4">
                    <Badge variant={m.is_enabled ? 'emerald' : 'rose'}>
                      {m.is_enabled ? 'Enabled' : 'Disabled'}
                    </Badge>
                  </td>
                  <td className="p-4 text-right">
                    <Button size="sm" variant="ghost" onClick={() => toggleModel(m.model_id)}>
                      {m.is_enabled ? 'Disable' : 'Enable'}
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>

      {/* Audit Logs */}
      <Card className="p-0 border-[#1E2433] overflow-hidden">
        <div className="p-4 border-b border-[#1E2433] text-xs font-semibold text-white">
          Security & Execution Audit Trail ({auditLogs.length} events)
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs min-w-[500px]">
            <thead className="bg-[#0C0E15] border-b border-[#1E2433] text-slate-400 font-mono">
              <tr>
                <th className="p-4">Action</th>
                <th className="p-4">Resource Type</th>
                <th className="p-4">User ID</th>
                <th className="p-4">Timestamp</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#1E2433]">
              {auditLogs.length === 0 ? (
                <tr>
                  <td colSpan={4} className="p-6 text-center text-slate-500 font-mono text-xs">
                    No audit records logged yet.
                  </td>
                </tr>
              ) : (
                auditLogs.slice(0, 15).map((log) => (
                  <tr key={log.id} className="hover:bg-[#161B26]/30">
                    <td className="p-4 font-mono font-semibold text-emerald-400 text-[11px]">
                      {log.action}
                    </td>
                    <td className="p-4 font-mono text-slate-300 text-[11px]">
                      {log.resource_type}
                    </td>
                    <td className="p-4 font-mono text-slate-500 text-[10px]">
                      {log.user_id ? log.user_id.slice(0, 8) + '...' : 'System'}
                    </td>
                    <td className="p-4 font-mono text-slate-500 text-[11px]">
                      {new Date(log.created_at).toLocaleString()}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}
