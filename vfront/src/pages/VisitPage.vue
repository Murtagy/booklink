<!-- Main page of visit booking process.
 Visit page is in control of fetching the data and setting the props of other components
 Other pages are considered sub-pages and are not independant -->

<template>
  <div>
    <wide-header :title="current_screen_title" />

    <div class="box">
      <form v-if="current_screen == 'start'">
        <ul>
          <li>
            <button
              class="menu"
              @click="
                changeCurrentScreen(
                  'visit-select-service',
                  (current_screen_title = 'Выбор услуги'),
                )
              "
            >
              <img src="../assets/list-icon.jpg" />Услуга
            </button>

            <span v-if="checked_services.length != 0">
              <p
                v-for="service in checked_services"
                :key="String(service.service_id)"
              >
                {{ service.name }} {{ service.price }} {{ service.currency }}
              </p>
            </span>
          </li>
          <li>
            <button
              class="menu"
              @click="
                changeCurrentScreen('visit-select-worker', 'Выбор исполнителя')
              "
            >
              <img src="../assets/worker-icon.png" />Сотрудник
            </button>

            <span v-if="worker != null" class="selected">
              {{ worker.name }}
            </span>
          </li>
          <li v-show="checked_services.length > 0">
            <button
              class="menu"
              @click="
                changeCurrentScreen('visit-select-datetime', 'Выбор даты')
              "
            >
              <img src="../assets/calendar-icon.png" />Дата и время
            </button>
            <span v-if="visit_slot != null" class="selected">
              Дата и время {{ visit_slot }}
            </span>
          </li>
        </ul>
        <input
          type="button"
          class="sticky_button"
          value="Сформировать запись"
          @click="
            changeCurrentScreen(
              'visit-details',
              (current_screen_title = 'Подтверждение записи'),
            )
          "
        />
      </form>

      <visit-select-service
        v-if="current_screen == 'visit-select-service'"
        @go-start-screen="changeToStartScreen()"
        @check-services="applyCheckedServices"
        :services="services"
        :alreadyCheckedServices="checked_services"
      />
      <visit-select-worker
        v-if="current_screen == 'visit-select-worker'"
        @go-start-screen="changeToStartScreen()"
        @select-worker="applySelectedWorker"
        v-bind:workers="workers"
      />
      <visit-select-datetime
        v-if="current_screen == 'visit-select-datetime' && availability"
        @go-start-screen="changeToStartScreen()"
        @select-datetime="applySelectedDateTime"
        v-bind:availability="availability"
      />
      <visit-details
        v-if="
          current_screen == 'visit-details' && worker && visit_slot && client_id
        "
        @go-start-screen="changeToStartScreen()"
        :client_id="client_id"
        :worker="worker"
        :visit_slot="visit_slot"
        :services="checked_services"
      />
    </div>
  </div>
</template>

<style scoped src="@/assets/styles/visit.css"></style>

<script lang="ts">
import WideHeader from "@/components/WideHeader.vue";
import VisitSelectDatetime from "@/components/VisitSelectDatetime.vue";
import VisitSelectService from "@/components/VisitSelectService.vue";
import VisitSelectWorker from "@/components/VisitSelectWorker.vue";
import VisitDetails from "@/components/VisitDetails.vue";

import availability_mock from "@/mocks/availability_mock.js";
import services_mock from "@/mocks/services_mock.js";
import workers_mock from "@/mocks/workers_mock.js";
import type { AxiosError } from "axios";

import { DefaultService } from "@/client";
import type { OutWorker } from "@/client/models/OutWorker";
import type { OutService } from "@/client/models/OutService";
import type { Availability } from "@/client/models/Availability";
import type { TimeSlot } from "@/models/availability/TimeSlot";
// import type { AvailabilityPerWorker } from "@/client/models/AvailabilityPerWorker";

declare interface ComponentData {
  availability: Availability | null;
  checked_services: OutService[];
  client_id: number | null;
  current_screen: string;
  current_screen_title: string;
  services: OutService[];
  visit_slot: TimeSlot | null;
  worker: OutWorker | null;
  workers: OutWorker[];
}

