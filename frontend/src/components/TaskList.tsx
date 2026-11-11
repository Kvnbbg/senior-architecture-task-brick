"""
Strictly typed React component for Task list display.
Mirrors backend Pydantic models exactly.
Uses Tailwind for clean, accessible UI.
"""
import React from "react";

export enum TaskStatus {
  TODO = "todo",
  IN_PROGRESS = "in_progress",
  DONE = "done",
}

export interface Task {
  id: string;
  title: string;
  description?: string | null;
  status: TaskStatus;
  created_at: string;
  updated_at: string;
}

export interface TaskListProps {
  tasks: Task[];
  onStatusChange?: (id: string, status: TaskStatus) => void;
  emptyMessage?: string;
}

const statusStyles: Record<TaskStatus, string> = {
  [TaskStatus.TODO]: "bg-gray-100 text-gray-800",
  [TaskStatus.IN_PROGRESS]: "bg-blue-100 text-blue-800",
  [TaskStatus.DONE]: "bg-green-100 text-green-800",
};

export const TaskList: React.FC<TaskListProps> = ({
  tasks,
  onStatusChange,
  emptyMessage = "No tasks yet. Create one with rigor.",
}) => {
  if (tasks.length === 0) {
    return (
      <div className="p-8 text-center text-gray-500 border border-dashed rounded-lg">
        {emptyMessage}
      </div>
    );
  }

  return (
    <ul className="space-y-3" role="list">
      {tasks.map((task) => (
        <li
          key={task.id}
          className="flex items-start justify-between p-4 bg-white border rounded-lg shadow-sm"
        >
          <div className="flex-1 min-w-0">
            <h3 className="text-base font-medium text-gray-900 truncate">
              {task.title}
            </h3>
            {task.description && (
              <p className="mt-1 text-sm text-gray-600 line-clamp-2">
                {task.description}
              </p>
            )}
          </div>
          <div className="ml-4 flex items-center gap-2">
            <span
              className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${statusStyles[task.status]}`}
            >
              {task.status.replace("_", " ")}
            </span>
            {onStatusChange && (
              <select
                aria-label={`Change status for ${task.title}`}
                value={task.status}
                onChange={(e) =>
                  onStatusChange(task.id, e.target.value as TaskStatus)
                }
                className="text-sm border rounded px-2 py-1"
              >
                {Object.values(TaskStatus).map((s) => (
                  <option key={s} value={s}>
                    {s.replace("_", " ")}
                  </option>
                ))}
              </select>
            )}
          </div>
        </li>
      ))}
    </ul>
  );
};

export default TaskList;
