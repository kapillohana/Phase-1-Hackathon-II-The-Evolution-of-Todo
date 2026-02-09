'use client';

import { useState, useEffect, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useRouter } from 'next/navigation';
import { useSession } from '../../lib/auth';
import { taskApi, Task } from '../../lib/api';
import { TaskCard } from '@/components/ui/task-card';
import { Button } from '@/components/ui/button';
import { TaskForm } from '@/components/ui/task-form';
import { LoadingSpinner } from '@/components/ui/loading-spinner';
import { ErrorMessage } from '@/components/ui/error-message';
import { Plus, Search, Filter, Calendar, CheckCircle, Tag, User, Settings, LogOut } from 'lucide-react';
import { toast } from '@/components/ui/toast';

function DashboardPageContent() {
  const router = useRouter();
  const { data: session, status } = useSession();
  const sessionLoading = status === 'loading';
  const [tasks, setTasks] = useState<Task[]>([]);
  const [filteredTasks, setFilteredTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState<'all' | 'completed' | 'pending'>('all');

  const fetchTasks = useCallback(async () => {
    if (!session?.user) return;

    try {
      setLoading(true);
      setError(null);

      const userId = session.user.id;
      const response = await taskApi.getTasks(userId, {
        search: searchTerm,
        filter_status: filterStatus,
      });

      if (response.success) {
        setTasks(response.data?.tasks || []);
        setFilteredTasks(response.data?.tasks || []); // Update filtered tasks too
      } else {
        if (response.error && response.error.includes('Forbidden')) {
          console.error('Access forbidden - clearing tokens and prompting re-login');
          setError('Access denied. Please log out and log back in.');
          toast.error('Access Denied', 'Please log out and log back in.');
        } else {
          setError(response.error || 'Failed to fetch tasks');
          toast.error('Failed to Fetch Tasks', response.error || 'An error occurred');
        }
        console.error('Error fetching tasks:', response.error);
      }
    } catch (err: any) {
      if (err.message?.includes('Forbidden')) {
        console.error('Access forbidden in catch block - clearing tokens');
        setError('Access denied. Please log out and log back in.');
        toast.error('Access Denied', 'Please log out and log back in.');
      } else {
        setError(err.message || 'An error occurred while fetching tasks');
        toast.error('Error Fetching Tasks', err.message || 'An unexpected error occurred');
      }
      console.error('Unexpected error fetching tasks:', err);
    } finally {
      setLoading(false);
    }
  }, [session?.user?.id, searchTerm, filterStatus]);

  // Fetch tasks when component mounts, session changes, or search/filter changes
  useEffect(() => {
    if (session?.user) {
      fetchTasks();
    }
  }, [session?.user?.id, searchTerm, filterStatus, fetchTasks]);

  // Apply filters when tasks or filters change
  useEffect(() => {
    let result = [...tasks];

    // Apply search filter
    if (searchTerm) {
      const term = searchTerm.toLowerCase();
      result = result.filter(task =>
        task.title.toLowerCase().includes(term) ||
        (task.description && task.description.toLowerCase().includes(term))
      );
    }

    // Apply status filter
    if (filterStatus !== 'all') {
      if (filterStatus === 'completed') {
        result = result.filter(task => task.completed);
      } else if (filterStatus === 'pending') {
        result = result.filter(task => !task.completed);
      }
    }

    setFilteredTasks(result);
  }, [tasks, searchTerm, filterStatus]);

  const handleCreateTask = async (taskData: any) => {
    if (!session?.user) return;

    try {
      const userId = session.user.id;
      const response = await taskApi.createTask(userId, taskData);

      if (response.success) {
        setTasks(prev => [...prev, response.data!]);
        setShowForm(false);
        toast.success('Task Created', 'Your task has been created successfully!');
      } else {
        if (response.error && response.error.includes('Forbidden')) {
          console.error('Access forbidden - clearing tokens and prompting re-login');
          setError('Access denied. Please log out and log back in.');
          toast.error('Access Denied', 'Please log out and log back in.');
        } else {
          toast.error('Failed to Create Task', response.error || 'An error occurred');
        }
        console.error('Error creating task:', response.error);
      }
    } catch (err: any) {
      if (err.message?.includes('Forbidden')) {
        console.error('Access forbidden in catch block - clearing tokens');
        setError('Access denied. Please log out and log back in.');
        toast.error('Access Denied', 'Please log out and log back in.');
      } else {
        toast.error('Error Creating Task', err.message || 'An unexpected error occurred');
        console.error('Unexpected error creating task:', err);
      }
    }
  };

  const handleUpdateTask = async (taskId: number, taskData: any) => {
    if (!session?.user) return;

    try {
      const userId = session.user.id;
      const response = await taskApi.updateTask(userId, taskId, taskData);

      if (response.success) {
        setTasks(prev => prev.map(task => (task.id === taskId ? response.data! : task)));
        setEditingTask(null);
        setShowForm(false);
        toast.success('Task Updated', 'Your task has been updated successfully!');
      } else {
        toast.error('Failed to Update Task', response.error || 'An error occurred');
        console.error('Error updating task:', response.error);
      }
    } catch (err: any) {
      toast.error('Error Updating Task', err.message || 'An unexpected error occurred');
      console.error('Unexpected error updating task:', err);
    }
  };

  const handleDeleteTask = async (taskId: number) => {
    if (!session?.user) return;

    try {
      const userId = session.user.id;
      const response = await taskApi.deleteTask(userId, taskId);

      if (response.success) {
        setTasks(prev => prev.filter(task => task.id !== taskId));
        toast.success('Task Deleted', 'Your task has been deleted successfully!');
      } else {
        toast.error('Failed to Delete Task', response.error || 'An error occurred');
        console.error('Error deleting task:', response.error);
      }
    } catch (err: any) {
      toast.error('Error Deleting Task', err.message || 'An unexpected error occurred');
      console.error('Unexpected error deleting task:', err);
    }
  };

  const handleToggleComplete = async (taskId: number) => {
    if (!session?.user) return;

    try {
      const userId = session.user.id;
      const response = await taskApi.toggleTaskCompletion(userId, taskId);

      if (response.success) {
        setTasks(prev => prev.map(task =>
          task.id === taskId
            ? { ...task, completed: response.data!.completed, completed_at: response.data!.completed_at }
            : task
        ));
        
        // Show appropriate toast based on completion status
        if (response.data!.completed) {
          toast.success('Task Completed!', 'Great job completing this task!');
        } else {
          toast.info('Task Marked Incomplete', 'Task status updated to incomplete');
        }
      } else {
        toast.error('Failed to Update Task', response.error || 'An error occurred');
        console.error('Error toggling task completion:', response.error);
      }
    } catch (err: any) {
      toast.error('Error Updating Task', err.message || 'An unexpected error occurred');
      console.error('Unexpected error toggling task completion:', err);
    }
  };

  // Show loading if session is loading
  if (sessionLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <LoadingSpinner />
      </div>
    );
  }

  // Show error if no session
  if (!session) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center py-12 max-w-md mx-auto px-4">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">🔒 You need to be signed in to view tasks.</h2>
          <p className="mt-2 text-gray-600 dark:text-gray-300">Please log in to manage your todo list.</p>
          <button
            onClick={() => router.push('/auth/signin')}
            className="mt-4 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 dark:bg-blue-700 dark:hover:bg-blue-800 transition-colors"
          >
            Go to Login
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="flex h-screen bg-gray-50 dark:bg-gray-900">
      {/* Sidebar */}
      <div className="w-64 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 flex flex-col">
        <div className="p-6 border-b border-gray-200 dark:border-gray-700">
          <h1 className="text-xl font-bold text-gray-900 dark:text-white">TaskFlow</h1>
        </div>
        
        <nav className="flex-1 p-4">
          <div className="space-y-2">
            <a href="#" className="flex items-center px-4 py-3 text-sm font-medium text-white bg-blue-600 rounded-lg">
              <CheckCircle className="w-5 h-5 mr-3" />
              My Tasks
            </a>
            <a href="#" className="flex items-center px-4 py-3 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors">
              <Calendar className="w-5 h-5 mr-3" />
              Scheduled
            </a>
            <a href="#" className="flex items-center px-4 py-3 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors">
              <CheckCircle className="w-5 h-5 mr-3" />
              Completed
            </a>
            <a href="#" className="flex items-center px-4 py-3 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors">
              <Tag className="w-5 h-5 mr-3" />
              Tags
            </a>
          </div>
        </nav>
        
        <div className="p-4 border-t border-gray-200 dark:border-gray-700">
          <div className="flex items-center">
            <img className="w-10 h-10 rounded-full" src={`https://ui-avatars.com/api/?name=${session.user?.email?.split('@')[0]}&background=6366f1&color=fff`} alt="User" />
            <div className="ml-3">
              <p className="text-sm font-medium text-gray-900 dark:text-white">{session.user?.email?.split('@')[0]}</p>
              <p className="text-xs text-gray-500 dark:text-gray-400">Online</p>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top Bar */}
        <header className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
          <div className="flex items-center justify-between p-4">
            <div className="flex items-center">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white">My Tasks</h2>
              <span className="ml-2 px-2 py-1 text-xs bg-blue-100 dark:bg-blue-900/30 text-blue-800 dark:text-blue-400 rounded-full">
                {filteredTasks.length} tasks
              </span>
            </div>
            
            <div className="flex items-center space-x-4">
              <div className="relative">
                <input
                  type="text"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  placeholder="Search tasks..."
                  className="pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white/90 dark:bg-gray-700/90 text-gray-900 dark:text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
                />
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              </div>
              
              <Button
                onClick={() => {
                  setEditingTask(null);
                  setShowForm(!showForm);
                }}
                className="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white px-4 py-2 rounded-lg transition-all transform hover:scale-105"
              >
                <Plus className="w-4 h-4 mr-2" />
                Add Task
              </Button>
            </div>
          </div>
        </header>

        {/* Filters */}
        <div className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 p-4">
          <div className="flex flex-wrap gap-2">
            <button
              onClick={() => setFilterStatus('all')}
              className={`px-3 py-1.5 text-sm rounded-full transition-colors ${
                filterStatus === 'all'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
              }`}
            >
              All
            </button>
            <button
              onClick={() => setFilterStatus('pending')}
              className={`px-3 py-1.5 text-sm rounded-full transition-colors ${
                filterStatus === 'pending'
                  ? 'bg-yellow-600 text-white'
                  : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
              }`}
            >
              Pending
            </button>
            <button
              onClick={() => setFilterStatus('completed')}
              className={`px-3 py-1.5 text-sm rounded-full transition-colors ${
                filterStatus === 'completed'
                  ? 'bg-green-600 text-white'
                  : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
              }`}
            >
              Completed
            </button>
          </div>
        </div>

        {/* Task List */}
        <main className="flex-1 overflow-y-auto p-6">
          {error && error.includes('mismatch') && (
            <div className="mb-4 p-4 bg-yellow-100 border border-yellow-400 text-yellow-700 rounded-lg shadow-sm">
              <p className="font-bold">Authentication Issue Detected</p>
              <p>Please clear your browser cookies and refresh the page, or try logging out and back in.</p>
              <button
                onClick={() => {
                  import('../../lib/auth').then(({ forceLogout }) => {
                    forceLogout();
                  });
                }}
                className="mt-2 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
              >
                Force Logout & Clear Tokens
              </button>
            </div>
          )}

          {showForm && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="mb-6"
            >
              <TaskForm
                onSubmit={editingTask ? (data) => handleUpdateTask(editingTask.id, data) : handleCreateTask}
                onCancel={() => {
                  setShowForm(false);
                  setEditingTask(null);
                }}
                task={editingTask || undefined}
                isLoading={loading}
              />
            </motion.div>
          )}

          {error && <ErrorMessage message={error} />}

          {loading ? (
            <div className="flex items-center justify-center h-64">
              <LoadingSpinner />
            </div>
          ) : (
            <AnimatePresence>
              {filteredTasks.length > 0 ? (
                <div className="space-y-3">
                  {filteredTasks.map((task) => (
                    <motion.div
                      key={task.id}
                      layout
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, x: -100 }}
                      transition={{ duration: 0.2 }}
                    >
                      <TaskCard
                        task={task}
                        onEdit={(task) => {
                          setEditingTask(task);
                          setShowForm(true);
                        }}
                        onDelete={handleDeleteTask}
                        onToggleComplete={handleToggleComplete}
                      />
                    </motion.div>
                  ))}
                </div>
              ) : (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="text-center py-12"
                >
                  <div className="mx-auto h-24 w-24 flex items-center justify-center rounded-full bg-gray-100 dark:bg-gray-800">
                    <div className="text-4xl">📋</div>
                  </div>
                  <h3 className="mt-4 text-sm font-medium text-gray-900 dark:text-white">No tasks</h3>
                  <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
                    Get started by creating a new task.
                  </p>
                  <div className="mt-6">
                    <Button
                      onClick={() => setShowForm(true)}
                      className="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 transform hover:scale-105 transition-transform"
                    >
                      <Plus className="w-4 h-4 mr-2" />
                      Create new task
                    </Button>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          )}
        </main>
      </div>
    </div>
  );
}

export default function DashboardPage() {
  return <DashboardPageContent />;
}