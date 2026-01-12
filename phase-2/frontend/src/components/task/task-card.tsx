import { Card, CardContent, CardFooter, CardHeader } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Task } from "@/lib/api/task-service";
import { Checkbox } from "@/components/ui/checkbox";
import { toast } from "sonner";
import { taskService } from "@/lib/api/task-service";

interface TaskCardProps {
  task: Task;
  onTaskUpdate: () => void;
}

export function TaskCard({ task, onTaskUpdate }: TaskCardProps) {
  const handleToggleComplete = async () => {
    try {
      // Assuming userId is available from context or prop - in real app, this would come from auth context
      await taskService.toggleTaskCompletion(task.user_id as unknown as string, task.id);
      onTaskUpdate(); // Refresh the task list
      toast.success(`Task marked as ${task.is_completed ? 'incomplete' : 'completed'}`);
    } catch (error: any) {
      toast.error("Failed to update task", {
        description: error.message || "An error occurred while updating the task",
      });
    }
  };

  const handleDelete = async () => {
    try {
      // Assuming userId is available from context or prop
      await taskService.deleteTask(task.user_id as unknown as string, task.id);
      onTaskUpdate(); // Refresh the task list
      toast.success("Task deleted successfully");
    } catch (error: any) {
      toast.error("Failed to delete task", {
        description: error.message || "An error occurred while deleting the task",
      });
    }
  };

  return (
    <Card className="hover:shadow-md transition-shadow">
      <CardHeader className="pb-2">
        <div className="flex items-start space-x-2">
          <Checkbox
            id={`task-${task.id}`}
            checked={task.is_completed}
            onCheckedChange={handleToggleComplete}
            aria-label={`Mark task ${task.title} as ${task.is_completed ? 'incomplete' : 'complete'}`}
          />
          <div className="flex-1 min-w-0">
            <h3 className={`text-base font-medium break-words ${task.is_completed ? 'line-through text-gray-500' : ''}`}>
              {task.title}
            </h3>
          </div>
        </div>
      </CardHeader>
      <CardContent className="pb-2">
        {task.description && (
          <p className="text-sm text-gray-600 break-words">
            {task.description}
          </p>
        )}
      </CardContent>
      <CardFooter className="flex justify-between pt-2 border-t">
        <span className={`text-xs px-2 py-1 rounded-full ${
          task.is_completed
            ? 'bg-green-100 text-green-800'
            : 'bg-yellow-100 text-yellow-800'
        }`}>
          {task.is_completed ? 'Completed' : 'Pending'}
        </span>
        <div className="flex space-x-2">
          <Button
            variant="outline"
            size="sm"
            onClick={handleDelete}
          >
            Delete
          </Button>
        </div>
      </CardFooter>
    </Card>
  );
}