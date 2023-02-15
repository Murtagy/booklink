import type { WorkerAvailability } from "@/models/availability/WorkerAvailability";

export class ClientAvailability {
  constructor(public availability: WorkerAvailability[]) {}
}
