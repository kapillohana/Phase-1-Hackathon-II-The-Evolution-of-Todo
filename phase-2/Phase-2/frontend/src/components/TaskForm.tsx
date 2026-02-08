'use client';

import { useState, useEffect } from 'react';
import { Task } from '@/lib/api'; // Adjust import path as needed
import ErrorMessage from './ErrorMessage'; // We'll create this component
import LoadingSpinner from './LoadingSpinner'; // We'll create this component

interface TaskFormProps {
  onSubmit: (taskData: any) => void;
  onCancel: () => void;
  task?: Task;
  isLoading?: boolean;
}

export default function TaskForm({ onSubmit, onCancel, task, isLoading }: TaskFormProps) {
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
    <form onSubmit={handleSubmit} className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
      {apiError && <ErrorMessage message={apiError} />}
      <div className="grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-6">
        {/* Title */}
        <div className="sm:col-span-6">
          <label htmlFor="title" className="block text-sm font-medium text-gray-700 dark:text-gray-300">
            Title *
          </label>
          <div className="mt-1">
            <input
              type="text"
              name="title"
              id="title"
              value={formData.title}
              onChange={handleChange}
              required
              className={`block w-full rounded-md border-gray-300 dark:border-gray-600 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-white ${
                errors.title ? 'border-red-500' : ''
              }`}
              placeholder="Task title"
            />
            {errors.title && <p className="mt-1 text-sm text-red-600">{errors.title}</p>}
          </div>
        </div>

        {/* Description */}
        <div className="sm:col-span-6">
          <label htmlFor="description" className="block text-sm font-medium text-gray-700 dark:text-gray-300">
            Description
          </label>
          <div className="mt-1">
            <textarea
              id="description"
              name="description"
              rows={3}
              value={formData.description}
              onChange={handleChange}
              className={`block w-full rounded-md border-gray-300 dark:border-gray-600 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-white ${
                errors.description ? 'border-red-500' : ''
              }`}
              placeholder="Task description"
            />
            {errors.description && <p className="mt-1 text-sm text-red-600">{errors.description}</p>}
          </div>
        </div>

        {/* Priority */}
        <div className="sm:col-span-3">
          <label htmlFor="priority" className="block text-sm font-medium text-gray-700 dark:text-gray-300">
            Priority
          </label>
          <div className="mt-1">
            <select
              id="priority"
              name="priority"
              value={formData.priority}
              onChange={handleChange}
              className="block w-full rounded-md border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
            >
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
            </select>
          </div>
        </div>

        {/* Recurring */}
        <div className="sm:col-span-3">
          <label htmlFor="recurring" className="block text-sm font-medium text-gray-700 dark:text-gray-300">
            Recurring
          </label>
          <div className="mt-1">
            <select
              id="recurring"
              name="recurring"
              value={formData.recurring}
              onChange={handleChange}
              className="block w-full rounded-md border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
            >
              <option value="none">None</option>
              <option value="daily">Daily</option>
              <option value="weekly">Weekly</option>
              <option value="monthly">Monthly</option>
            </select>
          </div>
        </div>

        {/* Tags */}
        <div className="sm:col-span-6">
          <label htmlFor="tags" className="block text-sm font-medium text-gray-700 dark:text-gray-300">
            Tags
          </label>
          <div className="mt-1">
            <input
              type="text"
              name="tags"
              id="tags"
              value={formData.tags}
              onChange={handleChange}
              className={`block w-full rounded-md border-gray-300 dark:border-gray-600 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-white ${
                errors.tags ? 'border-red-500' : ''
              }`}
              placeholder="Work, Personal, Urgent (comma separated)"
            />
            <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
              Separate tags with commas (e.g., "work, urgent, important")
            </p>
            {errors.tags && <p className="mt-1 text-sm text-red-600">{errors.tags}</p>}
          </div>
        </div>

        {/* Due Date */}
        <div className="sm:col-span-3">
          <label htmlFor="due_date" className="block text-sm font-medium text-gray-700 dark:text-gray-300">
            Due Date
          </label>
          <div className="mt-1">
            <input
              type="datetime-local"
              name="due_date"
              id="due_date"
              value={formData.due_date}
              onChange={handleChange}
              className={`block w-full rounded-md border-gray-300 dark:border-gray-600 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-white ${
                errors.due_date ? 'border-red-500' : ''
              }`}
            />
            {errors.due_date && <p className="mt-1 text-sm text-red-600">{errors.due_date}</p>}
          </div>
        </div>

        {/* Completed */}
        {isEditing && (
          <div className="sm:col-span-3 flex items-center">
            <input
              id="completed"
              name="completed"
              type="checkbox"
              checked={formData.completed}
              onChange={handleChange}
              className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 dark:border-gray-600 rounded"
            />
            <label htmlFor="completed" className="ml-2 block text-sm text-gray-900 dark:text-white">
              Mark as completed
            </label>
          </div>
        )}
      </div>

      {/* Form Actions */}
      <div className="mt-6 flex justify-end space-x-3">
        <button
          type="button"
          onClick={onCancel}
          disabled={isSubmitting}
          className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
        >
          Cancel
        </button>
        <button
          type="submit"
          disabled={isSubmitting || isLoading}
          className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
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
        </button>
      </div>
    </form>
  );
}