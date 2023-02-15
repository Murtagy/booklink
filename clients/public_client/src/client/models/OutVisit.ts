/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

export type OutVisit = {
  version?: OutVisit.version;
  email?: string;
  has_notification: boolean;
  phone?: string;
  status: string;
  visit_id: number;
  worker_id?: number;
};

export namespace OutVisit {
  export enum version {
    "_1" = 1,
  }
}
