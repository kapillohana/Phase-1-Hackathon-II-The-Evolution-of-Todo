'use client';

import { motion } from 'framer-motion';
import { CheckCircle, Users, Clock, TrendingUp } from 'lucide-react';

const stats = [
  {
    icon: CheckCircle,
    value: '99.9%',
    label: 'Task Completion Rate',
    description: 'Higher than average productivity'
  },
  {
    icon: Users,
    value: '10K+',
    label: 'Active Users',
    description: 'Trusted by professionals worldwide'
  },
  {
    icon: Clock,
    value: '50%',
    label: 'Time Saved',
    description: 'Average time saved per week'
  },
  {
    icon: TrendingUp,
    value: '3x',
    label: 'Faster Completion',
    description: 'Tasks completed faster'
  }
];

export function StatsSection() {
  return (
    <section className="py-12 bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-gray-900 dark:to-gray-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
          {stats.map((stat, index) => (
            <motion.div
              key={index}
              className="text-center"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
            >
              <div className="w-12 h-12 mx-auto mb-2 rounded-full bg-gradient-to-r from-blue-500 to-indigo-500 flex items-center justify-center">
                <stat.icon className="w-5 h-5 text-white" />
              </div>
              <div className="text-2xl md:text-3xl font-bold text-gray-900 dark:text-white mb-1">
                {stat.value}
              </div>
              <div className="text-xs md:text-sm text-gray-600 dark:text-gray-400">
                {stat.label}
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}