export default {
  components: {
    VisitDetails,
    VisitSelectDatetime,
    VisitSelectService,
    VisitSelectWorker,
    WideHeader,
  },
  data(): ComponentData {
    var services: OutService[] = [];
    var workers: OutWorker[] = [];
    if (import.meta.env.VITE_APP_OFFLINE == "true") {
      services = services_mock["mock"];
      workers = workers_mock["mock"];
    }
    const worker: Worker | null = null;
    return {
      availability: null, // availability is mocked at get av
      checked_services: [],
      client_id: null, // sets when mounted
      current_screen: "start",
      current_screen_title: "Онлайн запись",
      services: services,
      visit_slot: null,
      worker: worker,
      workers: workers,
      // todo: add loading (passed to child components and renders loading screen while something is loaded)
      // todo: expose selection in the path; https://forum.vuejs.org/t/how-to-restore-the-exact-state-of-a-route-when-clicking-the-back-button/109105/6
    };
  },
  computed: {
    checkedServicesIds() {
      const services_ids = this.checked_services.map((s) => {
        return s.service_id;
      });

      if (services_ids.length == 0) {
        return undefined;
      }
      return services_ids.join(",");
    },
  },
  watch: {
    checked_services() {
      this.getWorkers();
    },
    services() {
      for (const checked_service of this.checked_services) {
        let in_checked = false;
        for (const service of this.services) {
          if (service.service_id == checked_service.service_id) {
            in_checked = true;
          }
        }
        if (!in_checked) {
          // picked service is not in the new list - we must flush the selections
          this.checked_services = [];
          return;
        }
      }
    },
    worker() {
      this.availability = null;
      this.getAvailability();
      this.getServices();
    },
  },
  mounted() {
    this.client_id =
      this.$route.query.org || import.meta.env.VITE_APP_CLIENT_ID; // setting null to avoid undefined

    this.getWorkers();
    this.getServices();
    // alert(`client_id ${this.client_id}`)
  },
  methods: {
    getClientId(): number {
      if (!this.client_id) {
        throw Error("Client id not set");
      }
      return this.client_id;
    },
    changeCurrentScreen: function (screen: string, screen_title: string) {
      console.log("Change screen!", screen, screen_title);
      this.current_screen = screen;
      this.current_screen_title = screen_title;
    },
    changeToStartScreen: function () {
      console.log("Change screen!");
      this.current_screen = "start";
      this.current_screen_title = "Онлайн запись";
    },
    applyCheckedServices: function (x: OutService[]) {
      this.checked_services = x;
      this.getAvailability();
      this.changeToStartScreen();
    },
    applySelectedWorker: function (x: OutWorker | null) {
      this.worker = x;
      this.changeToStartScreen();
    },
    applySelectedDateTime: function (date: string, slot: TimeSlot) {
      console.log(date, slot);
      this.visit_slot = slot;
      this.changeToStartScreen();
    },
    async getWorkers() {
      if (import.meta.env.VITE_APP_OFFLINE == "true") {
        return;
      }

      try {
        const workers = await DefaultService.getWorkersByClient(
          this.getClientId(),
          this.checkedServicesIds,
        );
        this.workers = workers.workers;
        console.log("Got workers", workers);
      } catch (error) {
        console.log(error);
      }
    },
    async getServices() {
      if (import.meta.env.VITE_APP_OFFLINE == "true") {
        return;
      }
      var workerId;
      if (this.worker?.worker_id) {
        workerId = Number.parseInt(this.worker.worker_id);
      }
      try {
        const services_response = await DefaultService.getServicesByClient(
          this.getClientId(),
          workerId,
        );
        this.services = services_response.services;

        // no need for auth here, keeping for example use
        // {"headers": {'Authorization': 'bearer ' + this.$authStore.state.jwt_auth}}
      } catch (error: any | AxiosError) {
        console.log(error);
      }
    },
    async getAvailability() {
      console.log("Getting availability");
      // sets this.availability
      if (import.meta.env.VITE_APP_OFFLINE == "true") {
        this.availability = this.parseAvailability(availability_mock["mock"]);
      }

      try {
        if (this.worker == null) {
          // r = await DefaultService.getClientAvailability(this.getClientId(), picked_services_str)
          return;
        }
        const r = await DefaultService.getWorkerAvailability(
          String(this.getClientId()),
          this.worker.worker_id,
          this.checkedServicesIds,
        );
        this.availability = this.parseAvailability(r);
      } catch (error: any | AxiosError) {
        console.log(error);
      }
    },
    parseAvailability(a: Availability): Availability {
      // should be a single Availability type here
      console.log("Parsing...", a);
      if ("days" in a) {
        return a;
      }
      // TODO
      throw Error("not implemented");
    },
  },
};
</script>
