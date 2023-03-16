/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { CustomerInfoIn } from "./CustomerInfoIn";
import type { InServiceToVisit } from "./InServiceToVisit";
import type { SlotType } from "./SlotType";

export type CreateSlot = {
  slot_type: SlotType;
  worker_id?: number;
  from_datetime: string;
  to_datetime: string;
  customer_info?: CustomerInfoIn;
  services?: Array<InServiceToVisit>;
  has_notification?: boolean;
  status?: string;
};
