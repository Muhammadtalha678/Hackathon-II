import { Task } from "@/lib/api/task-service";
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import { toast } from "sonner";
import { taskService } from "@/lib/api/task-service";
import { useState } from "react";
import { TaskForm } from "./task-form";
import { useRouter } from "next/navigation";

interface TaskListProps {
  tasks: Task[];
  onTaskUpdate: () => void;
}

export function TaskList({ tasks, onTaskUpdate }: TaskListProps) {
  const router = useRouter();

  const handleToggleComplete = async (task: Task) => {
    try {
      await taskService.toggleTaskCompletion(task.user_id as unknown as string, task.id);
      onTaskUpdate(); // Refresh the task list
      toast.success(`Task marked as ${task.is_completed ? 'incomplete' : 'completed'}`);
    } catch (error: any) {
      toast.error("Failed to update task", {
        description: error.message || "An error occurred while updating the task",
      });
    }
  };

  const handleDelete = async (taskId: number, userId: string) => {
    try {
      await taskService.deleteTask(userId, taskId);
      onTaskUpdate(); // Refresh the task list
      toast.success("Task deleted successfully");
    } catch (error: any) {
      toast.error("Failed to delete task", {
        description: error.message || "An error occurred while deleting the task",
      });
    }
  };

  const handleEdit = (task: Task) => {
    router.push(`/tasks/${task.id}/edit`);
  };

  if (tasks.length === 0) {
    return (
      <div className="text-center py-10">
        <p className="text-gray-500">No tasks found. Create your first task!</p>
      </div>
    );
  }

  return (
    <div className="rounded-md border">
      <table className="w-full">
        <thead className="border-b">
          <tr>
            <th className="h-12 px-4 text-left align-middle font-medium text-muted-foreground w-12"></th>
            <th className="h-12 px-4 text-left align-middle font-medium text-muted-foreground">Title</th>
            <th className="h-12 px-4 text-left align-middle font-medium text-muted-foreground hidden md:table-cell">Description</th>
            <th className="h-12 px-4 text-right align-middle font-medium text-muted-foreground">Actions</th>
          </tr>
        </thead>
        <tbody>
          {tasks.map((task) => (
            <tr key={task.id} className="border-b hover:bg-muted/50">
              <td className="p-4 align-middle">
                <Checkbox
                  id={`task-${task.id}`}
                  checked={task.is_completed}
                  onCheckedChange={() => handleToggleComplete(task)}
                  aria-label={`Mark task ${task.title} as ${task.is_completed ? 'incomplete' : 'complete'}`}
                />
              </td>
              <td className="p-4 align-middle">
                <div
                  className={`cursor-pointer ${task.is_completed ? 'line-through text-gray-500' : 'text-blue-600 hover:underline'}`}
                  onClick={() => router.push(`/tasks/${task.id}`)}
                >
                  {task.title}
                </div>
              </td>
              <td className="p-4 align-middle hidden md:table-cell">
                <div className="text-sm text-gray-600 max-w-md truncate">
                  {task.description || '-'}
                </div>
              </td>
              <td className="p-4 align-middle text-right">
                <div className="flex justify-end space-x-2">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => handleToggleComplete(task)}
                  >
                    {task.is_completed ? 'Mark Incomplete' : 'Mark Complete'}
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => handleEdit(task)}
                  >
                    Edit
                  </Button>
                  <Button
                    variant="destructive"
                    size="sm"
                    onClick={() => handleDelete(task.id, task.user_id as unknown as string)}
                  >
                    Delete
                  </Button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}