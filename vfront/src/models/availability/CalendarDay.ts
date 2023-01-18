import type { TimeSlot } from "@/models/availability/TimeSlot";

export class CalendarDay {
  constructor(public date: string, public timeslots: TimeSlot[]) {}
}
