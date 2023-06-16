<template>
  <div>
    <header style="display: flex">
        <button class="left" @click="moveToPrevMonth">
            <img class="left" src="../assets/arrow2.png" />
        </button>
        <span class="month">
            {{ months_rus[calendar_start_date.getMonth()] }}
            {{ calendar_start_date.getFullYear() }}
        </span>
        <button class="right" @click="moveToNextMonth">
            <img class="right" src="../assets/arrow2.png" />
        </button>
    </header>
    <div
      class="calendar"
    >
      <span class="weekday">Пн</span>
      <span class="weekday">Вт</span>
      <span class="weekday">Ср</span>
      <span class="weekday">Чт</span>
      <span class="weekday">Пт</span>
      <span class="weekday">Сб</span>
      <span class="weekday">Вс</span>
      <span
        v-for="day in calendar_dates"
        :key="day.getTime()"
        v-bind:class="{
            clickable: !IsLessThenToday(day)
        }"
        class="cell"
        @click="$emit('dateClick', day)"
        >
            {{ day.getUTCDate() }}
      </span>
    </div>
    <br />
    <div class="explication">
      <!-- clickable cell - class="clickable" -->
      <span class="square clickable"></span>
      <span class="description">- дата доступна для выбора</span>
      <br /><br />
      <!-- nonclickacle - usual cell  -->
      <span class="square dates"></span>
      <span class="description">- дата не доступна для выбора</span>
      <!-- class="empty" for empty cells -->
    </div>
  </div>
</template>

<style scoped 
    src="@/assets/styles/calendar.css"
>

</style>

<script lang="ts">
import type { Availability } from "@/client/models/Availability";
import type { Day } from "@/client/models/Day";
import type { PropType } from "vue";

const months_rus = {
  0: "Январь",
  1: "Февраль",
  2: "Март",
  3: "Апрель",
  4: "Май",
  5: "Июнь",
  6: "Июль",
  7: "Август",
  8: "Сентябрь",
  9: "Октябрь",
  10: "Ноябрь",
  11: "Декабрь",
};

declare interface ComponentData {
  calendar_dates: Date[];
  calendar_start_date: Date;
  months_rus: Record<number, string>;
  no_backend: boolean;
}

export default {
  data(): ComponentData {
    const today = new Date();
    return {
      calendar_start_date: today,
      calendar_dates: [],
      months_rus: months_rus,
      no_backend: import.meta.env.VITE_APP_OFFLINE, // todo switch to env var
    };
  },
  props: {
  },
  components: {},
  created() {
    this.updateCalendarDates();
  },
  computed: {
  },
  emits: {
      dateClick: (date: Date) => true
  },
  methods: {
    findCalendarBase(_date: Date) {
      // finds a cell to begin calendar with (Monday which is 1st in current month or prior to that)
      let date = new Date(_date);

      date.setUTCDate(1);
      // console.debug("Here", date);
      for (;;) {
        if (date.getUTCDay() == 1) {
          break;
        }
        date = new Date(date.getTime() - 1000 * 60 * 60 * 24); // (miliseconds * seconds)... 24h
      }
      // console.log("Base date", date);
      return date;
    },
    listCalendarDatesFromBase(_date: Date): Date[] {
      // returns 5 weeks of days
      let date = new Date(_date);

      const dates = [];
      for (let i = 0; i < 35; i++) {
        date = new Date(date.getTime() + 1000 * 60 * 60 * 24); // 24h
        dates.push(date);
      }
      // console.log("Calendar dates", dates);
      return dates;
    },
    updateCalendarDates() {
      console.log("Rendering from", this.calendar_start_date);
      const base = this.findCalendarBase(this.calendar_start_date);
      const calendar_dates = this.listCalendarDatesFromBase(base);
      this.calendar_dates = calendar_dates;
    },
    IsLessThenToday(date: Date) {
      // @bug
      // here might be a bug in comparison, e.g. date with current timestamp compared with almost the same date
      // triggered when updating the page fast enough
      const today = new Date();
      return date < today;
    },
    moveToNextMonth() {
      const date = this.calendar_start_date;
      const month = date.getUTCMonth();
      this.calendar_start_date.setUTCMonth(month + 1);

      this.updateCalendarDates();
    },
    moveToPrevMonth() {
      console.log("MOVIT");
      const date = this.calendar_start_date;
      const month = date.getUTCMonth();
      this.calendar_start_date.setUTCMonth(month - 1);
      console.log(this.calendar_start_date);

      this.updateCalendarDates();
    },

  },
};
</script>
