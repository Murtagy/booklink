<template>
  <!-- <div class="box" style="display: flex; flex-flow: row wrap; width: 100%"> -->

  <div class="calendar" style="display: flex; flex-flow: row wrap">
    <div
      class="calendar__hour-grid"
      v-for="day in days"
      :key="day.worker.worker_id"
    >
      {{ day.worker.name }}
      <div
        class="calendar__hour"
        v-for="hour in getHours(day)"
        :key="hour.number"
        @click="clickHour($event, hour, day)"
        :style="{
          'background-color': isAvailable(hour, day)
            ? 'white'
            : 'lightsteelblue',
        }"
      >
        <label style="float: left">{{ hour.number }}</label>
        <!-- {{ hour.events }} -->
        <div
          v-if="shouldRenderForm(hour, day)"
          id="form-container"
          tabindex="0"
          @keydown.esc="hour_form = undefined"
          @click="closeFormIfClickedOutside($event)"
        >
          <div id="form-content">
            <CreateVisitPage
              :date="day.date"
              :time_in="getTime(hour)"
              :worker_in="day.worker"
            />
            <!-- @created-visit="hour.events.push($event.slot)" -->
            <div></div>

            <div
              v-for="visit of getVisits(hour)"
              :key="visit.visit.slot_id"
              style="
                width: 100%;
                background-color: red;
                opacity: 0.2;
                position: absolute;
                border: 1px solid;
              "
              :style="{ height: hour_height * getVisitHours(visit) + 'em' }"
            ></div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <!-- </div> -->
</template>

<style scoped>
/* https://dev.to/crayoncode/building-a-vertical-calendar-with-html-css-js-2po2 */

calendar__hour-grid {
  width: v-bind(hour_width + "em");
}
.calendar__hour {
  border: 1px groove;
  height: v-bind(hour_height + "em");
  width: v-bind(hour_width + "em");
}
</style>

<script lang="ts">
// import VisitsDayCaruselDay from "@/components/VisitsDayCaruselDay.vue";

import type {
  OutVisitExtended,
  OutWorker,
  TimeSlot,
  WorkerDay,
} from "@/client";
import dayjs from "dayjs";
import type { PropType } from "vue";
import CreateVisitPage from "@/pages/CreateVisitPage.vue";

declare interface Hour {
  number: number;
  events: (TimeSlot | OutVisitExtended)[];
}

declare interface HourForm {
  hour: Hour;
  worker: OutWorker;
}

declare interface Data {
  hour_height: number;
  hour_width: number;
  hour_form?: HourForm;
}

export default {
  components: { CreateVisitPage },
  computed: {
    // workers() {
    // for (let job_hour in days.
    // },
  },
  data(): Data {
    return {
      hour_height: 2,
      hour_width: 7,
      hour_form: undefined,
    };
  },
  methods: {
    shouldRenderForm(h: Hour, day: WorkerDay) {
      if (this.hour_form == undefined) {
        console.log("not render");
        return false;
      }
      if (
        this.hour_form.hour.number == h.number &&
        this.hour_form.worker.worker_id == day.worker.worker_id
      ) {
        console.log("render", this.hour_form);
        return true;
      }
      return false;
    },
    closeFormIfClickedOutside(e: MouseEvent) {
      if (
        e.target != null &&
        (e.target as HTMLElement).id == "form-container"
      ) {
        this.hour_form = undefined;
      }
    },
    clickHour(e: MouseEvent, h: Hour, day: WorkerDay) {
      // console.log("click", e.target);
      if (
        e.target != null &&
        (e.target as HTMLElement).id == "form-container"
      ) {
        return;
      }
      if (!this.hour_form) {
        this.hour_form = {
          hour: h,
          worker: day.worker,
        };
      }
    },
    isAvailable(h: Hour, d: WorkerDay) {
      for (const jh of d.job_hours) {
        const from = dayjs(jh.from_datetime);
        const to = dayjs(jh.to_datetime);
        if (h.number >= from.hour() && h.number <= to.hour()) {
          return true;
        }
      }
      return false;
    },
    getTime(h: Hour) {
      // todo : lookup minutes
      return String(h.number).padStart(2, "0") + ":00";
    },
    getVisitHours(v: OutVisitExtended): number {
      const length_hours =
        dayjs(v.visit.to_datetime).hour() -
        dayjs(v.visit.from_datetime).hour() +
        1;
      return length_hours;
    },
    getVisits(h: Hour): OutVisitExtended[] {
      const out: OutVisitExtended[] = [];
      for (const event of h.events) {
        if ((event as OutVisitExtended).visit != undefined) {
          out.push(event as OutVisitExtended);
        }
      }
      return out;
    },
    getHours(day: WorkerDay): Hour[] {
      const hours: Hour[] = [];
      for (var i = 0; i < 24; i++) {
        const events = [];
        for (const e of day.job_hours) {
          if (dayjs(e.from_datetime).hour() == i) {
            events.push(e);
          }
        }
        for (const e of day.visit_hours) {
          if (dayjs(e.visit.from_datetime).hour() == i) {
            events.push(e);
          }
        }
        hours.push({ number: i, events: events });
      }
      return hours;
    },
  },
  props: {
    days: {
      type: Object as PropType<WorkerDay[]>,
    },
  },
};
</script>
