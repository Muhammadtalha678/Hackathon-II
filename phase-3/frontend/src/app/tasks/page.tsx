"use client";

import { useEffect, useState } from "react";
import { toast } from "sonner";
import { taskService, Task } from "@/lib/api/task-service";
import { authClient } from "@/lib/auth/auth-client";
import { TaskForm } from "@/components/task/task-form";
import { TaskList } from "@/components/task/task-list";
import { Button } from "@/components/ui/button";

export default function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [userId, setUserId] = useState<string>("");
  const [showAddForm, setShowAddForm] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Get current user to get userId
        const { data: session } = await authClient.getSession();

        if (session?.user) {
          const currentUserId = session.user.id;
          setUserId(currentUserId);

          const userTasks = await taskService.getAllTasks(currentUserId);
          setTasks(userTasks);
        } else {
          throw new Error("User not authenticated");
        }
      } catch (error: any) {
        toast.error("Error fetching tasks", {
          description: error.message || "Failed to load tasks",
        });
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const fetchTasks = async () => {
    try {
      // Get current user to get userId
      const { data: session } = await authClient.getSession();

      if (session?.user) {
        const currentUserId = session.user.id;

        const userTasks = await taskService.getAllTasks(currentUserId);
        setTasks(userTasks);
      } else {
        throw new Error("User not authenticated");
      }
    } catch (error: any) {
      toast.error("Error fetching tasks", {
        description: error.message || "Failed to load tasks",
      });
    }
  };

  if (loading) {
    return (
      <div className="container mx-auto py-10">
        <p>Loading tasks...</p>
      </div>
    );
  }

  return (
    <div className=" mx-4 sm:mx-6 md:mx-8 py-10">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Your Tasks</h1>
        <Button onClick={() => setShowAddForm(!showAddForm)}>
          {showAddForm ? "Hide Form" : "Add Task"}
        </Button>
      </div>

      <div className="space-y-6">
        <div>
          {showAddForm && <TaskForm userId={userId} onTaskSubmit={fetchTasks} />}
        </div>

        <div>
          <TaskList tasks={tasks} onTaskUpdate={fetchTasks} />
        </div>
      </div>
    </div>
  );
}