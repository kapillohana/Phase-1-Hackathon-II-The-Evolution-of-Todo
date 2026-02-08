'use client';

import { motion } from 'framer-motion';
import { BookOpen, Cpu, Database, Globe, Github, Zap } from 'lucide-react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';

export default function AboutPage() {
  const techStack = [
    { name: 'Next.js', icon: Globe, description: 'React framework for production' },
    { name: 'FastAPI', icon: Zap, description: 'Modern, fast web framework' },
    { name: 'Neon', icon: Database, description: 'Serverless Postgres' },
    { name: 'SQLModel', icon: Cpu, description: 'SQL databases with Python' },
    { name: 'Tailwind CSS', icon: BookOpen, description: 'Utility-first CSS framework' },
    { name: 'Framer Motion', icon: Zap, description: 'Production-ready animation' },
  ];

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12"
    >
      <div className="text-center mb-16">
        <motion.h1
          className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-6"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          About TodoAI
        </motion.h1>

        <motion.p
          className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto mb-8"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
        >
          We're on a mission to revolutionize task management with AI-powered insights and a beautifully crafted user experience.
        </motion.p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center mb-16">
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Our Mission</h2>
          <p className="text-gray-600 dark:text-gray-300 mb-4">
            At TodoAI, we believe that effective task management should be intuitive, intelligent, and inspiring.
            Our platform leverages cutting-edge technology to help you achieve more with less effort.
          </p>
          <p className="text-gray-600 dark:text-gray-300 mb-4">
            We're committed to building tools that adapt to your workflow, not the other way around.
            Our AI-powered features learn from your habits to provide personalized recommendations and insights.
          </p>
          <p className="text-gray-600 dark:text-gray-300">
            Join thousands of users who have transformed their productivity with our innovative approach to task management.
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
          className="bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-gray-800 dark:to-gray-900 rounded-2xl p-8 border border-gray-200 dark:border-gray-700"
        >
          <div className="text-center">
            <div className="text-5xl mb-4">🎯</div>
            <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">Smart Productivity</h3>
            <p className="text-gray-600 dark:text-gray-300">
              Intelligent task prioritization and deadline management powered by AI algorithms.
            </p>
          </div>
        </motion.div>
      </div>

      <div className="mb-16">
        <motion.h2
          className="text-3xl font-bold text-gray-900 dark:text-white mb-8 text-center"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
        >
          Tech Stack
        </motion.h2>

        <motion.div
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.5 }}
        >
          {techStack.map((tech, index) => (
            <motion.div
              key={index}
              className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg border border-gray-100 dark:border-gray-700 hover:shadow-xl transition-shadow duration-300"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.1 * index }}
              whileHover={{ y: -5 }}
            >
              <div className="w-12 h-12 rounded-full bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center mb-4">
                <tech.icon className="w-6 h-6 text-blue-600 dark:text-blue-400" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                {tech.name}
              </h3>
              <p className="text-gray-600 dark:text-gray-400 text-sm">
                {tech.description}
              </p>
            </motion.div>
          ))}
        </motion.div>
      </div>

      <motion.div
        className="text-center"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.8 }}
      >
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Want to contribute?</h2>
        <p className="text-gray-600 dark:text-gray-300 mb-6 max-w-2xl mx-auto">
          TodoAI is an open-source project. Check out our repository and join our community of contributors.
        </p>

        <Link href="https://github.com/your-repo/todoai" target="_blank" rel="noopener noreferrer">
          <Button size="lg" className="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white">
            <Github className="w-5 h-5 mr-2" />
            View on GitHub
          </Button>
        </Link>
      </motion.div>
    </motion.div>
  );
}