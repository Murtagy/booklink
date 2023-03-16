/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { SlotType } from "./SlotType";

/**
 * Both in and Out
 */
export type TimeSlot = {
  dt_from: string;
  dt_to: string;
  slot_type: SlotType;
};
