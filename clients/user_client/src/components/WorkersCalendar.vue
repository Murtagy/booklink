<template>
  <!-- <div class="box" style="display: flex; flex-flow: row wrap; width: 100%"> -->

    <div class="calendar"> 
    <div class="calendar__hour-grid" v-for="day in days">
      <div
        class="calendar__hour"
        v-for="hour in getHours(day)"
        :style="{ 'background-color': isAvailable(hour, day) ? 'white' : 'lightsteelblue'}"
      >
        <label style="float: left">{{ hour.number }}</label> 
        <!-- {{ hour.events }} -->
        <div
          v-for="visit of getVisits(hour)"
          style="width: 100%; background-color: red; opacity: 0.2; position: absolute; border: 1px solid"
          :style="{ 'height': (height * getVisitHours(visit)) + 'em' }"
        > </div>
    </div>
    </div>
    </div>
  <!-- </div> -->
</template>

<style scoped>
/* https://dev.to/crayoncode/building-a-vertical-calendar-with-html-css-js-2po2 */

.calendar__hour {
  border: 1px groove;
  height: v-bind(height + 'em');
}
</style>

<script lang="ts">
// import VisitsDayCaruselDay from "@/components/VisitsDayCaruselDay.vue";

import type { OutVisitExtended, TimeSlot, WorkerDay } from '@/client';
import dayjs from 'dayjs';
import type { PropType } from 'vue';

declare interface Hour {
  number: number,
  events: (TimeSlot | OutVisitExtended) []
}

export default {
  // components: { VisitsDayCaruselDay },
  computed: {
    workers() {
      // for (let job_hour in days.
    },
  },
  data() {
    return {
      height: 2
    };
  },
  methods: {
    isAvailable(h: Hour, d: WorkerDay) {
      for (const jh of d.job_hours) {
        const from = dayjs(jh.dt_from);
        const to = dayjs(jh.dt_to)
        if ((h.number >= from.hour()) && (h.number <= to.hour() )) {
          return true
        }
      }
      return false
    },
    getVisitHours(v: OutVisitExtended): number {
      const length_hours = (
        dayjs(v.visit.to_datetime).hour() -
        dayjs(v.visit.from_datetime).hour() 
      ) + 1
      return length_hours
    },
    getVisits(h: Hour): OutVisitExtended[] {
      const out: OutVisitExtended[] = []
      for (const event of h.events ) {
        if ((event as OutVisitExtended).visit != undefined) {
          out.push(event as OutVisitExtended)
        }
      }
      return out
    },
    getHours(day: WorkerDay): Hour[] {
      const hours: Hour[] = []
      for (var i = 0; i < 24; i++ ) {
        const events = []
        for (const e of day.job_hours){
          if (dayjs(e.dt_from).hour() == i) {
            events.push(e)
          }
        }
        for (const e of day.visit_hours){
          if (dayjs(e.visit.from_datetime).hour() == i) {
            events.push(e)
          }
        }
        hours.push({number: i, events: events})
      }
      return hours
    }
  },
  props: {
    days: {
      type: Object as PropType<WorkerDay[]>,
    },
  },
};
</script>
