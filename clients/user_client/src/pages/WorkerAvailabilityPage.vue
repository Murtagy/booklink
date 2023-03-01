<template>
  <div class="box">
    <div v-for="week in days_by_week" style="display: flex; flex-flow: row wrap; width: 100%"> 
      <div v-for="day in week" :key="day.date" class="border_main1" style="width: 10em">
        {{ day.date }}
        <br />
        <div v-for="timeslot in day.timeslots" :key="timeslot.dt_from">
          {{ timeslot.dt_from.slice(11, 16) }} - {{ timeslot.dt_to.slice(11, 16) }}
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>

<script lang="ts">

import { DefaultService, type Day } from "@/client";

export default {
  computed: {
    days_by_week() {
      let i = 0
      const weeks: Day[][] = []
      let week: Day[] = []
      for (const day of this.days) {
        if (i % 7 == 0) {
          weeks.push(week)
          week = []
        }
        week.push(day)
        i += 1
      }
      return weeks
    }
  },
  components: {
    // VisitsDayCaruselDay
  },
  data() {
    const days: Day[] = [];
    const today = new Date();
    const startOfMonth = today.toISOString().split("T")[0].slice(0, 8) + "01";
    return {
      from: startOfMonth,
      days: days,
    };
  },
  mounted() {
    this.fetchDays();
  },
  methods: {
    async fetchDays() {
      this.days = (await DefaultService.getWorkerAvailabilityByUser(this.worker_id, this.from)).days;
    },
  },
  props: {
    worker_id: {
      type: String,
      required: true,
    }
  },
};
</script>
