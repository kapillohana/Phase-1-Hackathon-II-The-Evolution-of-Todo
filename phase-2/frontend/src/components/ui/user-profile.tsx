'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { User, LogOut, Settings } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { useAuth } from '@/lib/auth';
import { useRouter } from 'next/navigation';

export function UserProfile() {
  // Safely get the auth context - handle if not available
  let authContext = null;
  let user = null;
  let signOut = null;

  try {
    authContext = useAuth();
    user = authContext.user;
    signOut = authContext.signOut;
  } catch (error) {
    // If not in an AuthProvider context, set defaults
    user = null;
    signOut = null;
  }

  const [isOpen, setIsOpen] = useState(false);
  const router = useRouter();

  const handleSignOut = async () => {
    if (!signOut) {
      console.error('Sign out function not available');
      return;
    }

    try {
      await signOut();
      router.push('/auth/signin');
    } catch (error) {
      console.error('Error signing out:', error);
    }
    setIsOpen(false);
  };

  if (!user) {
    return null;
  }

  return (
    <div className="relative">
      <Button
        variant="ghost"
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center space-x-2 p-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-700"
      >
        <div className="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center text-white text-sm font-medium">
          {user.email.charAt(0).toUpperCase()}
        </div>
        <span className="hidden md:inline text-sm font-medium text-gray-700 dark:text-gray-300">
          {user.email.split('@')[0]}
        </span>
      </Button>

      {isOpen && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -10 }}
          className="absolute right-0 mt-2 w-48 bg-white dark:bg-gray-800 rounded-md shadow-lg py-1 border border-gray-200 dark:border-gray-700 z-50"
        >
          <div className="px-4 py-2 border-b border-gray-100 dark:border-gray-700">
            <p className="text-sm font-medium text-gray-900 dark:text-white truncate">
              {user.email}
            </p>
          </div>
          <button
            onClick={() => {
              setIsOpen(false);
              router.push('/settings'); // Redirect to settings page when implemented
            }}
            className="flex items-center w-full px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
          >
            <Settings className="w-4 h-4 mr-2" />
            Settings
          </button>
          <button
            onClick={handleSignOut}
            className="flex items-center w-full px-4 py-2 text-sm text-red-600 dark:text-red-400 hover:bg-gray-100 dark:hover:bg-gray-700"
          >
            <LogOut className="w-4 h-4 mr-2" />
            Sign out
          </button>
        </motion.div>
      )}
    </div>
  );
}