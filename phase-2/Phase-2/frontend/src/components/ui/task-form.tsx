'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Task } from '@/lib/api';
import { Button } from '@/components/ui/button';
import { ErrorMessage } from '@/components/ui/error-message';
import { LoadingSpinner } from '@/components/ui/loading-spinner';

interface TaskFormProps {
  onSubmit: (taskData: any) => void;
  onCancel: () => void;
  task?: Task;
  isLoading?: boolean;
}

export function TaskForm({ onSubmit, onCancel, task, isLoading }: TaskFormProps) {
  const isEditing = !!task;

  const [formData, setFormData] = useState({
    title: task?.title || '',
    description: task?.description || '',
    priority: task?.priority || 'medium',
    tags: task?.tags?.join(', ') || '', // Convert tags array to comma-separated string
    due_date: task?.due_date ? new Date(task.due_date).toISOString().slice(0, 16) : '', // Format for datetime-local input
    recurring: task?.recurring || 'none',
    completed: task?.completed || false,
  });

  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [apiError, setApiError] = useState<string | null>(null);

  // Update form data when task prop changes (for editing)
  useEffect(() => {
    if (task) {
      setFormData({
        title: task.title || '',
        description: task.description || '',
        priority: task.priority || 'medium',
        tags: task.tags?.join(', ') || '',
        due_date: task.due_date ? new Date(task.due_date).toISOString().slice(0, 16) : '',
        recurring: task.recurring || 'none',
        completed: task.completed || false,
      });
    }
  }, [task]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    const val = type === 'checkbox' ? (e.target as HTMLInputElement).checked : value;

    setFormData(prev => ({
      ...prev,
      [name]: val
    }));

    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => {
        const newErrors = { ...prev };
        delete newErrors[name];
        return newErrors;
      });
    }

    // Clear API error when user starts typing
    if (apiError) {
      setApiError(null);
    }
  };

  const validateForm = () => {
    const newErrors: Record<string, string> = {};

    if (!formData.title.trim()) {
      newErrors.title = 'Title is required';
    } else if (formData.title.length > 255) {
      newErrors.title = 'Title must be 255 characters or less';
    }

    if (formData.description && formData.description.length > 1000) {
      newErrors.description = 'Description must be 1000 characters or less';
    }

    // Validate tags format
    if (formData.tags) {
      const tags = formData.tags.split(',').map(tag => tag.trim()).filter(tag => tag);
      if (tags.length > 10) {
        newErrors.tags = 'Maximum 10 tags allowed';
      } else {
        for (const tag of tags) {
          if (tag.length > 50) {
            newErrors.tags = 'Each tag must be 50 characters or less';
            break;
          }
        }
      }
    }

    // Validate due date format
    if (formData.due_date) {
      const date = new Date(formData.due_date);
      if (isNaN(date.getTime())) {
        newErrors.due_date = 'Invalid date format';
      } else if (date < new Date()) {
        newErrors.due_date = 'Due date must be in the future';
      }
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    setIsSubmitting(true);
    setApiError(null); // Clear any previous API errors

    try {
      // Prepare tags array from comma-separated string
      const tags = formData.tags
        ? formData.tags
            .split(',')
            .map(tag => tag.trim())
            .filter(tag => tag) // Remove empty tags
        : [];

      // Prepare the task data object
      const taskData = {
        title: formData.title.trim(),
        description: formData.description.trim(),
        priority: formData.priority,
        tags: tags,
        due_date: formData.due_date || undefined,
        recurring: formData.recurring,
        completed: formData.completed,
      };

      await onSubmit(taskData);

      // If successful, clear any previous errors
      setApiError(null);
    } catch (error: any) {
      console.error('Error submitting task:', error);
      // Set the API error to display to the user
      setApiError(error.message || 'An error occurred while saving the task');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, height: 0 }}
      animate={{ opacity: 1, height: 'auto' }}
      exit={{ opacity: 0, height: 0 }}
      className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-4 shadow-sm"
    >
      <div className="mb-4">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
          {isEditing ? 'Edit Task' : 'Create New Task'}
        </h3>
      </div>

      {apiError && <ErrorMessage message={apiError} />}

      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Title */}
        <div>
          <label htmlFor="title" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
            Task Title *
          </label>
          <input
            type="text"
            name="title"
            id="title"
            value={formData.title}
            onChange={handleChange}
            required
            className={`w-full rounded-lg border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors ${
              errors.title
                ? 'border-red-500'
                : 'border-gray-300 dark:border-gray-600'
            }`}
            placeholder="What needs to be done?"
          />
          {errors.title && (
            <p className="mt-1 text-xs text-red-600">{errors.title}</p>
          )}
        </div>

        {/* Description */}
        <div>
          <label htmlFor="description" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
            Description
          </label>
          <textarea
            id="description"
            name="description"
            rows={3}
            value={formData.description}
            onChange={handleChange}
            className={`w-full rounded-lg border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors ${
              errors.description
                ? 'border-red-500'
                : 'border-gray-300 dark:border-gray-600'
            }`}
            placeholder="Add more details about this task..."
          />
          {errors.description && (
            <p className="mt-1 text-xs text-red-600">{errors.description}</p>
          )}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Priority */}
          <div>
            <label htmlFor="priority" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Priority
            </label>
            <select
              id="priority"
              name="priority"
              value={formData.priority}
              onChange={handleChange}
              className="w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
            >
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
            </select>
          </div>

          {/* Recurring */}
          <div>
            <label htmlFor="recurring" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Recurring
            </label>
            <select
              id="recurring"
              name="recurring"
              value={formData.recurring}
              onChange={handleChange}
              className="w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
            >
              <option value="none">None</option>
              <option value="daily">Daily</option>
              <option value="weekly">Weekly</option>
              <option value="monthly">Monthly</option>
            </select>
          </div>

          {/* Due Date */}
          <div>
            <label htmlFor="due_date" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Due Date
            </label>
            <input
              type="datetime-local"
              name="due_date"
              id="due_date"
              value={formData.due_date}
              onChange={handleChange}
              className="w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
            />
          </div>
        </div>

        {/* Tags */}
        <div>
          <label htmlFor="tags" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
            Tags
          </label>
          <input
            type="text"
            name="tags"
            id="tags"
            value={formData.tags}
            onChange={handleChange}
            className={`w-full rounded-lg border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors ${
              errors.tags
                ? 'border-red-500'
                : 'border-gray-300 dark:border-gray-600'
            }`}
            placeholder="Add tags separated by commas (e.g., work, urgent, important)"
          />
          {errors.tags && (
            <p className="mt-1 text-xs text-red-600">{errors.tags}</p>
          )}
          <p className="mt-1 text-xs text-gray-500 dark:text-gray-400">
            Separate tags with commas (e.g., work, urgent, important)
          </p>
        </div>

        {/* Completed */}
        {isEditing && (
          <div className="flex items-center">
            <input
              id="completed"
              name="completed"
              type="checkbox"
              checked={formData.completed}
              onChange={handleChange}
              className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 dark:border-gray-600 rounded transition-colors"
            />
            <label htmlFor="completed" className="ml-2 block text-sm text-gray-700 dark:text-gray-300">
              Mark as completed
            </label>
          </div>
        )}

        {/* Form Actions */}
        <div className="flex justify-end space-x-3 pt-2">
          <Button
            type="button"
            onClick={onCancel}
            disabled={isSubmitting}
            variant="outline"
            className="px-4 py-2 text-sm rounded-lg"
          >
            Cancel
          </Button>
          <Button
            type="submit"
            disabled={isSubmitting || isLoading}
            className="px-4 py-2 text-sm bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white rounded-lg transition-colors"
          >
            {isSubmitting || isLoading ? (
              <span className="flex items-center">
                <LoadingSpinner size="sm" />
                <span className="ml-2">{isEditing ? 'Updating...' : 'Creating...'}</span>
              </span>
            ) : isEditing ? (
              'Update Task'
            ) : (
              'Create Task'
            )}
          </Button>
        </div>
      </form>
    </motion.div>
  );
}