/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Availability } from '../models/Availability';
import type { AvailabilityPerWorker } from '../models/AvailabilityPerWorker';
import type { Body_create_file_endpoint_file_post } from '../models/Body_create_file_endpoint_file_post';
import type { Body_login_for_access_token_endpoint_token_post } from '../models/Body_login_for_access_token_endpoint_token_post';
import type { CreateService } from '../models/CreateService';
import type { CreateServiceWithClientId } from '../models/CreateServiceWithClientId';
import type { CreateSlot } from '../models/CreateSlot';
import type { CreateWeeklySlot } from '../models/CreateWeeklySlot';
import type { CreateWorker } from '../models/CreateWorker';
import type { InVisit } from '../models/InVisit';
import type { OutService } from '../models/OutService';
import type { OutServices } from '../models/OutServices';
import type { OutVisit } from '../models/OutVisit';
import type { OutWorker } from '../models/OutWorker';
import type { OutWorkers } from '../models/OutWorkers';
import type { Received } from '../models/Received';
import type { SkillIn } from '../models/SkillIn';
import type { SkillsIn } from '../models/SkillsIn';
import type { SkillsOut } from '../models/SkillsOut';
import type { Slot } from '../models/Slot';
import type { TokenOut } from '../models/TokenOut';
import type { UpdateWorker } from '../models/UpdateWorker';
import type { UserCreate } from '../models/UserCreate';
import type { UserOut } from '../models/UserOut';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class DefaultService {

    /**
     * Ping
     * @returns any Successful Response
     * @throws ApiError
     */
    public static pingPingGet(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/ping',
        });
    }

    /**
     * Create User Endpoint
     * @param requestBody
     * @returns TokenOut Successful Response
     * @throws ApiError
     */
    public static createUserEndpointSignupPost(
        requestBody: UserCreate,
    ): CancelablePromise<TokenOut> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/signup',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Read Users Me Endpoint
     * @returns UserOut Successful Response
     * @throws ApiError
     */
    public static readUsersMeEndpointUsersMeGet(): CancelablePromise<UserOut> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/users/me/',
        });
    }

    /**
     * Read Users Me2 Endpoint
     * @returns UserOut Successful Response
     * @throws ApiError
     */
    public static readUsersMe2EndpointMyUserGet(): CancelablePromise<UserOut> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/my_user',
        });
    }

    /**
     * Login For Access Token Endpoint
     * @param formData
     * @returns any Successful Response
     * @throws ApiError
     */
    public static loginForAccessTokenEndpointTokenPost(
        formData: Body_login_for_access_token_endpoint_token_post,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/token',
            formData: formData,
            mediaType: 'application/x-www-form-urlencoded',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Worker Endpoint
     * @param workerId
     * @returns OutWorker Successful Response
     * @throws ApiError
     */
    public static getWorkerEndpointWorkerWorkerIdGet(
        workerId: number,
    ): CancelablePromise<OutWorker> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/worker/{worker_id}',
            path: {
                'worker_id': workerId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Update Worker Endpoint
     * @param workerId
     * @param requestBody
     * @returns OutWorker Successful Response
     * @throws ApiError
     */
    public static updateWorkerEndpointWorkerWorkerIdPut(
        workerId: number,
        requestBody: UpdateWorker,
    ): CancelablePromise<OutWorker> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/worker/{worker_id}',
            path: {
                'worker_id': workerId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Delete Worker Endpoint
     * @param workerId
     * @returns any Successful Response
     * @throws ApiError
     */
    public static deleteWorkerEndpointWorkerWorkerIdDelete(
        workerId: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/worker/{worker_id}',
            path: {
                'worker_id': workerId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Workers By Client Endpoint
     * @param clientId
     * @returns OutWorkers Successful Response
     * @throws ApiError
     */
    public static getWorkersByClientEndpointClientClientIdWorkersGet(
        clientId: number,
    ): CancelablePromise<OutWorkers> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/client/{client_id}/workers',
            path: {
                'client_id': clientId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Workers Endpoint
     * @returns OutWorkers Successful Response
     * @throws ApiError
     */
    public static getWorkersEndpointWorkersGet(): CancelablePromise<OutWorkers> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/workers',
        });
    }

    /**
     * Create Worker Endpoint
     * @param requestBody
     * @returns OutWorker Successful Response
     * @throws ApiError
     */
    public static createWorkerEndpointWorkerPost(
        requestBody: CreateWorker,
    ): CancelablePromise<OutWorker> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/worker',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Create Service Endpoint
     * @param requestBody
     * @returns OutService Successful Response
     * @throws ApiError
     */
    public static createServiceEndpointServicePost(
        requestBody: CreateService,
    ): CancelablePromise<OutService> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/service',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * My Create Service Endpoint
     * @param requestBody
     * @returns OutService Successful Response
     * @throws ApiError
     */
    public static myCreateServiceEndpointMyServicePost(
        requestBody: CreateServiceWithClientId,
    ): CancelablePromise<OutService> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/my_service',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Service Endpoint
     * @param serviceId
     * @returns OutService Successful Response
     * @throws ApiError
     */
    public static getServiceEndpointServiceServiceIdGet(
        serviceId: number,
    ): CancelablePromise<OutService> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/service/{service_id}',
            path: {
                'service_id': serviceId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Service By Client Endpoint
     * @param clientId
     * @param serviceId
     * @returns OutService Successful Response
     * @throws ApiError
     */
    public static getServiceByClientEndpointClientClientIdServiceServiceIdGet(
        clientId: number,
        serviceId: number,
    ): CancelablePromise<OutService> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/client/{client_id}/service/{service_id}',
            path: {
                'client_id': clientId,
                'service_id': serviceId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Services By Client Endpoint
     * @param clientId
     * @param workerId
     * @returns OutServices Successful Response
     * @throws ApiError
     */
    public static getServicesByClientEndpointClientClientIdServicesGet(
        clientId: number,
        workerId?: number,
    ): CancelablePromise<OutServices> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/client/{client_id}/services',
            path: {
                'client_id': clientId,
            },
            query: {
                'worker_id': workerId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Add Skills Endpoint
     * @param requestBody
     * @returns Received Successful Response
     * @throws ApiError
     */
    public static addSkillsEndpointWorkerServicesPost(
        requestBody: SkillsIn,
    ): CancelablePromise<Received> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/worker_services',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Add Skill Endpoint
     * @param requestBody
     * @returns Received Successful Response
     * @throws ApiError
     */
    public static addSkillEndpointWorkerServicePost(
        requestBody: SkillIn,
    ): CancelablePromise<Received> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/worker_service',
            body: requestBody,
            mediaType: 'application/json',
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
    public static myAddSkillMyWorkerServicesPost(
        requestBody: SkillIn,
    ): CancelablePromise<Received> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/my_worker_services',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Skills Endpoint
     * @param clientId
     * @param workerId
     * @returns SkillsOut Successful Response
     * @throws ApiError
     */
    public static getSkillsEndpointClientClientIdPickerServicesGet(
        clientId: number,
        workerId?: number,
    ): CancelablePromise<SkillsOut> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/client/{client_id}/picker/services',
            path: {
                'client_id': clientId,
            },
            query: {
                'worker_id': workerId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Create Slot Endpoint
     * @param requestBody
     * @returns Slot Successful Response
     * @throws ApiError
     */
    public static createSlotEndpointSlotPost(
        requestBody: CreateSlot,
    ): CancelablePromise<Slot> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/slot',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Delete Client Slot Endpoint
     * @param slotId
     * @returns Slot Successful Response
     * @throws ApiError
     */
    public static deleteClientSlotEndpointSlotSlotIdDelete(
        slotId: number,
    ): CancelablePromise<Slot> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/slot/{slot_id}',
            path: {
                'slot_id': slotId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Create Client Weekly Slot Endpoint
     * @param clientId
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public static createClientWeeklySlotEndpointClientClientIdClientWeeklySlotPost(
        clientId: number,
        requestBody: CreateWeeklySlot,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/client/{client_id}/client_weekly_slot',
            path: {
                'client_id': clientId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Create Worker Weekly Slot Endpoint
     * @param workerId
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public static createWorkerWeeklySlotEndpointWorkerWeeklySlotWorkerIdPost(
        workerId: number,
        requestBody: CreateWeeklySlot,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/worker_weekly_slot/{worker_id}',
            path: {
                'worker_id': workerId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Visit Endpoint
     * @param visitId
     * @returns OutVisit Successful Response
     * @throws ApiError
     */
    public static getVisitEndpointVisitVisitIdGet(
        visitId: number,
    ): CancelablePromise<OutVisit> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/visit/{visit_id}',
            path: {
                'visit_id': visitId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Update Visit Endpoint
     * @param visitId
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public static updateVisitEndpointVisitVisitIdPut(
        visitId: string,
        requestBody: InVisit,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/visit/{visit_id}',
            path: {
                'visit_id': visitId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Visits Endpoint
     * @param workerId
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getVisitsEndpointVisitsGet(
        workerId?: number,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/visits',
            query: {
                'worker_id': workerId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Create Visit Slot Endpoint
     * @param requestBody
     * @returns OutVisit Successful Response
     * @throws ApiError
     */
    public static createVisitSlotEndpointVisitPost(
        requestBody: CreateSlot,
    ): CancelablePromise<OutVisit> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/visit',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Public Book Visit Endpoint
     * @param requestBody
     * @returns OutVisit Successful Response
     * @throws ApiError
     */
    public static publicBookVisitEndpointPublicVisitPost(
        requestBody: InVisit,
    ): CancelablePromise<OutVisit> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/public/visit',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Worker Availability Endpoint
     * @param workerId
     * @param services
     * @returns Availability Successful Response
     * @throws ApiError
     */
    public static getWorkerAvailabilityEndpointClientClientIdWorkerWorkerIdAvailabilityGet(
        workerId: number,
        services?: string,
    ): CancelablePromise<Availability> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/client/{client_id}/worker/{worker_id}/availability',
            path: {
                'worker_id': workerId,
            },
            query: {
                'services': services,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Client Availability Endpoint
     * @param clientId
     * @param services
     * @returns AvailabilityPerWorker Successful Response
     * @throws ApiError
     */
    public static getClientAvailabilityEndpointClientClientIdAvailabilityGet(
        clientId: number,
        services?: string,
    ): CancelablePromise<AvailabilityPerWorker> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/client/{client_id}/availability/',
            path: {
                'client_id': clientId,
            },
            query: {
                'services': services,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Create File Endpoint
     * @param formData
     * @returns any Successful Response
     * @throws ApiError
     */
    public static createFileEndpointFilePost(
        formData: Body_create_file_endpoint_file_post,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/file',
            formData: formData,
            mediaType: 'multipart/form-data',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get File Endpoint
     * @param fileName
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getFileEndpointFileFileNameGet(
        fileName: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/file/{file_name}',
            path: {
                'file_name': fileName,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

}
