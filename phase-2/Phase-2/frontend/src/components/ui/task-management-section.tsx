'use client';

import { motion } from 'framer-motion';
import { Calendar, Target, Repeat2, Flag, Clock, Users } from 'lucide-react';

const taskManagementFeatures = [
  {
    icon: Calendar,
    title: 'Smart Scheduling',
    description: 'Automatically schedule tasks based on priority and deadlines with intelligent time management.'
  },
  {
    icon: Target,
    title: 'Goal Setting',
    description: 'Break down large projects into manageable tasks with clear milestones and objectives.'
  },
  {
    icon: Repeat2,
    title: 'Recurring Tasks',
    description: 'Set up daily, weekly, or monthly recurring tasks that automatically appear when needed.'
  },
  {
    icon: Flag,
    title: 'Priority Management',
    description: 'Visually organize tasks by importance with color-coded priority levels and categories.'
  },
  {
    icon: Clock,
    title: 'Time Tracking',
    description: 'Monitor how much time you spend on each task to improve your productivity.'
  },
  {
    icon: Users,
    title: 'Team Collaboration',
    description: 'Assign tasks to team members and track progress in real-time with shared dashboards.'
  }
];

export function TaskManagementSection() {
  return (
    <section className="py-20 bg-white dark:bg-gray-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <motion.h2 
            className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5 }}
          >
            Powerful Task Management
          </motion.h2>
          <motion.p 
            className="text-lg text-gray-600 dark:text-gray-300 max-w-2xl mx-auto"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5, delay: 0.1 }}
          >
            Everything you need to organize, prioritize, and accomplish your goals
          </motion.p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {taskManagementFeatures.map((feature, index) => (
            <motion.div
              key={index}
              className="bg-gradient-to-br from-white to-gray-50 dark:from-gray-800 dark:to-gray-800/50 rounded-2xl p-6 shadow-lg hover:shadow-xl transition-all duration-300 border border-gray-100 dark:border-gray-700"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              whileHover={{ y: -5 }}
            >
              <div className="w-12 h-12 rounded-xl bg-gradient-to-r from-blue-500 to-indigo-500 flex items-center justify-center mb-4">
                <feature.icon className="w-6 h-6 text-white" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                {feature.title}
              </h3>
              <p className="text-gray-600 dark:text-gray-400">
                {feature.description}
              </p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}