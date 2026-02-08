"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { toast } from "sonner";
import { taskService, TaskFormData } from "@/lib/api/task-service";
import { useEffect, useState } from "react";
import { Checkbox } from "@/components/ui/checkbox";
import { authClient } from "@/lib/auth/auth-client";

const taskSchema = z.object({
  title: z.string().min(1, "Title is required").max(500, "Title must be less than 500 characters"),
  description: z.string().max(2000, "Description must be less than 2000 characters").optional().nullable(),
  is_completed: z.boolean(),
});

interface TaskFormProps {
  userId: string;
  onTaskSubmit: () => void;
  initialData?: TaskFormData & { id?: number };
  isEditing?: boolean;
}

export function TaskForm({ userId, onTaskSubmit, initialData, isEditing = false }: TaskFormProps) {
  const [currentUserId, setCurrentUserId] = useState<string | null>(null);

  useEffect(() => {
    const fetchUserId = async () => {
      if (userId) {
        setCurrentUserId(userId);
      } else {
        const { data: session } = await authClient.getSession();
        setCurrentUserId(session?.user?.id || "");
      }
    };

    fetchUserId();
  }, [userId]);

  const form = useForm<z.infer<typeof taskSchema>>({
    resolver: zodResolver(taskSchema),
    defaultValues: {
      title: initialData?.title || "",
      description: initialData?.description || "",
      is_completed: initialData?.is_completed || false,
    },
  });

  async function onSubmit(values: z.infer<typeof taskSchema>) {
    try {
      if (!currentUserId) {
        toast.error("User not authenticated");
        return;
      }

      if (isEditing && initialData && initialData.id !== undefined) {
        // Update existing task
        const { id, ...taskData } = initialData; // Exclude id from taskData
        await taskService.updateTask(currentUserId, initialData.id, {
          title: values.title,
          description: values.description ?? null, // Ensure description is either string or null, not undefined
          is_completed: values.is_completed,
        });

        toast.success("Task updated successfully!");
        form.reset();
        onTaskSubmit(); // Refresh the task list
      } else {
        await taskService.createTask(currentUserId, {
          title: values.title,
          description: values.description ?? null, // Ensure description is either string or null, not undefined
          is_completed: values.is_completed,
        });

        toast.success("Task created successfully!");
        form.reset();
        onTaskSubmit(); // Refresh the task list
      }
    } catch (error: any) {
      toast.error("Failed to save task", {
        description: error.message || "An error occurred while saving the task",
      });
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>{isEditing ? "Edit Task" : "Create New Task"}</CardTitle>
      </CardHeader>
      <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)}>
          <CardContent className="space-y-4">
            <FormField
              control={form.control}
              name="title"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Title *</FormLabel>
                  <FormControl>
                    <Input placeholder="Task title" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="description"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Description</FormLabel>
                  <FormControl>
                    <Textarea
                      placeholder="Task description (optional)"
                      rows={3}
                      {...field}
                      value={field.value ?? ""} // Handle nullable/undefined value
                      onChange={field.onChange}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="is_completed"
              render={({ field }) => (
                <FormItem className="flex flex-row items-start space-x-3 space-y-0">
                  <FormControl>
                    <Checkbox
                      checked={field.value}
                      onCheckedChange={field.onChange}
                    />
                  </FormControl>
                  <div className="space-y-1 leading-none">
                    <FormLabel>Mark as completed</FormLabel>
                  </div>
                </FormItem>
              )}
            />
          </CardContent>
          <CardFooter>
            <Button type="submit" disabled={form.formState.isSubmitting}>
              {form.formState.isSubmitting
                ? (isEditing ? "Updating..." : "Creating...")
                : (isEditing ? "Update Task" : "Create Task")}
            </Button>
          </CardFooter>
        </form>
      </Form>
    </Card>
  );
}