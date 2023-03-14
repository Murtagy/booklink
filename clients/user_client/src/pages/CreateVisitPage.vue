<template>
  <form @submit.prevent="submitForm">
    <label for="name">Клиент </label>
    <input id="name" />
    <br />

    <label for="visittime">Время </label>
    <input id="visittime" type="time" v-model="time" required />
    <br />

    <br />
    Услуги

    <div style="border: 1px solid var(--color1)">
      <div style="overflow-y: scroll; height: 5em">
        <div v-for="service in services" @click="selectService(service)">
          <input
            type="checkbox"
            v-bind:checked="selected_services.includes(service)"
          />
          <span style="list-style-type: none">{{ service.name }}</span>
        </div>
      </div>
    </div>

    Продолжительность
    <select v-model="length_hours">
      <option value="0">0 ч</option>
      <option value="1">1 ч</option>
      <option value="2">2 ч</option>
      <option value="3">3 ч</option>
      <option value="4">4 ч</option>
      <option value="5">5 ч</option>
      <option value="6">6 ч</option>
      <option value="7">7 ч</option>
      <option value="8">8 ч</option>
      <option value="9">9 ч</option>
    </select>

    <select v-model="length_minutes">
      <option value="0">00 мин</option>
      <option value="05">05 мин</option>
      <option value="10">10 мин</option>
      <option value="15">15 мин</option>
      <option value="20">20 мин</option>
      <option value="25">25 мин</option>
      <option value="30">30 мин</option>
      <option value="35">35 мин</option>
      <option value="40">40 мин</option>
      <option value="45">45 мин</option>
      <option value="50">50 мин</option>
      <option value="55">55 мин</option>
    </select>

    <br />
    Юнит
    <select v-model="selected_worker">
      <option v-for="worker in workers" :value="worker">
        {{ worker.name }}
      </option>
    </select>

    <br />
    Напомнить?
    <input type="checkbox" id="checkbox" v-model="notify" />

    <br />

    <div v-if="show_pick_worker_please" style="border: 1px; background: tomato">
      <p class="bold">Время недоступно, уточните юнит</p>
    </div>
    <div v-if="show_force" style="border: 1px; background: tomato">
      <p class="bold">
        Время недоступно (другой визит или нет расписания), все равно сохранить?
      </p>
      <input type="checkbox" v-model="force" />
    </div>

    <button class="save" type="submit">Сохранить</button>
  </form>
</template>

<style scoped></style>

<script lang="ts">
import {
  DefaultService,
  TimeSlotType,
  type OutService,
  type OutWorker,
} from "@/client";
import dayjs from "dayjs";

declare interface Data {
  force: boolean;
  show_force: boolean;
  show_pick_worker_please: boolean;
  date_parsed: dayjs.Dayjs;
  length_hours: number;
  length_minutes: number;
  notify: boolean;
  services: OutService[];
  selected_worker?: OutWorker;
  selected_services: OutService[];
  time?: string;
  workers: OutWorker[];
}

export default {
  data(): Data {
    const services: OutService[] = [];
    const workers: OutWorker[] = [];

    return {
      force: false,
      show_force: false,
      show_pick_worker_please: false,
      date_parsed: dayjs(this.date),
      length_hours: 0,
      length_minutes: 30,
      notify: false,
      services: services,
      selected_worker: undefined,
      selected_services: [],
      time: undefined,
      workers: workers,
    };
  },
  async mounted() {
    this.workers = (await DefaultService.getWorkers()).workers;
    this.services = (await DefaultService.getServicesByUser()).services;
  },
  methods: {
    selectService(service: OutService) {
      if (this.selected_services.includes(service)) {
        this.selected_services = this.selected_services.filter(
          (s) => s != service
        );
      } else {
        this.selected_services = this.selected_services.concat([service]); // triggering watcher
      }
    },
    SlotIsOccupiedAreYouSure() {
      this.show_force = true;
    },
    SlotIsOccupiedPickWorkerPlease() {
      this.show_pick_worker_please = true;
    },
    WorkerIsNotSkilled() {
      alert("Service not available at unit");
    },
    async submitForm() {
      let worker_id;
      if (this.selected_worker?.worker_id) {
        worker_id = parseInt(this.selected_worker.worker_id);
      }
      if (this.time == undefined) {
        return;
      }
      const time_h = parseInt(this.time.split(":")[0]);
      const time_m = parseInt(this.time.split(":")[1]);
      const date_from = this.date_parsed.add(time_h, "h").add(time_m, "m");
      const date_to = date_from
        .add(this.length_hours, "h")
        .add(this.length_minutes, "m");
      try {
        await DefaultService.createSlotWithCheck(
          {
            slot_type: TimeSlotType.VISIT,
            worker_id: worker_id,
            from_datetime: date_from.toISOString(),
            to_datetime: date_to.toISOString(),
            customer_info: {},
            services: this.selected_services.map((x) => {
              return { service_id: x.service_id };
            }),
            has_notification: this.notify,
          },
          this.force
        );
        this.$router.back();
      } catch (e: any) {
        if (e.status && e.status == 409) {
          if (worker_id) {
            this.SlotIsOccupiedAreYouSure();
          } else {
            this.SlotIsOccupiedPickWorkerPlease();
          }
        }
        if (
          e.status &&
          e.status == 404 &&
          e.body.details == "Worker not skilled of a service"
        ) {
          this.WorkerIsNotSkilled();
        }
      }
    },
  },
  watch: {
    selected_services() {
      let i = 0;
      this.selected_services.forEach((s) => (i += s.minutes));
      this.length_minutes = i % 60;
      this.length_hours = (i - this.length_minutes) / 60;
    },
  },
  props: {
    date: {
      type: String,
      required: true,
    },
  },
};
</script>
