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
        @dragover.prevent
        @drop="dropVisitAtHour($event, hour, day)"
        hour="true"
        :style="{
          'background-color': 'lightsteelblue',
        }"
      >
        <div
          v-for="working_slot of availableSlots(hour, day)"
          class="available_slot"
          :key="String(working_slot.from_datetime)"
          @click="clickHourSlot($event, hour, working_slot, day)"
          style="
            background-color: rgba(255, 255, 255);
            position: absolute;
            border-bottom: 1px solid gray;
            border-top: 1px solid gray;
          "
          :style="{
            height:
              hour_height *
                (Math.min(
                  working_slot.to_datetime.diff(
                    working_slot.from_datetime,
                    'minute'
                  ) / 60
                ),
                1) +
              'em',
            width: hour_width + 'em',
            marginTop:
              (working_slot.from_datetime.minute() / 64) * hour_height + 'em',
            // 64 is used insteaf of 60 to avoid border thickness between 2 visits
          }"
        >
          <!-- {{working_slot}} -->
        </div>
        <label style="float: left; position: relative; z-index: 1">{{
          hour.number
        }}</label>
        <div
          v-for="visit of getVisits(hour)"
          :key="visit.visit.slot_id"
          class="visit"
          draggable="true"
          @dragstart="startDragVisit($event, visit, day)"
          @dragend="endDragVisit($event, visit)"
          style="
            background-color: rgba(255, 0, 0, 0.2);
            position: absolute;
            border-bottom: 1px solid gray;
            border-top: 1px solid gray;
          "
          :style="{
            height: hour_height * getVisitHours(visit) + 'em',
            width: hour_width + 'em',
            marginTop:
              (dayjs(visit.visit.from_datetime).minute() / 64) * hour_height +
              'em',
            // 64 is used insteaf of 60 to avoid border thickness between 2 visits
          }"
          @click="clickVisit($event, visit)"
        >
          <!-- {{ visit.services }} -->
        </div>
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
              :time_in="getPossibleVisitTime(hour, day)"
              :worker_in="day.worker"
              :route_back="false"
              @created-visit="
                handleCreatedVisit($event.slot, day);
                hour_form = undefined;
              "
            />
          </div>
        </div>
      </div>
    </div>
  </div>
  <div
    v-if="visit_info"
    class="visit_card"
    :style="{ top: visit_info.clientY + 'px', left: visit_info.clientX + 'px' }"
  >
    <!-- TODO: replace with component? -->

    <p
      @click="visit_info = undefined"
      style="
        float: right;
        margin-right: 3px;
        border: 1px solid;
        border-radius: 1em;
        width: 1em;
      "
    >
      <center>x</center>
    </p>
    <img
      src="@/assets/edit.svg"
      @click="
        $router.push({
          name: 'visit.edit',
          params: { visit_id: visit_info.visit.visit.slot_id }, // ts is weird - visit_info is guaranteed
        })
      "
      style="float: right; height: 1em; margin-top: 1em"
    />
    <p class="bold">Время</p>
    <p>
      {{ dayjs(visit_info.visit.visit.from_datetime).format("hh:mm") }}
      -
      {{ dayjs(visit_info.visit.visit.to_datetime).format("hh:mm") }}
    </p>
    <h3>Услуги</h3>
    <p>{{ visit_info.visit.services }}</p>
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

.visit_card {
  padding: 1em;
  position: absolute;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0px 0px 5px 0px rgba(0, 0, 0, 0.75);
  z-index: 1;
}

.dragging {
  border: 5px solid black;
}
</style>

<script lang="ts">
// import VisitsDayCaruselDay from "@/components/VisitsDayCaruselDay.vue";

import {
  DefaultService,
  type OutSlot,
  type OutVisitExtended,
  type OutWorker,
  type TimeSlot,
  type WorkerDay,
} from "@/client";
import dayjs from "dayjs";
import type { PropType } from "vue";
import CreateVisitPage from "@/pages/CreateVisitPage.vue";

type Hour = {
  number: number;
  events: (TimeSlot | OutVisitExtended | OutSlot)[];
};

type AvailableTimeSlot = {
  from_datetime: dayjs.Dayjs;
  to_datetime: dayjs.Dayjs;
};
declare interface HourForm {
  hour: Hour;
  minute: number;
  worker: OutWorker;
}

declare interface VisitDragInfo {
  visit: OutVisitExtended;
  day: WorkerDay;
}

declare interface VisitClickInfo {
  clientX: number;
  clientY: number;
  visit: OutVisitExtended;
}

declare interface Data {
  hour_height: number;
  hour_width: number;
  hour_form?: HourForm;
  visit_info?: VisitClickInfo;
  dragged_visit_info?: VisitDragInfo;
}

