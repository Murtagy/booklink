/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { TimeSlotType } from "./TimeSlotType";

export type CreateSlot = {
  name: string;
  slot_type: TimeSlotType;
  client_id: number;
  worker_id?: number;
  from_datetime: string;
  to_datetime: string;
};
