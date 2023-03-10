/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { InServiceToVisit } from "./InServiceToVisit";

export type InVisit = {
  client_id: number;
  from_dt: string;
  services: Array<InServiceToVisit>;
  remind_me: boolean;
  version?: InVisit.version;
  worker_id?: string;
  phone: string;
  email: string;
  first_name: string;
  last_name: string;
};

export namespace InVisit {
  export enum version {
    "_1" = 1,
  }
}
