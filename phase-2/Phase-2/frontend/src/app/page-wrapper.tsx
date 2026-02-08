'use client';

import HomePage from './page';
import RootProvider from '../components/RootProvider';

export default function PageWrapper() {
  return (
    <RootProvider>
      <HomePage />
    </RootProvider>
  );
}