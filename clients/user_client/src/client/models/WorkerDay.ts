/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { OutVisitExtended } from "./OutVisitExtended";
import type { OutWorker } from "./OutWorker";
import type { TimeSlot } from "./TimeSlot";

export type WorkerDay = {
  date: string;
  job_hours: Array<TimeSlot>;
  visit_hours: Array<OutVisitExtended>;
  worker: OutWorker;
};
