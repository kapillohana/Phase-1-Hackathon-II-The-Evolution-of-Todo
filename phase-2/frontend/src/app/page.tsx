'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '../lib/auth';
import LoadingSpinner from '../components/LoadingSpinner';
import { AuthProvider } from '../lib/auth';
import { taskApi } from '../lib/api';
import { HeroSection } from '@/components/ui/hero-section';
import { FeatureCards } from '@/components/ui/feature-cards';
import { TestimonialsSection } from '@/components/ui/testimonials-section';
import { CtaSection } from '@/components/ui/cta-section';
import { TaskManagementSection } from '@/components/ui/task-management-section';
import { StatsSection } from '@/components/ui/stats-section';
import { Button } from '@/components/ui/button';
import { motion } from 'framer-motion';
import { Calendar, CheckCircle, Tag, User, Menu, X, Home, Settings, LogOut } from 'lucide-react';

export default function HomePage() {
  return <HomePageContent />;
}

function HomePageContent() {
  const router = useRouter();
  const { user, isLoading } = useAuth();
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [tasks, setTasks] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Fetch tasks for the authenticated user
  useEffect(() => {
    const fetchTasks = async () => {
      if (!user) return;

      try {
        setLoading(true);
        setError(null);

        // Use the proper task API service
        const response = await taskApi.getTasks(user.id);
        if (response.success) {
          // Flatten the tasks from the paginated response
          setTasks(response.data?.tasks || []);
        } else {
          throw new Error(response.error || 'Failed to fetch tasks');
        }
      } catch (err: any) {
        setError(err.message || 'Failed to load tasks');
        console.error('Error fetching tasks:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchTasks();
  }, [user]);

  // Show loading spinner while checking authentication status
  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <LoadingSpinner />
      </div>
    );
  }

  // If user is authenticated, show a collapsible sidebar layout
  if (user) {
    // Show loading state while fetching tasks
    if (loading) {
      return (
        <div className="flex h-screen bg-gray-50 dark:bg-gray-900">
          <div className="flex-1 flex items-center justify-center">
            <LoadingSpinner />
          </div>
        </div>
      );
    }

    // Show error state if there was an error loading tasks
    if (error) {
      return (
        <div className="flex h-screen bg-gray-50 dark:bg-gray-900">
          <div className="flex-1 flex items-center justify-center">
            <div className="text-center">
              <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">Error Loading Tasks</h2>
              <p className="text-gray-600 dark:text-gray-400 mb-4">{error}</p>
              <Button
                onClick={() => window.location.reload()}
                className="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white"
              >
                Retry
              </Button>
            </div>
          </div>
        </div>
      );
    }

    return (
      <div className="flex h-screen bg-gray-50 dark:bg-gray-900">
        {/* Collapsible Sidebar */}
        <div className={`fixed lg:relative inset-y-0 left-0 z-30 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 flex flex-col transform transition-all duration-300 ease-in-out ${sidebarOpen ? 'w-64 translate-x-0' : '-translate-x-full lg:translate-x-0 lg:w-20'} lg:translate-x-0`}>
          <div className="p-4 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between">
            {sidebarOpen && (
              <h1 className="text-xl font-bold text-gray-900 dark:text-white">TaskFlow</h1>
            )}
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200"
            >
              {sidebarOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>
          </div>

          <nav className="flex-1 p-2">
            <div className="space-y-1">
              <a href="#" className={`flex items-center ${sidebarOpen ? 'px-4 py-3' : 'p-3 justify-center'} text-sm font-medium text-white bg-blue-600 rounded-lg`}>
                <Home className="w-5 h-5 mr-3" />
                {sidebarOpen && <span>Home</span>}
              </a>
              <a href="/dashboard" className={`flex items-center ${sidebarOpen ? 'px-4 py-3' : 'p-3 justify-center'} text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors`}>
                <CheckCircle className="w-5 h-5 mr-3" />
                {sidebarOpen && <span>My Tasks</span>}
              </a>
              <a href="#" className={`flex items-center ${sidebarOpen ? 'px-4 py-3' : 'p-3 justify-center'} text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors`}>
                <Calendar className="w-5 h-5 mr-3" />
                {sidebarOpen && <span>Scheduled</span>}
              </a>
              <a href="#" className={`flex items-center ${sidebarOpen ? 'px-4 py-3' : 'p-3 justify-center'} text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors`}>
                <Tag className="w-5 h-5 mr-3" />
                {sidebarOpen && <span>Tags</span>}
              </a>
              <a href="#" className={`flex items-center ${sidebarOpen ? 'px-4 py-3' : 'p-3 justify-center'} text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors`}>
                <Settings className="w-5 h-5 mr-3" />
                {sidebarOpen && <span>Settings</span>}
              </a>
            </div>
          </nav>

          <div className="p-4 border-t border-gray-200 dark:border-gray-700">
            <div className="flex items-center">
              <img className="w-10 h-10 rounded-full" src={`https://ui-avatars.com/api/?name=${user.email?.split('@')[0]}&background=6366f1&color=fff`} alt="User" />
              {sidebarOpen && (
                <div className="ml-3">
                  <p className="text-sm font-medium text-gray-900 dark:text-white">{user.email?.split('@')[0]}</p>
                  <p className="text-xs text-gray-500 dark:text-gray-400">Online</p>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Mobile sidebar overlay */}
        {sidebarOpen && (
          <div
            className="fixed inset-0 z-20 bg-black bg-opacity-50 lg:hidden"
            onClick={() => setSidebarOpen(false)}
          />
        )}

        {/* Mobile sidebar toggle button */}
        {!sidebarOpen && (
          <button
            onClick={() => setSidebarOpen(true)}
            className="fixed top-4 left-4 z-40 p-2 bg-white dark:bg-gray-800 rounded-lg shadow-lg text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 lg:hidden"
          >
            <Menu className="h-6 w-6" />
          </button>
        )}

        {/* Main Content */}
        <div className="flex-1 flex flex-col overflow-hidden">
          {/* Top Bar */}
          <header className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
            <div className="flex items-center justify-between p-4">
              <div className="flex items-center">
                <button
                  onClick={() => setSidebarOpen(!sidebarOpen)}
                  className="mr-4 text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200"
                >
                  <Menu className="h-6 w-6" />
                </button>
                <h2 className="text-lg font-semibold text-gray-900 dark:text-white">Welcome Back, {user.email?.split('@')[0]}!</h2>
              </div>

              <div className="flex items-center space-x-4">
                <Button
                  onClick={() => router.push('/dashboard')}
                  className="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white px-4 py-2 rounded-lg transition-colors"
                >
                  Go to Dashboard
                </Button>
              </div>
            </div>
          </header>

          {/* Content Area */}
          <main className="flex-1 overflow-y-auto p-6">
            <div className="max-w-7xl mx-auto">
              <div className="text-center mb-8">
                <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
                  Welcome Back, {user.email?.split('@')[0]}!
                </h1>
                <p className="text-lg text-gray-600 dark:text-gray-300">
                  Here's what you need to focus on today
                </p>
              </div>

              {/* Calculate real metrics from tasks */}
              {tasks && tasks.length > 0 && (
                <>
                  {/* Today's Summary Cards */}
                  <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                    <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700">
                      <div className="flex items-center">
                        <div className="p-3 rounded-lg bg-blue-100 dark:bg-blue-900/30">
                          <CheckCircle className="h-6 w-6 text-blue-600 dark:text-blue-400" />
                        </div>
                        <div className="ml-4">
                          <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Completed</p>
                          <p className="text-2xl font-semibold text-gray-900 dark:text-white">
                            {tasks.filter(task => task.completed).length}
                          </p>
                        </div>
                      </div>
                    </div>

                    <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700">
                      <div className="flex items-center">
                        <div className="p-3 rounded-lg bg-yellow-100 dark:bg-yellow-900/30">
                          <Calendar className="h-6 w-6 text-yellow-600 dark:text-yellow-400" />
                        </div>
                        <div className="ml-4">
                          <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Due Today</p>
                          <p className="text-2xl font-semibold text-gray-900 dark:text-white">
                            {tasks.filter(task => {
                              if (!task.due_date) return false;
                              const today = new Date();
                              const dueDate = new Date(task.due_date);
                              return dueDate.toDateString() === today.toDateString() && !task.completed;
                            }).length}
                          </p>
                        </div>
                      </div>
                    </div>

                    <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700">
                      <div className="flex items-center">
                        <div className="p-3 rounded-lg bg-red-100 dark:bg-red-900/30">
                          <Tag className="h-6 w-6 text-red-600 dark:text-red-400" />
                        </div>
                        <div className="ml-4">
                          <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Overdue</p>
                          <p className="text-2xl font-semibold text-gray-900 dark:text-white">
                            {tasks.filter(task => {
                              if (!task.due_date || task.completed) return false;
                              const today = new Date();
                              const dueDate = new Date(task.due_date);
                              return dueDate < today;
                            }).length}
                          </p>
                        </div>
                      </div>
                    </div>

                    <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700">
                      <div className="flex items-center">
                        <div className="p-3 rounded-lg bg-green-100 dark:bg-green-900/30">
                          <CheckCircle className="h-6 w-6 text-green-600 dark:text-green-400" />
                        </div>
                        <div className="ml-4">
                          <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Progress</p>
                          <p className="text-2xl font-semibold text-gray-900 dark:text-white">
                            {tasks.length > 0
                              ? Math.round((tasks.filter(task => task.completed).length / tasks.length) * 100) + '%'
                              : '0%'}
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                </>
              )}

              {/* Today's Tasks Section */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Today's Tasks */}
                <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700">
                  <div className="flex items-center justify-between mb-6">
                    <h2 className="text-lg font-semibold text-gray-900 dark:text-white">Today's Tasks</h2>
                    <span className="text-sm text-gray-500 dark:text-gray-400">
                      {tasks ? tasks.filter(task => {
                        if (!task.due_date) return false;
                        const today = new Date();
                        const dueDate = new Date(task.due_date);
                        return dueDate.toDateString() === today.toDateString();
                      }).length : 0} tasks
                    </span>
                  </div>

                  <div className="space-y-4">
                    {tasks && tasks
                      .filter(task => {
                        if (!task.due_date) return false;
                        const today = new Date();
                        const dueDate = new Date(task.due_date);
                        return dueDate.toDateString() === today.toDateString();
                      })
                      .slice(0, 4) // Show only first 4 tasks for the dashboard
                      .map((task) => (
                        <div key={task.id} className="flex items-center p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
                          <div className={`flex-shrink-0 h-5 w-5 rounded border-2 ${
                            task.completed
                              ? 'bg-green-500 border-green-500'
                              : 'border-gray-300 dark:border-gray-600'
                          } flex items-center justify-center`}>
                            {task.completed ? (
                              <CheckCircle className="h-3 w-3 text-white" />
                            ) : (
                              <CheckCircle className="h-3 w-3 text-transparent" />
                            )}
                          </div>
                          <div className="ml-3 flex-1">
                            <p className={`text-sm font-medium ${
                              task.completed
                                ? 'text-gray-500 dark:text-gray-400 line-through'
                                : 'text-gray-900 dark:text-white'
                            }`}>
                              {task.title}
                            </p>
                            {task.due_date && (
                              <p className="text-xs text-gray-500 dark:text-gray-400">
                                Due: {new Date(task.due_date).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                              </p>
                            )}
                          </div>
                          <div className="flex items-center space-x-2">
                            {task.tags && task.tags.length > 0 && (
                              <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400">
                                {task.tags[0]}
                              </span>
                            )}
                            <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium ${
                              task.priority === 'high'
                                ? 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400'
                                : task.priority === 'medium'
                                  ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400'
                                  : 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400'
                            }`}>
                              {task.priority.charAt(0).toUpperCase() + task.priority.slice(1)}
                            </span>
                          </div>
                        </div>
                      ))}
                    {(!tasks || tasks.filter(task => {
                      if (!task.due_date) return false;
                      const today = new Date();
                      const dueDate = new Date(task.due_date);
                      return dueDate.toDateString() === today.toDateString();
                    }).length === 0) && (
                      <div className="text-center py-8">
                        <div className="mx-auto h-12 w-12 rounded-full bg-gray-100 dark:bg-gray-700 flex items-center justify-center">
                          <CheckCircle className="h-6 w-6 text-gray-400" />
                        </div>
                        <h3 className="mt-2 text-sm font-medium text-gray-900 dark:text-white">No tasks for today</h3>
                        <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
                          Great job! You've completed all your tasks for today.
                        </p>
                      </div>
                    )}
                  </div>
                </div>

                {/* Progress & Upcoming */}
                <div className="space-y-8">
                  {/* Progress Chart */}
                  <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700">
                    <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-6">Weekly Progress</h2>
                    <div className="space-y-4">
                      {tasks && tasks.length > 0 && (
                        <>
                          <div>
                            <div className="flex justify-between text-sm mb-1">
                              <span className="text-gray-600 dark:text-gray-400">Completed</span>
                              <span className="text-gray-900 dark:text-white">
                                {Math.round((tasks.filter(task => task.completed).length / tasks.length) * 100)}%
                              </span>
                            </div>
                            <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                              <div
                                className="bg-blue-600 h-2 rounded-full"
                                style={{
                                  width: `${tasks.length > 0 ? (tasks.filter(task => task.completed).length / tasks.length) * 100 : 0}%`
                                }}
                              ></div>
                            </div>
                          </div>
                          <div>
                            <div className="flex justify-between text-sm mb-1">
                              <span className="text-gray-600 dark:text-gray-400">Pending</span>
                              <span className="text-gray-900 dark:text-white">
                                {Math.round(((tasks.filter(task => !task.completed && !(
                                  task.due_date &&
                                  new Date(task.due_date) < new Date()
                                )).length) / tasks.length) * 100)}%
                              </span>
                            </div>
                            <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                              <div
                                className="bg-yellow-500 h-2 rounded-full"
                                style={{
                                  width: `${tasks.length > 0 ? ((tasks.filter(task => !task.completed && !(
                                    task.due_date &&
                                    new Date(task.due_date) < new Date()
                                  )).length) / tasks.length) * 100 : 0}%`
                                }}
                              ></div>
                            </div>
                          </div>
                          <div>
                            <div className="flex justify-between text-sm mb-1">
                              <span className="text-gray-600 dark:text-gray-400">Overdue</span>
                              <span className="text-gray-900 dark:text-white">
                                {Math.round(((tasks.filter(task =>
                                  task.due_date &&
                                  new Date(task.due_date) < new Date() &&
                                  !task.completed
                                ).length) / tasks.length) * 100)}%
                              </span>
                            </div>
                            <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                              <div
                                className="bg-red-500 h-2 rounded-full"
                                style={{
                                  width: `${tasks.length > 0 ? ((tasks.filter(task =>
                                    task.due_date &&
                                    new Date(task.due_date) < new Date() &&
                                    !task.completed
                                  ).length) / tasks.length) * 100 : 0}%`
                                }}
                              ></div>
                            </div>
                          </div>
                        </>
                      )}
                    </div>
                  </div>

                  {/* Upcoming Deadlines */}
                  <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700">
                    <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-6">Upcoming Deadlines</h2>
                    <div className="space-y-4">
                      {tasks && tasks
                        .filter(task => {
                          if (!task.due_date || task.completed) return false;
                          const today = new Date();
                          const tomorrow = new Date(today);
                          tomorrow.setDate(tomorrow.getDate() + 1);
                          const dueDate = new Date(task.due_date);

                          // Include tasks due tomorrow or in the next 7 days
                          return dueDate >= today && dueDate <= new Date(today.getTime() + 7 * 24 * 60 * 60 * 1000);
                        })
                        .sort((a, b) => new Date(a.due_date!).getTime() - new Date(b.due_date!).getTime())
                        .slice(0, 3) // Show only next 3 upcoming deadlines
                        .map((task) => (
                          <div key={task.id} className="flex items-center justify-between p-3 hover:bg-gray-50 dark:hover:bg-gray-700/50 rounded-lg">
                            <div>
                              <p className="text-sm font-medium text-gray-900 dark:text-white">{task.title}</p>
                              <p className="text-xs text-gray-500 dark:text-gray-400">
                                {new Date(task.due_date!).toLocaleDateString('en-US', {
                                  weekday: 'short',
                                  month: 'short',
                                  day: 'numeric',
                                  hour: '2-digit',
                                  minute: '2-digit'
                                })}
                              </p>
                            </div>
                            <div className="flex items-center">
                              <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium ${
                                new Date(task.due_date!) < new Date(Date.now() + 24 * 60 * 60 * 1000)
                                  ? 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400'
                                  : 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400'
                              }`}>
                                {new Date(task.due_date!) < new Date(Date.now() + 24 * 60 * 60 * 1000) ? 'Due Soon' : 'Upcoming'}
                              </span>
                            </div>
                          </div>
                        ))
                      }
                      {(!tasks || tasks.filter(task => {
                        if (!task.due_date || task.completed) return false;
                        const today = new Date();
                        const tomorrow = new Date(today);
                        tomorrow.setDate(tomorrow.getDate() + 1);
                        const dueDate = new Date(task.due_date);

                        // Include tasks due tomorrow or in the next 7 days
                        return dueDate >= today && dueDate <= new Date(today.getTime() + 7 * 24 * 60 * 60 * 1000);
                      }).length === 0) && (
                        <div className="text-center py-4">
                          <p className="text-sm text-gray-500 dark:text-gray-400">No upcoming deadlines</p>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </main>
        </div>
      </div>
    );
  }

  // Unauthenticated user sees the marketing page
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="w-full min-h-screen bg-gradient-to-b from-white to-blue-50 dark:from-gray-900 dark:to-gray-800"
    >
      <HeroSection />
      <StatsSection />
      <FeatureCards />
      <TaskManagementSection />
      <TestimonialsSection />
      <CtaSection />
    </motion.div>
  );
}