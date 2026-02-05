'use client';

import { AuthProvider } from '@/lib/auth';

export default function AppWrapper({ children }: { children: React.ReactNode }) {
  return (
    <AuthProvider>
      {children}
    </AuthProvider>
  );
}