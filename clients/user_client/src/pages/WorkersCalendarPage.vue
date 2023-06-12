<template>
  <center>
    <div class="chosen_date">
      <button @click="dateLeft">
        <img class="left px15" src="../assets/arrow2.png" />
      </button>
      {{ selected_date_str }}
      <button @click="dateRight">
        <img class="right px15" src="../assets/arrow2.png" />
      </button>
    </div>
  </center>

  <div>
    <WorkersCalendar :days="days_selected" />
  </div>
</template>

<style scoped>
img.left {
  transform: rotate(90deg);
}

img.right {
  transform: rotate(270deg);
}

img.px15 {
  height: 15px;
  width: 15px;
}
</style>

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
    const today_plus_14 = new Date(today.getTime() + 1000 * 60 * 60 * 24 * 14);
    const days: WorkerDay[] = [];
    return {
      days: days,
      date_selected: today,
      date_from: today,
      date_to: today_plus_14,
    };
  },
  methods: {
    async fetchDays() {
      const from = this.date_from.toISOString().split("T")[0];
      const to = this.date_to.toISOString().split("T")[0];
      this.days = await (await DefaultService.workersCalendar(from, to)).days;
    },
    dateLeft() {
      this.date_selected = new Date(
        this.date_selected.getTime() - 1000 * 60 * 60 * 24
      );
    },
    dateRight() {
      this.date_selected = new Date(
        this.date_selected.getTime() + 1000 * 60 * 60 * 24
      );
    },
  },
  mounted() {
    this.fetchDays();
  },
  watch: {
    date_selected() {
      // after 14 days we increase a windows by 7 days
      // @optimisation - not refetch already fetched
      if (this.date_selected < this.date_from) {
        this.date_from = new Date(
          this.date_from.getTime() - 1000 * 60 * 60 * 24 * 7
        );
      }
      if (this.date_selected > this.date_to) {
        this.date_to = new Date(
          this.date_to.getTime() + 1000 * 60 * 60 * 24 * 7
        );
      }
    },
    date_to() {
      this.fetchDays();
    },
    date_from() {
      this.fetchDays();
    },
  },
};
</script>