export default {
  components: { CreateVisitPage },
  computed: {},
  data(): Data {
    return {
      hour_height: 2,
      hour_width: 7,
      hour_form: undefined,
      visit_info: undefined,
      dragged_visit_info: undefined,
    };
  },
  methods: {
    startDragVisit(e: DragEvent, visit: OutVisitExtended, day: WorkerDay) {
      (e.target as HTMLElement).classList.add("dragging");
      this.dragged_visit_info = { visit: visit, day: day };
    },
    endDragVisit(e: DragEvent, visit: OutVisitExtended) {
      (e.target as HTMLElement).classList.remove("dragging");
      this.dragged_visit_info = undefined;
    },
    async dropVisitAtHour(e: Event, h: Hour, d: WorkerDay) {
      // dragged data has short TTL, so it is ok to modify it
      const dragged_visit_info = this.dragged_visit_info;
      if (dragged_visit_info != undefined) {
        const day_ref = dragged_visit_info.day;
        const visit = dragged_visit_info.visit;
        // remove visit from old place (for case when we re-render)
        day_ref.visit_hours = day_ref.visit_hours.filter((x) => x != visit);

        const length = dayjs(dragged_visit_info.visit.visit.to_datetime).diff(
          dragged_visit_info.visit.visit.from_datetime
        );
        const new_start = dayjs(dragged_visit_info.visit.visit.to_datetime).set(
          "hour",
          h.number
        );
        const new_end = new_start.add(length);
        console.log(new_start);

        // server sync
        try {
          await DefaultService.updateSlot(
            dragged_visit_info.visit.visit.slot_id,
            {
              from_datetime: new_start.toISOString(),
              to_datetime: new_end.toISOString(),
              worker_id: parseInt(d.worker.worker_id),
            }
          );
        } catch (error) {
          return;
        }

        // BUG: need to remove from old day? (for case when we re-render - would come back if toggle days forward and back)

        // modify visit to reflect new time and put into the day
        visit.visit.from_datetime = new_start.toISOString();
        visit.visit.to_datetime = new_end.toISOString();
        d.visit_hours.push(visit);
      }
    },
    consoleLog(e: any) {
      console.log(e);
    },
    clickVisit(e: MouseEvent, visit: OutVisitExtended) {
      console.log("open visit", e.clientX, e.clientY);
      this.visit_info = {
        clientX: e.clientX,
        clientY: e.clientY,
        visit: visit,
      };
    },
    async handleCreatedVisit(slot: OutSlot, d: WorkerDay) {
      const extended = await DefaultService.getVisitExtended(slot.slot_id);
      d.visit_hours.push(extended);
    },
    shouldRenderForm(h: Hour, day: WorkerDay): boolean {
      if (this.hour_form == undefined) {
        return false;
      }
      if (
        this.hour_form.hour.number == h.number &&
        this.hour_form.worker.worker_id == day.worker.worker_id
      ) {
        return true;
      }
      return false;
    },
    closeFormIfClickedOutside(e: Event) {
      if (
        e.target != null &&
        (e.target as HTMLElement).id == "form-container"
      ) {
        console.log("close form");
        this.hour_form = undefined;
      }
    },
    clickHour(e: Event, h: Hour, day: WorkerDay) {
      const clicked = e.target;
      if (
        !(
          clicked instanceof Element &&
          clicked.classList.contains("calendar__hour")
        )
      ) {
        return;
      }
      console.log("clicked hour");
      if (!this.hour_form) {
        this.hour_form = {
          hour: h,
          minute: this.getPossibleVisitMinute(h, day),
          worker: day.worker,
        };
      }
    },
    clickHourSlot(e: Event, h: Hour, s: AvailableTimeSlot, day: WorkerDay) {
      const clicked = e.target;
      if (
        !(
          clicked instanceof Element &&
          clicked.classList.contains("available_slot")
        )
      ) {
        return;
      }
      console.log("clicked slot");
      if (!this.hour_form) {
        this.hour_form = {
          hour: h,
          minute: s.from_datetime.minute(),
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
    availableSlots(h: Hour, d: WorkerDay) {
      const out: AvailableTimeSlot[] = [];

      for (const jh of d.job_hours) {
        const from = dayjs(jh.from_datetime);
        const to = dayjs(jh.to_datetime);
        // if both are lower or higher - the hour does not fit in
        if (h.number > from.hour() && h.number > to.hour()) {
          continue;
        }
        if (h.number < from.hour() && h.number < to.hour()) {
          continue;
        }
        // 1) inside hour
        if (h.number == from.hour() && h.number == to.hour()) {
          out.push({ from_datetime: from, to_datetime: to });
        }
        // 2) bigger than hour
        if (h.number > from.hour() && h.number < to.hour()) {
          const hour_start = from.set("hour", h.number).set("minute", 0);
          const hour_end = hour_start.set("hour", h.number + 1);
          out.push({ from_datetime: hour_start, to_datetime: hour_end });
        }
        // 3) starts within hour
        if (h.number == from.hour() && h.number < to.hour()) {
          const hour_end = from.set("hour", h.number + 1).set("minute", 0);
          out.push({ from_datetime: from, to_datetime: hour_end });
        }
        // 4) ends within hour
        if (h.number > from.hour() && h.number == to.hour()) {
          const hour_start = from.set("hour", h.number).set("minute", 0);
          out.push({ from_datetime: hour_start, to_datetime: to });
        }
      }
      return out;
    },
    dayjs(s: string) {
      return dayjs(s);
    },
    getVisitHours(v: OutVisitExtended): number {
      return this.getVisitMinutes(v) / 60;
    },
    getVisitMinutes(v: OutVisitExtended): number {
      const length_minutes =
        dayjs(v.visit.to_datetime).hour() * 60 +
        dayjs(v.visit.to_datetime).minute() -
        (dayjs(v.visit.from_datetime).hour() * 60 +
          dayjs(v.visit.from_datetime).minute());
      return length_minutes;
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
    getPossibleVisitTime(h: Hour, day: WorkerDay) {
      const minutes = this.getPossibleVisitMinute(h, day);
      return (
        String(h.number).padStart(2, "0") +
        ":" +
        String(minutes).padStart(2, "0")
      );
    },
    getPossibleVisitMinute(h: Hour, day: WorkerDay): number {
      let minutes = this.hour_form?.minute || 0;
      for (const visit of day.visit_hours) {
        const start = dayjs(visit.visit.from_datetime);
        const end = dayjs(visit.visit.to_datetime);
        if (start.hour() <= h.number && end.hour() >= h.number) {
          if (start.minute() <= minutes && end.minute() > minutes) {
            minutes = end.minute();
          }
        }
      }
      console.assert(minutes < 60, "Minutes may not go above 60");
      return minutes;
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
