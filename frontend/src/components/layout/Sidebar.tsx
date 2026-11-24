'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useAuth } from '@/lib/auth';
import {
  Sparkles, Image, Video, Wand2, FolderKanban, Library,
  History, FlaskConical, BarChart3, Settings, Shield,
  LogOut, LayoutDashboard, X
} from 'lucide-react';
import { clsx } from 'clsx';

interface SidebarProps {
  mobileOpen?: boolean;
  onMobileClose?: () => void;
}

export function Sidebar({ mobileOpen = false, onMobileClose }: SidebarProps) {
  const pathname = usePathname();
  const { user, logout } = useAuth();

  const studioLinks = [
    { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
    { name: 'Image Studio', href: '/studio/image', icon: Image },
    { name: 'Video Studio', href: '/studio/video', icon: Video },
    { name: 'Transform & Edit', href: '/studio/edit', icon: Wand2 },
  ];

  const workspaceLinks = [
    { name: 'Projects', href: '/projects', icon: FolderKanban },
    { name: 'Media Library', href: '/library', icon: Library },
    { name: 'Generation History', href: '/history', icon: History },
  ];

  const researchLinks = [
    { name: 'Research & Benchmarks', href: '/experiments', icon: FlaskConical },
    { name: 'Usage & Cost Tracker', href: '/usage', icon: BarChart3 },
    { name: 'Settings', href: '/settings', icon: Settings },
  ];

  const adminLinks = [
    { name: 'Admin Console', href: '/admin', icon: Shield },
  ];

  const renderNavGroup = (title: string, links: typeof studioLinks) => (
    <div className="mb-6">
      <div className="px-3 mb-2 text-[11px] font-semibold tracking-wider text-slate-500 uppercase font-mono">
        {title}
      </div>
      <div className="space-y-1">
        {links.map((link) => {
          const Icon = link.icon;
          const isActive = pathname === link.href || (link.href !== '/dashboard' && pathname.startsWith(link.href));
          return (
            <Link
              key={link.href}
              href={link.href}
              onClick={() => onMobileClose?.()}
              className={clsx(
                "flex items-center gap-3 px-3 py-2.5 rounded-lg text-xs font-medium transition-all group touch-target",
                isActive
                  ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-semibold"
                  : "text-slate-400 hover:text-slate-200 hover:bg-[#161B26]"
              )}
            >
              <Icon className={clsx("w-4 h-4 transition-colors flex-shrink-0", isActive ? "text-emerald-400" : "text-slate-400 group-hover:text-slate-200")} />
              <span>{link.name}</span>
            </Link>
          );
        })}
      </div>
    </div>
  );

  const sidebarContent = (
    <>
      {/* Brand Header */}
      <div className="h-16 flex items-center justify-between px-5 border-b border-[#1E2433]">
        <Link href="/dashboard" onClick={() => onMobileClose?.()} className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-emerald-500 to-teal-700 flex items-center justify-center shadow-md shadow-emerald-950">
            <Sparkles className="w-4 h-4 text-white" />
          </div>
          <div className="flex flex-col">
            <span className="font-bold text-base text-white tracking-tight leading-none">
              GenStudio <span className="text-emerald-400">AI</span>
            </span>
            <span className="text-[9px] text-slate-500 font-mono tracking-widest uppercase">M.Sc. IT Major</span>
          </div>
        </Link>
        {onMobileClose && (
          <button
            onClick={onMobileClose}
            aria-label="Close navigation"
            className="lg:hidden p-1.5 text-slate-400 hover:text-white rounded-lg hover:bg-[#1E2433]"
          >
            <X className="w-5 h-5 text-slate-400" />
          </button>
        )}
      </div>

      {/* Navigation Links */}
      <div className="flex-1 overflow-y-auto px-3 py-5">
        {renderNavGroup('Generation Studio', studioLinks)}
        {renderNavGroup('Creative Workspace', workspaceLinks)}
        {renderNavGroup('Academic Research', researchLinks)}

        {(user?.role === 'ADMIN' || user?.role === 'OWNER') &&
          renderNavGroup('Governance', adminLinks)}
      </div>

      {/* User Footer */}
      <div className="p-3 border-t border-[#1E2433] bg-[#090B0F]">
        <div className="flex items-center justify-between p-2 rounded-lg bg-[#121622] border border-[#1A2030]">
          <div className="flex items-center gap-2.5 min-w-0">
            <div className="w-7 h-7 rounded-full bg-emerald-950 border border-emerald-700/50 flex items-center justify-center text-xs font-semibold text-emerald-300">
              {user?.full_name?.charAt(0) || user?.email.charAt(0) || 'U'}
            </div>
            <div className="min-w-0">
              <p className="text-xs font-medium text-slate-200 truncate">{user?.full_name || 'Researcher'}</p>
              <p className="text-[10px] text-slate-500 font-mono uppercase">{user?.role || 'USER'}</p>
            </div>
          </div>
          <button
            onClick={logout}
            title="Sign out"
            aria-label="Sign out"
            className="p-1.5 text-slate-400 hover:text-rose-400 hover:bg-rose-950/30 rounded transition-colors"
          >
            <LogOut className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>
    </>
  );

  return (
    <>
      {/* Desktop Static Sidebar */}
      <aside className="w-64 border-r border-[#1E2433] bg-[#0C0E15] hidden lg:flex flex-col h-screen fixed left-0 top-0 bottom-0 z-40">
        {sidebarContent}
      </aside>

      {/* Mobile Drawer Backdrop & Sidebar */}
      {mobileOpen && (
        <div className="fixed inset-0 z-50 lg:hidden flex">
          <div
            className="fixed inset-0 bg-black/75 backdrop-blur-sm transition-opacity"
            onClick={onMobileClose}
            aria-hidden="true"
          />
          <aside className="relative w-72 max-w-[85vw] border-r border-[#1E2433] bg-[#0C0E15] flex flex-col h-full z-50 shadow-2xl animate-in slide-in-from-left duration-200">
            {sidebarContent}
          </aside>
        </div>
      )}
    </>
  );
}
