<template>
  <div class="box" style="display: flex; flex-flow: row wrap; width: 100%">
    <VisitsDayCaruselDay
      v-for="day in days"
      :key="day.date"
      :day="day"
      @click="$router.push(`/visits/day/${day.date}`)"
    />
  </div>
</template>

<script lang="ts">
import { DefaultService, type VisitDay } from "@/client";
import VisitsDayCaruselDay from "@/components/VisitsDayCaruselDay.vue";

export default {
  components: { VisitsDayCaruselDay },
  data() {
    const days: VisitDay[] = [];
    return {
      days: days,
    };
  },
  mounted() {
    this.fetchDays();
  },
  methods: {
    async fetchDays() {
      const from = this.date_from.toISOString().split("T")[0];
      const to = this.date_to.toISOString().split("T")[0];
      this.days = await DefaultService.workersCalendar(from, to);
    },
  },
  props: {
    date_from: {
      type: Date,
      required: true,
    },
    date_to: {
      type: Date,
      required: true,
    },
  },
};
</script>
