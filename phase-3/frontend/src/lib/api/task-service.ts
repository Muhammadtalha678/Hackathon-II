// lib/api/task-service.ts
import { authClient } from '../auth/auth-client';
import { AppRoutes } from './AppRoutes';

export interface Task {
  id: number;
  title: string;
  description: string | null;
  is_completed: boolean;
  user_id: string;
  created_at: string; // ISO timestamp
  updated_at: string; // ISO timestamp
}

export interface TaskFormData {
  id?: number;
  title: string;
  description: string | null;
  is_completed: boolean;
  user_id?: string;
}

export interface TaskDeletionResponse {
  success: boolean;
  message: string;
  deleted_id: number;
}

export interface TaskService {
  getAllTasks(userId: string): Promise<Task[]>;
  getTaskById(userId: string, taskId: number): Promise<Task>;
  createTask(userId: string, taskData: TaskFormData): Promise<Task>;
  updateTask(userId: string, taskId: number, taskData: Omit<TaskFormData, 'id'>): Promise<Task>;
  deleteTask(userId: string, taskId: number): Promise<TaskDeletionResponse>;
  toggleTaskCompletion(userId: string, taskId: number): Promise<Task>;
}

class TaskServiceImpl implements TaskService {
  async getAllTasks(userId: string): Promise<Task[]> {
    const { data, error } = await authClient.token();
    const token = data?.token
    if (!token) {
      throw new Error('No authentication token found');
    }
    console.log(token);

    const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}${AppRoutes.TASKS(userId).ALL}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || `Failed to fetch tasks: ${response.statusText}`);
    }

    return response.json();
  }

  async getTaskById(userId: string, taskId: number): Promise<Task> {
    const { data, error } = await authClient.token();
    const token = data?.token
    if (!token) {
      throw new Error('No authentication token found');
    }

    const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}${AppRoutes.TASKS(userId).SINGLE(taskId)}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || `Failed to fetch task: ${response.statusText}`);
    }

    return response.json();
  }

  async createTask(userId: string, taskData: TaskFormData): Promise<Task> {
    const { data, error } = await authClient.token();
    const token = data?.token
    if (!token) {
      throw new Error('No authentication token found');
    }
    taskData["user_id"] = userId
    const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}${AppRoutes.TASKS(userId).ALL}`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(taskData),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || `Failed to create task: ${response.statusText}`);
    }

    return response.json();
  }

  async updateTask(userId: string, taskId: number, taskData: Omit<TaskFormData, 'id'>): Promise<Task> {
    const { data, error } = await authClient.token();
    const token = data?.token
    if (!token) {
      throw new Error('No authentication token found');
    }

    const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}${AppRoutes.TASKS(userId).SINGLE(taskId)}`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(taskData),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || `Failed to update task: ${response.statusText}`);
    }

    return response.json();
  }

  async deleteTask(userId: string, taskId: number): Promise<TaskDeletionResponse> {
    const { data, error } = await authClient.token();
    const token = data?.token
    if (!token) {
      throw new Error('No authentication token found');
    }

    const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}${AppRoutes.TASKS(userId).SINGLE(taskId)}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || `Failed to delete task: ${response.statusText}`);
    }

    return response.json();
  }

  async toggleTaskCompletion(userId: string, taskId: number): Promise<Task> {
    const { data, error } = await authClient.token();
    const token = data?.token
    if (!token) {
      throw new Error('No authentication token found');
    }

    const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}${AppRoutes.TASKS(userId).COMPLETE(taskId)}`, {
      method: 'PATCH',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || `Failed to toggle task completion: ${response.statusText}`);
    }

    return response.json();
  }
}

export const taskService = new TaskServiceImpl();