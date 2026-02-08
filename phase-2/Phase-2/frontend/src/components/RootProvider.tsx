'use client';

import { AuthProvider } from '@/lib/auth';
import { useState, useEffect } from 'react';

interface RootProviderProps {
  children: React.ReactNode;
}

export default function RootProvider({ children }: RootProviderProps) {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    // Check for saved theme preference or system preference on client side
    const savedTheme = localStorage.getItem('theme');
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

    if (savedTheme === 'dark' || (!savedTheme && systemPrefersDark)) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }

    setMounted(true);
  }, []);

  if (!mounted) {
    return <>{children}</>; // Render children without providers during SSR
  }

  return (
    <AuthProvider>
      {children}
    </AuthProvider>
  );
}