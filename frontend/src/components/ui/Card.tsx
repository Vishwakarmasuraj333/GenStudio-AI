import React from 'react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  bordered?: boolean;
}

export function Card({ className, bordered = true, children, ...props }: CardProps) {
  return (
    <div
      className={twMerge(
        clsx(
          "bg-[#11141D] rounded-xl p-5",
          bordered && "border border-[#1E2433]",
          className
        )
      )}
      {...props}
    >
      {children}
    </div>
  );
}
