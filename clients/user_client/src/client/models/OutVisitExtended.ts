/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { OutVisit } from "./OutVisit";
import type { OutVisitServiceSmall } from "./OutVisitServiceSmall";
import type { OutWorker } from "./OutWorker";

export type OutVisitExtended = {
  services: Array<OutVisitServiceSmall>;
  visit: OutVisit;
  worker?: OutWorker;
};
