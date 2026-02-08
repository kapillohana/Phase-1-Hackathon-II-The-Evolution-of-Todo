'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { CalendarIcon, ClockIcon, TagIcon, ArrowPathIcon, CheckCircleIcon, XCircleIcon } from '@heroicons/react/24/outline';
import { CheckCircleIcon as CheckCircleSolidIcon } from '@heroicons/react/24/solid';
import clsx from 'clsx';
import { Task } from '@/lib/api'; // Adjust import path as needed

interface TaskItemProps {
  task: Task;
  onEdit: (task: Task) => void;
  onDelete: (taskId: number) => void;
  onToggleComplete: (taskId: number) => void;
}

export default function TaskItem({ task, onEdit, onDelete, onToggleComplete }: TaskItemProps) {
  const [isDeleting, setIsDeleting] = useState(false);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [isCompleted, setIsCompleted] = useState(task.completed);

  // Update local state when task prop changes
  useEffect(() => {
    setIsCompleted(task.completed);
  }, [task.completed]);

  const handleToggleComplete = () => {
    setIsCompleted(!isCompleted);
    onToggleComplete(task.id);
  };

  const handleDeleteClick = () => {
    if (showDeleteConfirm) {
      setIsDeleting(true);
      setTimeout(() => {
        onDelete(task.id);
      }, 300); // Allow animation to complete
    } else {
      setShowDeleteConfirm(true);
      // Reset confirmation after 5 seconds
      setTimeout(() => {
        if (showDeleteConfirm) {
          setShowDeleteConfirm(false);
        }
      }, 5000);
    }
  };

  const handleCancelDelete = () => {
    setShowDeleteConfirm(false);
  };

  // Format date for display
  const formatDate = (dateString: string | undefined) => {
    if (!dateString) return '';
    const date = new Date(dateString);

    // Check if the date is valid
    if (isNaN(date.getTime())) {
      console.warn(`Invalid date received: ${dateString}`);
      return 'Invalid date';
    }

    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    });
  };

  // Get priority display text and color classes
  const getPriorityClasses = (priority: string) => {
    switch (priority) {
      case 'high':
        return 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400 border-red-200 dark:border-red-800';
      case 'medium':
        return 'bg-amber-100 text-amber-800 dark:bg-amber-900/30 dark:text-amber-400 border-amber-200 dark:border-amber-800';
      case 'low':
        return 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400 border-green-200 dark:border-green-800';
      default:
        return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300 border-gray-200 dark:border-gray-600';
    }
  };

  // Get recurring display text
  const getRecurringText = (recurring: string) => {
    switch (recurring) {
      case 'daily':
        return 'Daily';
      case 'weekly':
        return 'Weekly';
      case 'monthly':
        return 'Monthly';
      default:
        return '';
    }
  };

  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, x: -100 }}
      className={clsx(
        'border rounded-lg p-4 mb-3 transition-all duration-300 hover:shadow-md',
        'bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700',
        isCompleted ? 'opacity-70' : 'opacity-100',
        isDeleting ? 'scale-95 opacity-0' : 'scale-100'
      )}
    >
      <div className="flex items-start">
        {/* Checkbox */}
        <button
          onClick={handleToggleComplete}
          className={clsx(
            'flex-shrink-0 h-6 w-6 rounded-full flex items-center justify-center mr-3 mt-1 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500',
            isCompleted
              ? 'bg-green-500 text-white border-green-500'
              : 'border-2 border-gray-300 dark:border-gray-600 hover:border-primary-500'
          )}
          aria-label={isCompleted ? 'Mark as incomplete' : 'Mark as complete'}
        >
          <AnimatePresence>
            {isCompleted && (
              <motion.svg
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                exit={{ scale: 0 }}
                width="16"
                height="16"
                viewBox="0 0 24 24"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
                className="text-white"
              >
                <CheckCircleSolidIcon />
              </motion.svg>
            )}
          </AnimatePresence>
        </button>

        {/* Task Content */}
        <div className="flex-grow min-w-0">
          <div className="flex items-start justify-between">
            <div className="flex-1 min-w-0">
              <h3
                className={clsx(
                  'text-lg font-medium truncate',
                  isCompleted
                    ? 'text-gray-500 dark:text-gray-400 line-through'
                    : 'text-gray-900 dark:text-white'
                )}
              >
                {task.title}
              </h3>

              {task.description && (
                <p
                  className={clsx(
                    'mt-1 text-sm truncate',
                    isCompleted
                      ? 'text-gray-400 dark:text-gray-500 line-through'
                      : 'text-gray-600 dark:text-gray-400'
                  )}
                >
                  {task.description}
                </p>
              )}
            </div>

            {/* Action Buttons */}
            <div className="flex space-x-2 ml-4 flex-shrink-0">
              <button
                onClick={() => onEdit(task)}
                className="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 p-1 rounded-full hover:bg-gray-100 dark:hover:bg-gray-700"
                aria-label="Edit task"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
              </button>

              <button
                onClick={handleDeleteClick}
                className="text-gray-500 hover:text-red-500 dark:text-gray-400 dark:hover:text-red-400 p-1 rounded-full hover:bg-gray-100 dark:hover:bg-gray-700"
                aria-label="Delete task"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </button>
            </div>
          </div>

          {/* Task Metadata */}
          <div className="mt-3 flex flex-wrap items-center gap-2">
            {/* Priority Badge */}
            {task.priority !== 'medium' && (
              <span
                className={clsx(
                  'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border',
                  getPriorityClasses(task.priority)
                )}
              >
                {task.priority.charAt(0).toUpperCase() + task.priority.slice(1)}
              </span>
            )}

            {/* Tags */}
            {task.tags && task.tags.length > 0 && (
              <div className="flex flex-wrap gap-1">
                {task.tags.map((tag, index) => (
                  <span
                    key={index}
                    className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400"
                  >
                    <TagIcon className="w-3 h-3 mr-1" />
                    {tag}
                  </span>
                ))}
              </div>
            )}

            {/* Due Date */}
            {task.due_date && (
              <div className="flex items-center text-xs text-gray-500 dark:text-gray-400">
                <CalendarIcon className="w-4 h-4 mr-1" />
                <span>Due: {formatDate(task.due_date)}</span>
              </div>
            )}

            {/* Recurring Indicator */}
            {task.recurring !== 'none' && (
              <div className="flex items-center text-xs text-gray-500 dark:text-gray-400">
                <ArrowPathIcon className="w-4 h-4 mr-1" />
                <span>{getRecurringText(task.recurring)}</span>
              </div>
            )}

            {/* Completed Indicator */}
            {isCompleted && task.completed_at && (
              <div className="flex items-center text-xs text-green-600 dark:text-green-400">
                <CheckCircleIcon className="w-4 h-4 mr-1" />
                <span>Completed: {formatDate(task.completed_at)}</span>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Delete Confirmation */}
      <AnimatePresence>
        {showDeleteConfirm && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="mt-3 pt-3 border-t border-gray-200 dark:border-gray-700"
          >
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600 dark:text-gray-400">Are you sure you want to delete this task?</span>
              <div className="flex space-x-2">
                <button
                  onClick={handleCancelDelete}
                  className="px-3 py-1 text-sm rounded-md border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700"
                >
                  Cancel
                </button>
                <button
                  onClick={handleDeleteClick}
                  className="px-3 py-1 text-sm rounded-md bg-red-600 text-white hover:bg-red-700"
                >
                  Delete
                </button>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}