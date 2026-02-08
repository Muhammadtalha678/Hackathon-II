"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { toast } from "sonner";
import { Task } from "@/lib/api/task-service";
import { taskService } from "@/lib/api/task-service";
import { authClient } from "@/lib/auth/auth-client";
import { TaskForm } from "@/components/task/task-form";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";

export default function EditTaskPage() {
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

  const handleSave = () => {
    toast.success("Task updated successfully!");
    router.push("/tasks");
  };

  const handleCancel = () => {
    router.back();
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
      <Card className="max-w-2xl mx-auto">
        <CardHeader>
          <CardTitle className="text-2xl">Edit Task</CardTitle>
        </CardHeader>
        <CardContent>
          <TaskForm
            userId={task.user_id as unknown as string}
            onTaskSubmit={handleSave}
            initialData={{
              id: task.id,
              title: task.title,
              description: task.description,
              is_completed: task.is_completed
            }}
            isEditing={true}
          />
        </CardContent>
        <CardFooter className="flex justify-end space-x-2">
          <Button variant="outline" onClick={handleCancel}>
            Cancel
          </Button>
        </CardFooter>
      </Card>
    </div>
  );
}