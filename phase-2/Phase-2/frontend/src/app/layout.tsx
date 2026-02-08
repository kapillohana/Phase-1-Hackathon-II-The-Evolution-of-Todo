import './globals.css';
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import { ThemeProvider } from '@/components/providers/theme-provider';
import { AuthProvider } from '@/lib/auth';
import { Navbar } from '@/components/ui/navbar';
import { ToastProvider } from '@/components/ui/toast';

export const metadata: Metadata = {
  title: 'Advanced Todo App',
  description: 'A full-featured todo application with advanced features',
};

export const viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 1,
  userScalable: false,
}

const inter = Inter({ subsets: ['latin'] });

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${inter.className} bg-gradient-to-br from-gray-50 to-gray-100 text-gray-900 antialiased dark:from-gray-900 dark:to-gray-950 dark:text-gray-100 min-h-screen w-full`}>
        <ThemeProvider
          attribute="class"
          defaultTheme="system"
          enableSystem
          disableTransitionOnChange
        >
          <AuthProvider>
            <ToastProvider>
              {/* Skip link for accessibility */}
              <a
                href="#main-content"
                className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50 focus:bg-primary-600 focus:text-white focus:px-4 focus:py-2 focus:rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
              >
                Skip to main content
              </a>

              <div id="__next" className="w-full">
                <Navbar />
                {/* Main content - Full width for dashboard */}
                <main id="main-content" className="w-full">
                  <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    {children}
                  </div>
                </main>

                {/* Footer */}
                <footer className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm border-t border-white/20 dark:border-gray-700/50 py-6 mt-12">
                  <div className="container mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex flex-col md:flex-row justify-between items-center">
                      <p className="text-gray-600 dark:text-gray-400 text-sm">
                        © {new Date().getFullYear()} Advanced Todo App. All rights reserved.
                      </p>
                      <div className="mt-4 md:mt-0 flex space-x-6">
                        <a
                          href="/privacy"
                          className="text-gray-600 hover:text-blue-600 dark:text-gray-400 dark:hover:text-blue-400 text-sm transition-colors"
                        >
                          Privacy
                        </a>
                        <a
                          href="/terms"
                          className="text-gray-600 hover:text-blue-600 dark:text-gray-400 dark:hover:text-blue-400 text-sm transition-colors"
                        >
                          Terms
                        </a>
                      </div>
                    </div>
                  </div>
                </footer>
              </div>
            </ToastProvider>
          </AuthProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}