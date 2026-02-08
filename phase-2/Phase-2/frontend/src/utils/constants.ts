// Constants for the Advanced Todo Application

// Environment variables
export const BETTER_AUTH_SECRET = process.env.NEXT_PUBLIC_BETTER_AUTH_SECRET || 'fallback-secret-key-change-in-production';
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api';
export const BETTER_AUTH_URL = process.env.NEXT_PUBLIC_BETTER_AUTH_URL || 'http://localhost:8000';

// Application settings
export const APP_NAME = 'Advanced Todo App';
export const DEFAULT_PAGE_SIZE = 20;
export const MAX_TAGS_PER_TASK = 10;
export const MAX_TAG_LENGTH = 50;
export const MAX_TITLE_LENGTH = 255;
export const MAX_DESCRIPTION_LENGTH = 1000;

// Priority levels
export const PRIORITY_LEVELS = {
  HIGH: 'high',
  MEDIUM: 'medium',
  LOW: 'low',
} as const;

// Recurring patterns
export const RECURRING_PATTERNS = {
  NONE: 'none',
  DAILY: 'daily',
  WEEKLY: 'weekly',
  MONTHLY: 'monthly',
} as const;

// Task status
export const TASK_STATUS = {
  COMPLETED: 'completed',
  PENDING: 'pending',
  ALL: 'all',
} as const;

// Date formats
export const DATE_FORMATS = {
  DISPLAY: 'MMM dd, yyyy',
  INPUT: 'yyyy-MM-dd',
  API: 'yyyy-MM-dd\'T\'HH:mm:ss.SSSXXX',
} as const;

// Error messages
export const ERROR_MESSAGES = {
  NETWORK_ERROR: 'Network error occurred. Please check your connection.',
  AUTH_REQUIRED: 'Authentication required. Please sign in.',
  INVALID_CREDENTIALS: 'Invalid email or password.',
  TASK_NOT_FOUND: 'Task not found.',
  UNAUTHORIZED_ACCESS: 'Unauthorized access. You can only access your own tasks.',
  INVALID_FORM_DATA: 'Please check the form for errors.',
};

// Success messages
export const SUCCESS_MESSAGES = {
  TASK_CREATED: 'Task created successfully!',
  TASK_UPDATED: 'Task updated successfully!',
  TASK_DELETED: 'Task deleted successfully!',
  SIGN_IN_SUCCESS: 'Successfully signed in!',
  SIGN_UP_SUCCESS: 'Account created successfully!',
};

// Animation durations (in milliseconds)
export const ANIMATION_DURATIONS = {
  FADE_IN: 300,
  SLIDE_UP: 200,
  BOUNCE: 1000,
};