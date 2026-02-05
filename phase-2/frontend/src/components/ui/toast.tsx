'use client';

import { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { CheckCircle, AlertCircle, XCircle, Info, X } from 'lucide-react';

type ToastType = 'success' | 'error' | 'info' | 'warning';

interface Toast {
  id: string;
  title: string;
  description?: string;
  type: ToastType;
}

const TOAST_TIMEOUT = 5000;

const getTypeConfig = (type: ToastType) => {
  switch (type) {
    case 'success':
      return {
        icon: CheckCircle,
        bgColor: 'bg-green-500',
        borderColor: 'border-green-500',
        textColor: 'text-green-700',
        darkTextColor: 'dark:text-green-400',
        iconColor: 'text-green-500',
      };
    case 'error':
      return {
        icon: XCircle,
        bgColor: 'bg-red-500',
        borderColor: 'border-red-500',
        textColor: 'text-red-700',
        darkTextColor: 'dark:text-red-400',
        iconColor: 'text-red-500',
      };
    case 'warning':
      return {
        icon: AlertCircle,
        bgColor: 'bg-yellow-500',
        borderColor: 'border-yellow-500',
        textColor: 'text-yellow-700',
        darkTextColor: 'dark:text-yellow-400',
        iconColor: 'text-yellow-500',
      };
    case 'info':
    default:
      return {
        icon: Info,
        bgColor: 'bg-blue-500',
        borderColor: 'border-blue-500',
        textColor: 'text-blue-700',
        darkTextColor: 'dark:text-blue-400',
        iconColor: 'text-blue-500',
      };
  }
};

// Global toast state
let toasts: Toast[] = [];
let listeners: ((toasts: Toast[]) => void)[] = [];

const addToast = (title: string, description?: string, type: ToastType = 'info'): string => {
  const id = Math.random().toString(36).substring(2, 9);
  const newToast: Toast = { id, title, description, type };
  
  toasts = [...toasts, newToast];
  notifyListeners();
  
  // Auto-remove toast after timeout
  setTimeout(() => {
    removeToast(id);
  }, TOAST_TIMEOUT);
  
  return id;
};

const removeToast = (id: string) => {
  toasts = toasts.filter(toast => toast.id !== id);
  notifyListeners();
};

const notifyListeners = () => {
  listeners.forEach(listener => listener(toasts));
};

export const toast = {
  success: (title: string, description?: string) => addToast(title, description, 'success'),
  error: (title: string, description?: string) => addToast(title, description, 'error'),
  info: (title: string, description?: string) => addToast(title, description, 'info'),
  warning: (title: string, description?: string) => addToast(title, description, 'warning'),
  dismiss: (id: string) => removeToast(id),
};

export const ToastProvider = ({ children }: { children: React.ReactNode }) => {
  const [toasts, setToasts] = useState<Toast[]>([]);

  useEffect(() => {
    const listener = (newToasts: Toast[]) => setToasts(newToasts);
    listeners.push(listener);
    
    return () => {
      listeners = listeners.filter(l => l !== listener);
    };
  }, []);

  return (
    <>
      {children}
      <div className="fixed top-4 right-4 z-[100] space-y-2 max-w-xs w-full">
        <AnimatePresence>
          {toasts.map((toast) => (
            <ToastItem key={toast.id} toast={toast} />
          ))}
        </AnimatePresence>
      </div>
    </>
  );
};

const ToastItem = ({ toast }: { toast: Toast }) => {
  const { icon: Icon, iconColor } = getTypeConfig(toast.type);

  return (
    <motion.div
      initial={{ opacity: 0, x: 300, scale: 0.8 }}
      animate={{ opacity: 1, x: 0, scale: 1 }}
      exit={{ opacity: 0, x: 300, scale: 0.8 }}
      transition={{ type: 'spring', damping: 25, stiffness: 300 }}
      className="flex items-start w-full max-w-sm p-4 mb-2 bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 overflow-hidden"
    >
      <div className={`flex-shrink-0 ${iconColor}`}>
        <Icon className="h-5 w-5" />
      </div>
      <div className="ml-3 flex-1">
        <p className="text-sm font-medium text-gray-900 dark:text-white">{toast.title}</p>
        {toast.description && (
          <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">{toast.description}</p>
        )}
      </div>
      <button
        onClick={() => removeToast(toast.id)}
        className="ml-4 flex-shrink-0 text-gray-400 hover:text-gray-500 dark:text-gray-500 dark:hover:text-gray-400"
      >
        <X className="h-4 w-4" />
      </button>
    </motion.div>
  );
};