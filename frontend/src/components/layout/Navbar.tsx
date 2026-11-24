'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useAuth } from '@/lib/auth';
import { Sparkles, Menu, X, ArrowRight } from 'lucide-react';
import { Button } from '../ui/Button';

export function Navbar() {
  const { user } = useAuth();
  const pathname = usePathname();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const navLinks = [
    { name: 'Features', href: '/features' },
    { name: 'Models & Registry', href: '/models' },
    { name: 'Research & Benchmarks', href: '/research' },
    { name: 'Pricing', href: '/pricing' },
  ];

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 border-b border-[#1E2433] bg-[#0A0C10]/95 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2.5 group">
          <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-emerald-500 to-teal-700 flex items-center justify-center shadow-lg shadow-emerald-950/40 group-hover:scale-105 transition-transform duration-200">
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          <div className="flex flex-col">
            <span className="font-bold text-lg text-white tracking-tight leading-none">
              GenStudio <span className="text-emerald-400">AI</span>
            </span>
            <span className="text-[10px] text-slate-400 font-mono tracking-wider">RESEARCH STUDIO</span>
          </div>
        </Link>

        {/* Desktop Navigation */}
        <div className="hidden md:flex items-center gap-7 text-sm font-medium text-slate-300">
          {navLinks.map((link) => {
            const isActive = pathname === link.href;
            return (
              <Link
                key={link.href}
                href={link.href}
                className={`transition-colors hover:text-emerald-400 py-1 border-b-2 ${
                  isActive ? 'border-emerald-400 text-emerald-400' : 'border-transparent text-slate-300'
                }`}
              >
                {link.name}
              </Link>
            );
          })}
        </div>

        {/* Desktop Actions */}
        <div className="hidden md:flex items-center gap-3">
          {user ? (
            <Link href="/dashboard">
              <Button size="sm" variant="primary">
                Enter Studio <ArrowRight className="w-3.5 h-3.5 ml-1.5" />
              </Button>
            </Link>
          ) : (
            <>
              <Link href="/login">
                <Button size="sm" variant="ghost">Sign In</Button>
              </Link>
              <Link href="/register">
                <Button size="sm" variant="primary">Create Account</Button>
              </Link>
            </>
          )}
        </div>

        {/* Mobile Hamburger Toggle Button */}
        <div className="flex md:hidden items-center gap-2">
          {user && (
            <Link href="/dashboard" className="sm:inline-block">
              <Button size="sm" variant="primary" className="text-xs px-2.5 py-1">Studio</Button>
            </Link>
          )}
          <button
            type="button"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            aria-label="Toggle navigation menu"
            aria-expanded={mobileMenuOpen}
            className="p-2 rounded-lg text-slate-400 hover:text-white hover:bg-[#161B26] focus:outline-none focus:ring-2 focus:ring-emerald-500 touch-target flex items-center justify-center"
          >
            {mobileMenuOpen ? <X className="w-5 h-5 text-emerald-400" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>
      </div>

      {/* Mobile Navigation Drawer */}
      {mobileMenuOpen && (
        <div className="md:hidden border-b border-[#1E2433] bg-[#0C0E15]/98 px-4 pt-3 pb-6 space-y-3 shadow-2xl animate-in slide-in-from-top-2 duration-200">
          <div className="flex flex-col space-y-1">
            {navLinks.map((link) => {
              const isActive = pathname === link.href;
              return (
                <Link
                  key={link.href}
                  href={link.href}
                  onClick={() => setMobileMenuOpen(false)}
                  className={`px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                    isActive
                      ? 'bg-emerald-950/50 text-emerald-400 border border-emerald-800/40 font-semibold'
                      : 'text-slate-300 hover:text-white hover:bg-[#161B26]'
                  }`}
                >
                  {link.name}
                </Link>
              );
            })}
          </div>

          <div className="pt-3 border-t border-[#1E2433] flex flex-col gap-2">
            {user ? (
              <Link href="/dashboard" onClick={() => setMobileMenuOpen(false)}>
                <Button size="md" variant="primary" className="w-full justify-center">
                  Enter Creative Studio <ArrowRight className="w-4 h-4 ml-1.5" />
                </Button>
              </Link>
            ) : (
              <>
                <Link href="/login" onClick={() => setMobileMenuOpen(false)}>
                  <Button size="md" variant="secondary" className="w-full justify-center">
                    Sign In
                  </Button>
                </Link>
                <Link href="/register" onClick={() => setMobileMenuOpen(false)}>
                  <Button size="md" variant="primary" className="w-full justify-center">
                    Create Account
                  </Button>
                </Link>
              </>
            )}
          </div>
        </div>
      )}
    </nav>
  );
}
