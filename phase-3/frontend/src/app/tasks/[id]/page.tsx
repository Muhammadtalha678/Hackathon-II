"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { toast } from "sonner";
import { Task } from "@/lib/api/task-service";
import { taskService } from "@/lib/api/task-service";
import { authClient } from "@/lib/auth/auth-client";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Checkbox } from "@/components/ui/checkbox";

export default function TaskDetailPage() {
  const params = useParams();
  const router = useRouter();
  const [task, setTask] = useState<Task | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchTask = async () => {
      try {
        const { data: session } = await authClient.getSession();

        if (session?.user) {
          const userId = session.user.id;
          // Handle both string and array forms of params.id
          const taskIdParam = params.id;
          const taskIdValue = Array.isArray(taskIdParam) ? taskIdParam[0] : taskIdParam;
          const taskId = parseInt(taskIdValue as string);

          const fetchedTask = await taskService.getTaskById(userId, taskId);
          setTask(fetchedTask);
        } else {
          throw new Error("User not authenticated");
        }
      } catch (error: any) {
        toast.error("Error fetching task", {
          description: error.message || "Failed to load task",
        });
        router.push("/tasks");
      } finally {
        setLoading(false);
      }
    };

    if (params.id) {
      fetchTask();
    }
  }, [params.id, router]);

  const handleToggleComplete = async () => {
    if (!task) return;

    try {
      const { data: session } = await authClient.getSession();

      if (session?.user) {
        const userId = session.user.id;
        const updatedTask = await taskService.toggleTaskCompletion(userId, task.id);
        setTask(updatedTask);
        toast.success(`Task marked as ${updatedTask.is_completed ? 'incomplete' : 'completed'}`);
      } else {
        throw new Error("User not authenticated");
      }
    } catch (error: any) {
      toast.error("Failed to update task", {
        description: error.message || "An error occurred while updating the task",
      });
    }
  };

  const handleBack = () => {
    router.push("/tasks");
  };

  if (loading) {
    return (
      <div className="container mx-auto py-10">
        <p>Loading task...</p>
      </div>
    );
  }

  if (!task) {
    return (
      <div className="container mx-auto py-10">
        <p>Task not found</p>
      </div>
    );
  }

  return (
    <div className="container mx-auto py-10">
      <Card className="max-w-3xl mx-auto">
        <CardHeader>
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div className="flex items-center gap-3">
              <Checkbox
                id={`task-${task.id}`}
                checked={task.is_completed}
                onCheckedChange={() => handleToggleComplete()}
                aria-label={`Mark task ${task.title} as ${task.is_completed ? 'incomplete' : 'complete'}`}
              />
              <div>
                <CardTitle className={`text-2xl ${task.is_completed ? 'line-through text-gray-500' : ''}`}>{task.title}</CardTitle>
                <div className={`mt-1 px-2 py-1 inline-block rounded-full text-xs font-medium ${
                  task.is_completed
                    ? 'bg-green-100 text-green-800'
                    : 'bg-yellow-100 text-yellow-800'
                }`}>
                  {task.is_completed ? 'Completed' : 'Pending'}
                </div>
              </div>
            </div>
          </div>
        </CardHeader>
        <CardContent className="space-y-6">
          <div>
            <h3 className="text-sm font-medium text-gray-500 mb-2">Description</h3>
            <p className="text-gray-700">{task.description || 'No description provided.'}</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
            <div className="bg-gray-50 p-3 rounded-md">
              <h3 className="font-medium text-gray-500">Created At</h3>
              <p className="text-gray-700">{new Date(task.created_at).toLocaleString()}</p>
            </div>
            <div className="bg-gray-50 p-3 rounded-md">
              <h3 className="font-medium text-gray-500">Updated At</h3>
              <p className="text-gray-700">{new Date(task.updated_at).toLocaleString()}</p>
            </div>
          </div>
        </CardContent>
        <CardFooter className="flex justify-between">
          <Button variant="outline" onClick={handleBack}>
            Back to Tasks
          </Button>
        </CardFooter>
      </Card>
    </div>
  );
}