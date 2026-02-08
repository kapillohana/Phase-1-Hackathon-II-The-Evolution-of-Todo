'use client';

import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { Play, CheckCircle, Star } from 'lucide-react';

export function HeroSection() {
  return (
    <section className="relative py-20 md:py-32 overflow-hidden">
      {/* Animated background elements */}
      <div className="absolute inset-0 bg-gradient-to-br from-blue-50 via-white to-indigo-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900"></div>

      {/* Floating shapes */}
      <div className="absolute top-20 left-10 w-24 h-24 bg-gradient-to-br from-blue-200/30 to-indigo-300/30 dark:from-blue-900/20 dark:to-indigo-900/20 rounded-full mix-blend-multiply filter blur-xl animate-blob"></div>
      <div className="absolute top-40 right-10 w-24 h-24 bg-gradient-to-br from-indigo-200/30 to-purple-300/30 dark:from-indigo-900/20 dark:to-purple-900/20 rounded-full mix-blend-multiply filter blur-xl animate-blob animation-delay-2000"></div>
      <div className="absolute bottom-20 left-1/3 w-24 h-24 bg-gradient-to-br from-slate-200/30 to-gray-300/30 dark:from-slate-900/20 dark:to-gray-900/20 rounded-full mix-blend-multiply filter blur-xl animate-blob animation-delay-4000"></div>

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="inline-block mb-4"
          >
            <span className="inline-flex items-center px-4 py-2 rounded-full text-sm font-medium bg-gradient-to-r from-blue-100 to-indigo-100 text-blue-800 dark:from-blue-900/30 dark:to-indigo-900/30 dark:text-blue-300 border border-blue-200 dark:border-blue-800">
              <Star className="w-4 h-4 mr-2 text-yellow-500" />
              Productivity Redefined
            </span>
          </motion.div>

          <motion.h1
            className="text-4xl md:text-6xl lg:text-7xl font-bold bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 bg-clip-text text-transparent mb-6"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.1 }}
          >
            Master Your Tasks
            <br />
            <span className="text-gray-900 dark:text-white">with AI-Powered</span>
          </motion.h1>

          <motion.p
            className="text-lg md:text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto mb-10"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
          >
            The most intuitive and powerful todo app designed to boost your productivity with smart features, beautiful UI, and AI-powered insights that adapt to your workflow.
          </motion.p>

          <motion.div
            className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-12"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.3 }}
          >
            <Button
              size="lg"
              className="px-8 py-4 text-lg rounded-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105"
            >
              Get Started Free
            </Button>

            <Button
              size="lg"
              variant="outline"
              className="px-8 py-4 text-lg rounded-full border-2 border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-all duration-300 flex items-center"
            >
              <Play className="w-5 h-5 mr-2" />
              Watch Demo
            </Button>
          </motion.div>

          {/* Stats section */}
          <motion.div
            className="flex flex-wrap justify-center gap-8 mb-16"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.4 }}
          >
            <div className="text-center">
              <div className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white">10K+</div>
              <div className="text-gray-600 dark:text-gray-400">Active Users</div>
            </div>
            <div className="text-center">
              <div className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white">99.9%</div>
              <div className="text-gray-600 dark:text-gray-400">Uptime</div>
            </div>
            <div className="text-center">
              <div className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white">50%</div>
              <div className="text-gray-600 dark:text-gray-400">More Productive</div>
            </div>
          </motion.div>
        </div>

        {/* Dashboard preview */}
        <motion.div
          className="mt-16 md:mt-24"
          initial={{ opacity: 0, y: 40, scale: 0.9 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          transition={{ duration: 0.8, delay: 0.5 }}
        >
          <div className="relative">
            <div className="absolute -inset-4 bg-gradient-to-r from-blue-600/20 to-indigo-600/20 rounded-3xl blur-xl opacity-50"></div>
            <div className="relative bg-white/80 dark:bg-gray-800/80 backdrop-blur-lg rounded-3xl shadow-2xl p-6 max-w-6xl mx-auto border border-gray-200 dark:border-gray-700">
              <div className="aspect-video bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-800 dark:to-gray-900 rounded-2xl p-6">
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 h-full">
                  {/* Left panel - Tasks */}
                  <div className="bg-white dark:bg-gray-700/50 rounded-xl p-4 shadow-sm">
                    <div className="flex items-center justify-between mb-4">
                      <h3 className="font-semibold text-gray-900 dark:text-white">Today's Tasks</h3>
                      <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                    </div>
                    <div className="space-y-3">
                      {[1, 2, 3].map((item) => (
                        <div key={item} className="flex items-center p-3 bg-gray-50 dark:bg-gray-600/30 rounded-lg">
                          <div className="w-5 h-5 border-2 border-gray-300 dark:border-gray-500 rounded-full mr-3"></div>
                          <span className="text-gray-700 dark:text-gray-300 text-sm">Task {item} description</span>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Middle panel - Analytics */}
                  <div className="bg-white dark:bg-gray-700/50 rounded-xl p-4 shadow-sm">
                    <h3 className="font-semibold text-gray-900 dark:text-white mb-4">Productivity</h3>
                    <div className="space-y-4">
                      <div>
                        <div className="flex justify-between text-sm mb-1">
                          <span className="text-gray-600 dark:text-gray-400">Completion Rate</span>
                        </div>
                        <div className="w-full bg-gray-200 dark:bg-gray-600 rounded-full h-2">
                          <div className="bg-gradient-to-r from-blue-500 to-indigo-500 h-2 rounded-full" style={{width: '75%'}}></div>
                        </div>
                      </div>

                      <div className="grid grid-cols-2 gap-4">
                        <div className="text-center p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                          <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">24</div>
                          <div className="text-xs text-gray-600 dark:text-gray-400">Tasks Done</div>
                        </div>
                        <div className="text-center p-3 bg-indigo-50 dark:bg-indigo-900/20 rounded-lg">
                          <div className="text-2xl font-bold text-indigo-600 dark:text-indigo-400">12</div>
                          <div className="text-xs text-gray-600 dark:text-gray-400">Remaining</div>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Right panel - Quick Actions */}
                  <div className="bg-white dark:bg-gray-700/50 rounded-xl p-4 shadow-sm">
                    <h3 className="font-semibold text-gray-900 dark:text-white mb-4">Quick Actions</h3>
                    <div className="space-y-3">
                      <button className="w-full p-3 bg-gradient-to-r from-blue-500 to-indigo-500 text-white rounded-lg text-sm font-medium hover:opacity-90 transition-opacity">
                        Add New Task
                      </button>
                      <button className="w-full p-3 bg-gray-100 dark:bg-gray-600 text-gray-700 dark:text-gray-300 rounded-lg text-sm font-medium hover:bg-gray-200 dark:hover:bg-gray-500 transition-colors">
                        Set Reminder
                      </button>
                      <button className="w-full p-3 bg-gray-100 dark:bg-gray-600 text-gray-700 dark:text-gray-300 rounded-lg text-sm font-medium hover:bg-gray-200 dark:hover:bg-gray-500 transition-colors">
                        View Analytics
                      </button>
                    </div>

                    <div className="mt-6 p-3 bg-gradient-to-r from-indigo-500/10 to-purple-500/10 dark:from-indigo-900/20 dark:to-purple-900/20 rounded-lg border border-indigo-200 dark:border-indigo-800">
                      <div className="flex items-center">
                        <CheckCircle className="w-5 h-5 text-indigo-500 dark:text-indigo-400 mr-2" />
                        <span className="text-sm text-gray-700 dark:text-gray-300">AI Suggestion: Focus on high-priority tasks</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}