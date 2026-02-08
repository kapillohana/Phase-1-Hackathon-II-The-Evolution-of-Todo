'use client';

import { useState, useEffect } from 'react';
import { PublicNavbar } from '@/components/ui/public-navbar';
import { AuthenticatedNavbar } from '@/components/ui/authenticated-navbar';
import { useAuth } from '@/lib/auth';

export function Navbar() {
  const { user, isLoading } = useAuth();
  const [shouldRenderAuthenticated, setShouldRenderAuthenticated] = useState(false);

  useEffect(() => {
    if (!isLoading) {
      setShouldRenderAuthenticated(!!user);
    }
  }, [user, isLoading]);

  // During loading or if no user, show public navbar
  if (isLoading || !shouldRenderAuthenticated) {
    return <PublicNavbar />;
  }

  // If user is authenticated, show authenticated navbar
  return <AuthenticatedNavbar />;
}