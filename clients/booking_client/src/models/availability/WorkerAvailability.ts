import type { CalendarDay } from "@/models/availability/CalendarDay";

export class WorkerAvailability {
  constructor(public days: CalendarDay[], public worker_id: number) {}
}
