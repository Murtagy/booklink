<template>
  <h2>
    Ближайшие визиты 

      <i
        class="fa-solid fa-add"
        style="float: right; overflow: auto"
        @click="showCalendar = !showCalendar"
      > 
      </i>

  </h2>
  <div>
    <VisitsCarusel :date_from="date_from" :date_to="date_to" />
  </div>
  <div
    v-if="showCalendar"
    id="form-container"
    tabindex="0"
    @keydown.esc="showCalendar = !showCalendar"
    @click="closeFormIfClickedOutside($event)"
  >
    <!-- @click="closeFormIfClickedOutside($event)" -->
    <div id="form-content">
      <BaseCalendar @dateClick="CalendarDateClicked" />
    </div>
  </div>
</template>

<style scoped></style>

<script lang="ts">
import VisitsCarusel from "@/components/VisitsCarusel.vue";
import BaseCalendar from "@/components/BaseCalendar.vue";
import dayjs from "dayjs";

declare interface Data {
  date_from: Date;
  date_to: Date;
  showCalendar: boolean;
}

export default {
  components: { VisitsCarusel, BaseCalendar },
  data(): Data {
    const today = new Date();
    const today_plus_7 = new Date(today.getTime() + 1000 * 60 * 60 * 24 * 7);
    return {
      date_from: today,
      date_to: today_plus_7,
      showCalendar: false,
    };
  },
  methods: {
    CalendarDateClicked(date: Date) {
      const date_clicked = dayjs(date);
      this.$router.push(`/visit/create/${date_clicked}`);
    },
    closeFormIfClickedOutside(e: Event) {
      if (
        e.target != null &&
        (e.target as HTMLElement).id == "form-container"
      ) {
        console.log("close form");
        this.showCalendar = false;
      }
    },
}};
</script>
