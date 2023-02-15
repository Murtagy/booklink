/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

export type CreateServiceWithClientId = {
  name: string;
  price?: number;
  price_lower_bound?: number;
  price_higher_bound?: number;
  seconds: number;
  description?: string;
  client_id: number;
};
