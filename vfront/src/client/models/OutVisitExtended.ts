/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { OutService } from "./OutService";
import type { OutSlot } from "./OutSlot";
import type { OutVisit } from "./OutVisit";

export type OutVisitExtended = {
  services: Array<OutService>;
  slot: OutSlot;
  visit: OutVisit;
};
