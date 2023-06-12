/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { OutService } from './OutService';
import type { OutVisit } from './OutVisit';
import type { OutWorker } from './OutWorker';

export type OutVisitExtended = {
    services: Array<OutService>;
    visit: OutVisit;
    worker: OutWorker;
};

