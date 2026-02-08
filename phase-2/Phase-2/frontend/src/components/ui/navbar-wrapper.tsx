'use client';

import { AuthProvider } from '@/lib/auth';
import { Navbar } from '@/components/ui/navbar';

export function NavbarWithAuth() {
  return (
    <AuthProvider>
      <Navbar />
    </AuthProvider>
  );
}