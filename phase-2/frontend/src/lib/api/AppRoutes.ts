// lib/api/AppRoutes.ts
export const AppRoutes = {
  // Authentication routes (Better Auth)
  AUTH: {
    REGISTER: '/api/auth/register',
    LOGIN: '/api/auth/login',
    LOGOUT: '/api/auth/logout',
    ME: '/api/auth/me',
    PROFILE: '/api/auth/profile',
    CHANGE_PASSWORD: '/api/auth/change-password'
  },

  // Task management routes (FastAPI Backend)
  TASKS: (userId: string) => ({
    ALL: `/api/${userId}/tasks`,
    SINGLE: (taskId: number) => `/api/${userId}/tasks/${taskId}`,
    COMPLETE: (taskId: number) => `/api/${userId}/tasks/${taskId}/complete`
  })
};