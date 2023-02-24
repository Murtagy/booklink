/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Availability } from "../models/Availability";
import type { AvailabilityPerWorker } from "../models/AvailabilityPerWorker";
import type { Body_create_file } from "../models/Body_create_file";
import type { Body_login_for_access_token } from "../models/Body_login_for_access_token";
import type { CreateService } from "../models/CreateService";
import type { CreateServiceWithClientId } from "../models/CreateServiceWithClientId";
import type { CreateSlot } from "../models/CreateSlot";
import type { CreateWorker } from "../models/CreateWorker";
import type { InVisit } from "../models/InVisit";
import type { OutService } from "../models/OutService";
import type { OutServices } from "../models/OutServices";
import type { OutSlot } from "../models/OutSlot";
import type { OutVisit } from "../models/OutVisit";
import type { OutVisitExtended } from "../models/OutVisitExtended";
import type { OutWorker } from "../models/OutWorker";
import type { OutWorkers } from "../models/OutWorkers";
import type { Received } from "../models/Received";
import type { SkillIn } from "../models/SkillIn";
import type { SkillsIn } from "../models/SkillsIn";
import type { SkillsOut } from "../models/SkillsOut";
import type { TokenOut } from "../models/TokenOut";
import type { UpdateService } from "../models/UpdateService";
import type { UpdateWorker } from "../models/UpdateWorker";
import type { UserCreate } from "../models/UserCreate";
import type { UserOut } from "../models/UserOut";
import type { VisitsByDays } from "../models/VisitsByDays";
import type { VisitsByDaysRQ } from "../models/VisitsByDaysRQ";

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
   * Create User
   * @param requestBody
   * @returns TokenOut Successful Response
   * @throws ApiError
   */
  public static createUser(
    requestBody: UserCreate
  ): CancelablePromise<TokenOut> {
    return __request(OpenAPI, {
      method: "POST",
      url: "/signup",
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    });
  }

  /**
   * Read Users Me
   * @returns UserOut Successful Response
   * @throws ApiError
   */
  public static readUsersMe(): CancelablePromise<UserOut> {
    return __request(OpenAPI, {
      method: "GET",
      url: "/users/me/",
    });
  }

  /**
   * Read Users Me2
   * @returns UserOut Successful Response
   * @throws ApiError
   */
  public static readUsersMe2(): CancelablePromise<UserOut> {
    return __request(OpenAPI, {
      method: "GET",
      url: "/my_user",
    });
  }

  /**
   * Login For Access Token
   * @param formData
   * @returns TokenOut Successful Response
   * @throws ApiError
   */
  public static loginForAccessToken(
    formData: Body_login_for_access_token
  ): CancelablePromise<TokenOut> {
    return __request(OpenAPI, {
      method: "POST",
      url: "/token",
      formData: formData,
      mediaType: "application/x-www-form-urlencoded",
      errors: {
        422: `Validation Error`,
      },
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
   * Update Worker
   * @param workerId
   * @param requestBody
   * @returns OutWorker Successful Response
   * @throws ApiError
   */
  public static updateWorker(
    workerId: string,
    requestBody: UpdateWorker
  ): CancelablePromise<OutWorker> {
    return __request(OpenAPI, {
      method: "PUT",
      url: "/worker/{worker_id}",
      path: {
        worker_id: workerId,
      },
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    });
  }

  /**
   * Delete Worker
   * @param workerId
   * @returns any Successful Response
   * @throws ApiError
   */
  public static deleteWorker(workerId: string): CancelablePromise<any> {
    return __request(OpenAPI, {
      method: "DELETE",
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
   * Create Worker
   * @param requestBody
   * @returns OutWorker Successful Response
   * @throws ApiError
   */
  public static createWorker(
    requestBody: CreateWorker
  ): CancelablePromise<OutWorker> {
    return __request(OpenAPI, {
      method: "POST",
      url: "/worker",
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    });
  }

  /**
   * Create Service
   * @param requestBody
   * @returns OutService Successful Response
   * @throws ApiError
   */
  public static createService(
    requestBody: CreateService
  ): CancelablePromise<OutService> {
    return __request(OpenAPI, {
      method: "POST",
      url: "/service",
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    });
  }

  /**
   * Get Services By User
   * @param workerId
   * @returns OutServices Successful Response
   * @throws ApiError
   */
  public static getServicesByUser(
    workerId?: number
  ): CancelablePromise<OutServices> {
    return __request(OpenAPI, {
      method: "GET",
      url: "/services",
      query: {
        worker_id: workerId,
      },
      errors: {
        422: `Validation Error`,
      },
    });
  }

  /**
   * My Create Service
   * @param requestBody
   * @returns OutService Successful Response
   * @throws ApiError
   */
  public static myCreateService(
    requestBody: CreateServiceWithClientId
  ): CancelablePromise<OutService> {
    return __request(OpenAPI, {
      method: "POST",
      url: "/my_service",
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    });
  }

  /**
   * Get Service Must
   * @param serviceId
   * @returns OutService Successful Response
   * @throws ApiError
   */
  public static getServiceMust(
    serviceId: number
  ): CancelablePromise<OutService> {
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
   * Update Service
   * @param serviceId
   * @param requestBody
   * @returns OutService Successful Response
   * @throws ApiError
   */
  public static updateService(
    serviceId: number,
    requestBody: UpdateService
  ): CancelablePromise<OutService> {
    return __request(OpenAPI, {
      method: "POST",
      url: "/service/{service_id}",
      path: {
        service_id: serviceId,
      },
      body: requestBody,
      mediaType: "application/json",
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
   * Add Skills
   * @param requestBody
   * @returns Received Successful Response
   * @throws ApiError
   */
  public static addSkills(requestBody: SkillsIn): CancelablePromise<Received> {
    return __request(OpenAPI, {
      method: "POST",
      url: "/worker_services",
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    });
  }

  /**
   * Add Skill
   * @param requestBody
   * @returns Received Successful Response
   * @throws ApiError
   */
  public static addSkill(requestBody: SkillIn): CancelablePromise<Received> {
    return __request(OpenAPI, {
      method: "POST",
      url: "/worker_service",
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    });
  }

  /**
   * My Add Skill
   * @param requestBody
   * @returns Received Successful Response
   * @throws ApiError
   */
  public static myAddSkill(requestBody: SkillIn): CancelablePromise<Received> {
    return __request(OpenAPI, {
      method: "POST",
      url: "/my_worker_services",
      body: requestBody,
      mediaType: "application/json",
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
   * Create Slot With Check
   * @param requestBody
   * @param force
   * @returns OutSlot Successful Response
   * @throws ApiError
   */
  public static createSlotWithCheck(
    requestBody: CreateSlot,
    force: boolean = false
  ): CancelablePromise<OutSlot> {
    return __request(OpenAPI, {
      method: "POST",
      url: "/slot",
      query: {
        force: force,
      },
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    });
  }

  /**
   * Delete Client Slot
   * @param slotId
   * @returns OutSlot Successful Response
   * @throws ApiError
   */
  public static deleteClientSlot(slotId: number): CancelablePromise<OutSlot> {
    return __request(OpenAPI, {
      method: "DELETE",
      url: "/slot/{slot_id}",
      path: {
        slot_id: slotId,
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
   * Update Visit
   * @param visitId
   * @param requestBody
   * @returns any Successful Response
   * @throws ApiError
   */
  public static updateVisit(
    visitId: string,
    requestBody: InVisit
  ): CancelablePromise<any> {
    return __request(OpenAPI, {
      method: "PUT",
      url: "/visit/{visit_id}",
      path: {
        visit_id: visitId,
      },
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    });
  }

  /**
   * Get Visits
   * @param workerId
   * @returns any Successful Response
   * @throws ApiError
   */
  public static getVisits(workerId?: number): CancelablePromise<any> {
    return __request(OpenAPI, {
      method: "GET",
      url: "/visits",
      query: {
        worker_id: workerId,
      },
      errors: {
        422: `Validation Error`,
      },
    });
  }

  /**
   * Get Visits Days
   * @param requestBody
   * @param workerId
   * @returns VisitsByDays Successful Response
   * @throws ApiError
   */
  public static getVisitsDays(
    requestBody: VisitsByDaysRQ,
    workerId?: number
  ): CancelablePromise<VisitsByDays> {
    return __request(OpenAPI, {
      method: "POST",
      url: "/visits/by_days",
      query: {
        worker_id: workerId,
      },
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

  /**
   * Create Worker Availability
   * @param workerId
   * @param requestBody
   * @returns any Successful Response
   * @throws ApiError
   */
  public static createWorkerAvailability(
    workerId: string,
    requestBody: Availability
  ): CancelablePromise<any> {
    return __request(OpenAPI, {
      method: "POST",
      url: "/worker/{worker_id}/availability",
      path: {
        worker_id: workerId,
      },
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    });
  }

  /**
   * Create File
   * @param formData
   * @returns any Successful Response
   * @throws ApiError
   */
  public static createFile(formData: Body_create_file): CancelablePromise<any> {
    return __request(OpenAPI, {
      method: "POST",
      url: "/file",
      formData: formData,
      mediaType: "multipart/form-data",
      errors: {
        422: `Validation Error`,
      },
    });
  }

  /**
   * Get File
   * @param fileName
   * @returns any Successful Response
   * @throws ApiError
   */
  public static getFile(fileName: string): CancelablePromise<any> {
    return __request(OpenAPI, {
      method: "GET",
      url: "/file/{file_name}",
      path: {
        file_name: fileName,
      },
      errors: {
        422: `Validation Error`,
      },
    });
  }
}
