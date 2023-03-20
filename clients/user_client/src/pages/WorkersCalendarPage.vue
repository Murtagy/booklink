<template>
  <div>
    <WorkersCalendar :days="days_selected" />
  </div>
</template>

<style scoped></style>

<script lang="ts">
import { DefaultService, type WorkerDay } from "@/client";
import WorkersCalendar from "@/components/WorkersCalendar.vue";

export default {
  computed: {
    selected_date_str(): string {
      return this.date_selected.toISOString().split("T")[0];
    },
    days_selected(): WorkerDay[] {
      const days: WorkerDay[] = [];
      for (const day of this.days) {
        if (day.date == this.selected_date_str) {
          days.push(day);
        }
      }
      return days;
    },
  },
  components: { WorkersCalendar },
  data() {
    const today = new Date();
    const today_plus_7 = new Date(today.getTime() + 1000 * 60 * 60 * 24 * 7);
    const days: WorkerDay[] = [];
    return {
      days: days,
      date_selected: today,
      date_from: today,
      date_to: today_plus_7,
    };
  },
  methods: {
    async fetchDays() {
      const from = this.date_from.toISOString().split("T")[0];
      const to = this.date_to.toISOString().split("T")[0];
      this.days = await (await DefaultService.workersCalendar(from, to)).days;
    },
  },
  mounted() {
    this.fetchDays();
  },
};
</script>
