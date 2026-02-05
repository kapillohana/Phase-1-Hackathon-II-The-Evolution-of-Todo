'use client';

import { Moon, Sun } from 'lucide-react';
import { useTheme } from 'next-themes';

import { Button } from '@/components/ui/button';

export function ThemeToggle() {
  const { theme, setTheme } = useTheme();

  return (
    <Button
      variant="ghost"
      size="icon"
      onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
      aria-label="Toggle theme"
      className="relative rounded-full p-2 transition-all duration-300 hover:bg-gray-200 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
    >
      <div className="relative w-6 h-6">
        <Sun
          className="absolute h-5 w-5 rotate-0 scale-100 transition-all duration-300 text-yellow-500 dark:-rotate-90 dark:scale-0"
        />
        <Moon
          className="absolute h-5 w-5 rotate-90 scale-0 transition-all duration-300 text-gray-700 dark:rotate-0 dark:scale-100 dark:text-gray-300"
        />
      </div>
    </Button>
  );
}