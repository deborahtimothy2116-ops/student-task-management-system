"""
Business logic and persistence layer for Student Task Management System.
Includes CR-101 workload analytics and priority filtering.
"""

from datetime import datetime, date
from typing import List, Optional, Dict
from src.models import Task, TaskCreate, TaskUpdate, StatusEnum, PriorityEnum, WorkloadSummary


class TaskService:
    def __init__(self):
        self._tasks: Dict[int, Task] = {}
        self._next_id = 1
        self._seed_initial_data()

    def _seed_initial_data(self):
        """Seed initial student tasks for demonstration"""
        sample_tasks = [
            TaskCreate(
                title="SE Lab Unit-V: SCM & DevOps Implementation",
                description="Complete WBS, GitFlow branching, Dockerfile, and GitHub Actions CI/CD pipeline",
                course_code="231CS523",
                due_date="2026-11-15",
                priority=PriorityEnum.CRITICAL,
                estimated_hours=8.0
            ),
            TaskCreate(
                title="Prepare Gantt Chart & Critical Path Calculation",
                description="Identify Critical Path, Milestones M1-M5, and draw Gantt chart in PDF",
                course_code="231CS523",
                due_date="2026-11-13",
                priority=PriorityEnum.HIGH,
                estimated_hours=4.0
            ),
            TaskCreate(
                title="Data Science Model Evaluation & Cross-Validation",
                description="Perform 5-fold cross-validation and compute F1-score/ROC curves on sales dataset",
                course_code="231CS521",
                due_date="2026-11-20",
                priority=PriorityEnum.MEDIUM,
                estimated_hours=6.0
            ),
            TaskCreate(
                title="Computer Networks Socket Programming Lab",
                description="Implement multi-client chat server using TCP sockets and select/poll in C++",
                course_code="231CS522",
                due_date="2026-11-18",
                priority=PriorityEnum.LOW,
                estimated_hours=3.5
            )
        ]
        for item in sample_tasks:
            self.create_task(item)

    def _check_overdue(self, due_date_str: str, status: StatusEnum) -> bool:
        """Check if a pending or in-progress task is past its due date"""
        if status == StatusEnum.COMPLETED:
            return False
        try:
            due = datetime.strptime(due_date_str, "%Y-%m-%d").date()
            return due < date.today()
        except ValueError:
            return False

    def list_tasks(
        self,
        course_code: Optional[str] = None,
        priority: Optional[PriorityEnum] = None,
        status: Optional[StatusEnum] = None,
        search: Optional[str] = None
    ) -> List[Task]:
        """List tasks with optional filtering (CR-101 enhanced)"""
        results = list(self._tasks.values())

        if course_code:
            results = [t for t in results if t.course_code.upper() == course_code.upper()]

        if priority:
            results = [t for t in results if t.priority == priority]

        if status:
            results = [t for t in results if t.status == status]

        if search:
            query = search.lower()
            results = [
                t for t in results
                if query in t.title.lower() or query in t.description.lower() or query in t.course_code.lower()
            ]

        # Recalculate overdue status dynamically
        for t in results:
            t.is_overdue = self._check_overdue(t.due_date, t.status)

        # Sort by priority order (CRITICAL -> HIGH -> MEDIUM -> LOW) then due date
        priority_rank = {
            PriorityEnum.CRITICAL: 0,
            PriorityEnum.HIGH: 1,
            PriorityEnum.MEDIUM: 2,
            PriorityEnum.LOW: 3
        }
        results.sort(key=lambda t: (priority_rank.get(t.priority, 4), t.due_date))
        return results

    def get_task(self, task_id: int) -> Optional[Task]:
        task = self._tasks.get(task_id)
        if task:
            task.is_overdue = self._check_overdue(task.due_date, task.status)
        return task

    def create_task(self, task_in: TaskCreate) -> Task:
        task_id = self._next_id
        self._next_id += 1
        now_str = datetime.now().isoformat()
        
        task = Task(
            id=task_id,
            title=task_in.title,
            description=task_in.description or "",
            course_code=task_in.course_code.upper(),
            due_date=task_in.due_date,
            priority=task_in.priority,
            estimated_hours=task_in.estimated_hours,
            status=StatusEnum.PENDING,
            created_at=now_str,
            completed_at=None,
            is_overdue=self._check_overdue(task_in.due_date, StatusEnum.PENDING)
        )
        self._tasks[task_id] = task
        return task

    def update_task(self, task_id: int, task_in: TaskUpdate) -> Optional[Task]:
        task = self._tasks.get(task_id)
        if not task:
            return None

        update_data = task_in.model_dump(exclude_unset=True)
        if "course_code" in update_data and update_data["course_code"]:
            update_data["course_code"] = update_data["course_code"].upper()

        if "status" in update_data:
            new_status = update_data["status"]
            if new_status == StatusEnum.COMPLETED and task.status != StatusEnum.COMPLETED:
                task.completed_at = datetime.now().isoformat()
            elif new_status != StatusEnum.COMPLETED:
                task.completed_at = None

        for field, value in update_data.items():
            setattr(task, field, value)

        task.is_overdue = self._check_overdue(task.due_date, task.status)
        return task

    def delete_task(self, task_id: int) -> bool:
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def toggle_status(self, task_id: int) -> Optional[Task]:
        """Toggle task between PENDING and COMPLETED"""
        task = self._tasks.get(task_id)
        if not task:
            return None
        
        if task.status == StatusEnum.COMPLETED:
            task.status = StatusEnum.PENDING
            task.completed_at = None
        else:
            task.status = StatusEnum.COMPLETED
            task.completed_at = datetime.now().isoformat()

        task.is_overdue = self._check_overdue(task.due_date, task.status)
        return task

    def get_workload_summary(self) -> WorkloadSummary:
        """Calculate aggregate student workload metrics (CR-101 Feature)"""
        tasks = list(self._tasks.values())
        total = len(tasks)
        pending = sum(1 for t in tasks if t.status == StatusEnum.PENDING)
        in_progress = sum(1 for t in tasks if t.status == StatusEnum.IN_PROGRESS)
        completed = sum(1 for t in tasks if t.status == StatusEnum.COMPLETED)
        high_or_crit = sum(1 for t in tasks if t.priority in (PriorityEnum.HIGH, PriorityEnum.CRITICAL) and t.status != StatusEnum.COMPLETED)

        total_hours = round(sum(t.estimated_hours for t in tasks), 1)
        remaining_hours = round(sum(t.estimated_hours for t in tasks if t.status != StatusEnum.COMPLETED), 1)
        completion_rate = round((completed / total * 100.0), 1) if total > 0 else 0.0

        return WorkloadSummary(
            total_tasks=total,
            pending_tasks=pending,
            in_progress_tasks=in_progress,
            completed_tasks=completed,
            high_or_critical_tasks=high_or_crit,
            total_estimated_hours=total_hours,
            remaining_hours=remaining_hours,
            completion_rate_percentage=completion_rate
        )


# Global singleton instance
task_service = TaskService()
