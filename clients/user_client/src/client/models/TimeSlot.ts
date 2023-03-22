/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { SlotType } from "./SlotType";

/**
 * Both in and Out
 */
export type TimeSlot = {
  from_datetime: string;
  to_datetime: string;
  slot_type: SlotType;
};
