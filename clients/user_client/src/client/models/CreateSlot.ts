/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { TimeSlotType } from "./TimeSlotType";

export type CreateSlot = {
  slot_type: TimeSlotType;
  client_id: number;
  worker_id?: number;
  from_datetime: string;
  to_datetime: string;
  has_notification?: boolean;
  status?: string;
};
