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
                  (current_screen_title = 'Выбор услуги')
                )
              "
            >
              <img src="../assets/list-icon.jpg" />Услуга
            </button>

            <span v-if="checked_services.length != 0">
              <p v-for="service in checked_services" :key="service.id">
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
            <span v-if="visit_time != null" class="selected">
              Дата и время {{ visit_time }}
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
              (current_screen_title = 'Подтверждение записи')
            )
          "
        />
      </form>

      <visit-select-service
        v-if="current_screen == 'visit-select-service'"
        @go-start-screen="changeToStartScreen()"
        @check-services="applyCheckedServices"
        v-bind:services="services"
      />
      <visit-select-worker
        v-if="current_screen == 'visit-select-worker'"
        @go-start-screen="changeToStartScreen()"
        @select-worker="applySelectedWorker"
        v-bind:workers="workers"
      />
      <visit-select-datetime
        v-if="current_screen == 'visit-select-datetime'"
        @go-start-screen="changeToStartScreen()"
        @select-datetime="applySelectedDateTime"
        v-bind:availability="availability"
      />
      <visit-details
        v-if="current_screen == 'visit-details'"
        @go-start-screen="changeToStartScreen()"
        :worker="worker"
        :visit_time="visit_time"
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
import type { AxiosError, AxiosResponse } from "axios";

import {Services} from "@/models/Services"


export default {
  components: {
    VisitDetails,
    VisitSelectDatetime,
    VisitSelectService,
    VisitSelectWorker,
    WideHeader,
  },
  data() {
    var availability = null;
    var services = new Services([]);
    var workers = [];
    if (import.meta.env.VITE_APP_OFFLINE == "true") {
      availability = availability_mock["mock"];
      services = services_mock["mock"];
      workers = workers_mock["mock"];
    }
    return {
      availability: availability,
      checked_services: [],
      client_id: null, // sets when mounted
      current_screen: "start",
      current_screen_title: "Онлайн запись",
      services: services,
      visit_time: null,
      worker: null,
      workers: workers,
      // todo: add loading (passed to child components and renders loading screen while something is loaded)
      // todo: expose selection in the path; https://forum.vuejs.org/t/how-to-restore-the-exact-state-of-a-route-when-clicking-the-back-button/109105/6
    };
  },
  computed: {
    checkedServicesIds() {
      return this.checked_services.map((s) => {
        return s.service_id;
      });
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
    // todo: flush selection (something has been selected, current availability might be wrong)
    applyCheckedServices: function (x: object) {
      this.checked_services = x;
      this.getAvailability();
      this.changeToStartScreen();
    },
    applySelectedWorker: function (x: object) {
      this.worker = x;
      this.changeToStartScreen();
    },
    applySelectedDateTime: function (date: string, slot: object) {
      // todo: slots are parsed in a map atm, date: bool, not sure why did it, might be better to parse that into a simple array
      console.log(date, slot);
      this.visit_time = slot;
      this.changeToStartScreen();
    },
    async getWorkers() {
      if (import.meta.env.VITE_APP_OFFLINE == "true") {
        return;
      }

      let path = `/client/${this.client_id}/workers`;
      try {
        const response = await this.$api.get(path);
        if (response.data == null) {
          console.log("Got workers", response);
          alert("Empty");
        } else {
          let workers = response.data.workers;
          console.log("Got workers", response);
          this.workers = this.parseWorkers(workers);
        }
      } catch (error) {
        console.log(error);
      }
    },
    parseWorkers(w: object) {
      // todo
      console.log(w);
      return w;
    },
    async getServices() {
      if (import.meta.env.VITE_APP_OFFLINE == "true") {
        return;
      }

      let path = `/client/${this.client_id}/services`;
      try {
        const response: AxiosResponse<Services> = await this.$api.get<Services>(
          path
          // no need for auth here, keeping for example use
          // {"headers": {'Authorization': 'bearer ' + this.$authStore.state.jwt_auth}}
        );
        if (response.data == null) {
          console.log("Got services", response);
          alert("Empty");
        } else {
          console.log("Got services", response.data);
          this.services = this.parseResponse(response);
        }
      } catch (error: any | AxiosError) {
        console.log(error);
      }
    },
    parseResponse(r: AxiosResponse<Services>): Services {
      // todo
      console.log(r);
      return new Services(r.data.services);
    },
    async getAvailability() {
      // sets this.availability

      // todo: check if called in offline
      function handle_av_error(error: any | AxiosError) {
        console.log(error);
      }
      function _handle_av_response(response: AxiosResponse) {
        if (response.data == null) {
          console.log("GOT AVAILABILITY", response);
          alert("Empty");
        } else {
          let availability = response.data.availability;
          console.log("GOT AVAILABILITY", response);
          this.availability = this.parseAvailability(availability);
        }
      }
      const handle_av_response = _handle_av_response.bind(this);

      console.log("Getting availability");
      let path = `/client/${this.client_id}/availability`;
      if (this.worker != null) {
        path = `/client/${this.client_id}/worker/${this.worker.worker_id}/availability`;
      }
      if (this.checked_services.length > 0) {
        path += `?services=${this.checkedServicesIds.join(",")}`;
      }
      // todo add workers
      try {
        const response = await this.$api.get(
          path
          // no need for auth here, keeping for example use
          // {"headers": {'Authorization': 'bearer ' + this.$authStore.state.jwt_auth}}
        );
        handle_av_response(response);
      } catch (error: any | AxiosError) {
        handle_av_error(error);
      }
    },
    parseAvailability(a: object) {
      console.log("Parsing...", a);
      const av = {};
      for (const worker_av of Object.values(a)) {
        // console.log('worker_av', worker_av)
        for (const row of worker_av["days"]) {
          // console.log('row', row)
          const dt = row["date"];
          for (const ts of row["timeslots"]) {
            let _date;
            if (av[dt] != null) {
              _date = av[dt];
            } else {
              _date = {};
            }
            const from = ts["dt_from"];
            _date[from] = true;
            av[dt] = _date;
          }
        }
      }
      console.log("Parsed");

      return av;
    },
  },
};
</script>
