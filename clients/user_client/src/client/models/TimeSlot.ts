/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { TimeSlotType } from "./TimeSlotType";

/**
 * Both in and Out
 */
export type TimeSlot = {
  dt_from: string;
  dt_to: string;
  slot_type: TimeSlotType;
};
