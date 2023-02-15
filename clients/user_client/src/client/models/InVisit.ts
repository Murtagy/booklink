/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { InServiceToVisit } from "./InServiceToVisit";

export type InVisit = {
  client_id: number;
  from_dt: string;
  first_name: string;
  last_name: string;
  email: string;
  services: Array<InServiceToVisit>;
  phone: string;
  remind_me: boolean;
  version?: InVisit.version;
  worker_id?: string;
};

export namespace InVisit {
  export enum version {
    "_1" = 1,
  }
}
