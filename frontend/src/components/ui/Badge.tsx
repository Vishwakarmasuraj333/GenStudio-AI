import React from 'react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: 'emerald' | 'teal' | 'amber' | 'rose' | 'slate';
}

export function Badge({ className, variant = 'slate', children, ...props }: BadgeProps) {
  const variants = {
    emerald: "bg-emerald-950/60 text-emerald-400 border-emerald-800/40",
    teal: "bg-teal-950/60 text-teal-400 border-teal-800/40",
    amber: "bg-amber-950/60 text-amber-400 border-amber-800/40",
    rose: "bg-rose-950/60 text-rose-400 border-rose-800/40",
    slate: "bg-slate-800/60 text-slate-300 border-slate-700/50"
  };

  return (
    <span
      className={twMerge(
        clsx(
          "inline-flex items-center px-2 py-0.5 rounded text-xs font-medium border",
          variants[variant],
          className
        )
      )}
      {...props}
    >
      {children}
    </span>

  );
}
