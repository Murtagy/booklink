/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { TimeSlot } from "./TimeSlot";

/**
 * Both in and Out
 */
export type Day = {
  date: string;
  timeslots: Array<TimeSlot>;
};
