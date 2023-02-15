/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Availability } from "../models/Availability";
import type { AvailabilityPerWorker } from "../models/AvailabilityPerWorker";
import type { CreateSlot } from "../models/CreateSlot";
import type { InVisit } from "../models/InVisit";
import type { OutService } from "../models/OutService";
import type { OutServices } from "../models/OutServices";
import type { OutVisit } from "../models/OutVisit";
import type { OutVisitExtended } from "../models/OutVisitExtended";
import type { OutWorker } from "../models/OutWorker";
import type { OutWorkers } from "../models/OutWorkers";
import type { SkillsOut } from "../models/SkillsOut";

import type { CancelablePromise } from "../core/CancelablePromise";
import { OpenAPI } from "../core/OpenAPI";
import { request as __request } from "../core/request";

export class DefaultService {
  /**
   * Ping
   * @returns any Successful Response
   * @throws ApiError
   */
  public static ping(): CancelablePromise<any> {
    return __request(OpenAPI, {
      method: "GET",
      url: "/ping",
    });
  }

  /**
   * Get Worker
   * @param workerId
   * @returns OutWorker Successful Response
   * @throws ApiError
   */
  public static getWorker(workerId: string): CancelablePromise<OutWorker> {
    return __request(OpenAPI, {
      method: "GET",
      url: "/worker/{worker_id}",
      path: {
        worker_id: workerId,
      },
      errors: {
        422: `Validation Error`,
      },
    });
  }

  /**
   * Get Workers By Client
   * @param clientId
   * @param services
   * @returns OutWorkers Successful Response
   * @throws ApiError
   */
  public static getWorkersByClient(
    clientId: number,
    services?: string
  ): CancelablePromise<OutWorkers> {
    return __request(OpenAPI, {
      method: "GET",
      url: "/client/{client_id}/workers",
      path: {
        client_id: clientId,
      },
      query: {
        services: services,
      },
      errors: {
        422: `Validation Error`,
      },
    });
  }

  /**
   * Get Workers
   * @returns OutWorkers Successful Response
   * @throws ApiError
   */
  public static getWorkers(): CancelablePromise<OutWorkers> {
    return __request(OpenAPI, {
      method: "GET",
      url: "/workers",
    });
  }

  /**
   * Get Service
   * @param serviceId
   * @returns OutService Successful Response
   * @throws ApiError
   */
  public static getService(serviceId: number): CancelablePromise<OutService> {
    return __request(OpenAPI, {
      method: "GET",
      url: "/service/{service_id}",
      path: {
        service_id: serviceId,
      },
      errors: {
        422: `Validation Error`,
      },
    });
  }

  /**
   * Get Service By Client
   * @param clientId
   * @param serviceId
   * @returns OutService Successful Response
   * @throws ApiError
   */
  public static getServiceByClient(
    clientId: number,
    serviceId: number
  ): CancelablePromise<OutService> {
    return __request(OpenAPI, {
      method: "GET",
      url: "/client/{client_id}/service/{service_id}",
      path: {
        client_id: clientId,
        service_id: serviceId,
      },
      errors: {
        422: `Validation Error`,
      },
    });
  }

  /**
   * Get Services By Client
   * @param clientId
   * @param workerId
   * @returns OutServices Successful Response
   * @throws ApiError
   */
  public static getServicesByClient(
    clientId: number,
    workerId?: number
  ): CancelablePromise<OutServices> {
    return __request(OpenAPI, {
      method: "GET",
      url: "/client/{client_id}/services",
      path: {
        client_id: clientId,
      },
      query: {
        worker_id: workerId,
      },
      errors: {
        422: `Validation Error`,
      },
    });
  }

  /**
   * Get Skills
   * @param clientId
   * @param workerId
   * @returns SkillsOut Successful Response
   * @throws ApiError
   */
  public static getSkills(
    clientId: number,
    workerId?: number
  ): CancelablePromise<SkillsOut> {
    return __request(OpenAPI, {
      method: "GET",
      url: "/client/{client_id}/picker/services",
      path: {
        client_id: clientId,
      },
      query: {
        worker_id: workerId,
      },
      errors: {
        422: `Validation Error`,
      },
    });
  }

  /**
   * Get Visit
   * @param visitId
   * @returns OutVisit Successful Response
   * @throws ApiError
   */
  public static getVisit(visitId: number): CancelablePromise<OutVisit> {
    return __request(OpenAPI, {
      method: "GET",
      url: "/visit/{visit_id}",
      path: {
        visit_id: visitId,
      },
      errors: {
        422: `Validation Error`,
      },
    });
  }

  /**
   * Create Visit Slot
   * @param requestBody
   * @returns OutVisit Successful Response
   * @throws ApiError
   */
  public static createVisitSlot(
    requestBody: CreateSlot
  ): CancelablePromise<OutVisit> {
    return __request(OpenAPI, {
      method: "POST",
      url: "/visit",
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    });
  }

  /**
   * Public Book Visit
   * @param requestBody
   * @returns OutVisitExtended Successful Response
   * @throws ApiError
   */
  public static publicBookVisit(
    requestBody: InVisit
  ): CancelablePromise<OutVisitExtended> {
    return __request(OpenAPI, {
      method: "POST",
      url: "/public/visit",
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    });
  }

  /**
   * Get Worker Availability
   * @param clientId
   * @param workerId
   * @param services
   * @returns Availability Successful Response
   * @throws ApiError
   */
  public static getWorkerAvailability(
    clientId: string,
    workerId: string,
    services?: string
  ): CancelablePromise<Availability> {
    return __request(OpenAPI, {
      method: "GET",
      url: "/client/{client_id}/worker/{worker_id}/availability",
      path: {
        client_id: clientId,
        worker_id: workerId,
      },
      query: {
        services: services,
      },
      errors: {
        422: `Validation Error`,
      },
    });
  }

  /**
   * Get Client Availability
   * @param clientId
   * @param services
   * @returns AvailabilityPerWorker Successful Response
   * @throws ApiError
   */
  public static getClientAvailability(
    clientId: number,
    services?: string
  ): CancelablePromise<AvailabilityPerWorker> {
    return __request(OpenAPI, {
      method: "GET",
      url: "/client/{client_id}/availability/",
      path: {
        client_id: clientId,
      },
      query: {
        services: services,
      },
      errors: {
        422: `Validation Error`,
      },
    });
  }
}
