// todo - move render and logic in different places, here should be only render
part // todo - copy to components

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
    <div v-if="availability == null && availability_mode">Loading ...</div>
    <div
      v-if="!availability_mode || (availability != null && availability_mode)"
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
          clickable: isClickable(day),
          empty: isNotSelectedMonth(day),
        }"
        class="cell"
        @click="emitDateIfClickable(day)"
        >{{ isNotSelectedMonth(day) ? "" : day.getUTCDate() }}
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

<style scoped src="@/assets/styles/calendar.css"></style>

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
      // 'availability': this.INavailability,
      // 'availability_mode': this.availability_mode,
      calendar_start_date: today,
      calendar_dates: [],
      months_rus: months_rus,
      no_backend: import.meta.env.VITE_APP_OFFLINE, // todo switch to env var
    };
  },
  props: {
    availability: {
      type: Object as PropType<Availability>,
      required: true,
    },
    availability_mode: {
      type: Boolean,
    },
  }, // todo - handle None
  components: {},
  created() {
    //   console.debug('Created Calendar page')
    //   if (this.no_backend) {
    //       this.availability = true
    //   } else {
    //       this.getAvailability()
    this.updateCalendarDates();
  },
  computed: {
    availability_days(): string[] {
      const days = [];
      for (const day of this.availability.days) {
        days.push(day.date);
      }
      return days;
    },
  },
  methods: {
    emitDateIfClickable(day: Date) {
      if (this.isClickable(day)) {
        this.$emit("pick-date", day);
      }
    },
    getDay(target_day: string): Day | null {
      for (const day of this.availability.days) {
        if (day.date == target_day) {
          return day;
        }
      }
      return null;
    },
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
    isClickable(date: Date) {
      // validates date against calendar and availability
      if (this.IsLessThenToday(date)) {
        return false;
      }
      if (this.isNotSelectedMonth(date)) {
        return false;
      }
      if (this.isAvailable(date)) {
        return true;
      }

      return false;
    },
    isAvailable(__date: Date) {
      // for now
      if (!this.availability_mode) {
        console.log("Not in availability mode");
        return true;
      }
      if (this.availability == undefined) {
        // still loading?
        console.log("No availability (undefined)");
        return false;
      }

      // js date to YYYY-MM-DD str
      // ? do I need to care about UTC offset, seems no. https://stackoverflow.com/questions/23593052/format-javascript-date-as-yyyy-mm-dd
      // ^ todo: need to handle date offset
      const _date = new Date(__date);
      const date = _date.toISOString().split("T")[0];

      const date_not_in_availability_days =
        this.availability_days.indexOf(date) == -1;
      if (date_not_in_availability_days) {
        return false;
      }
      const day = this.getDay(date);
      if (!day) {
        return false;
      }
      if (day.timeslots.length == 0) {
        return false;
      }
      return true;
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
    isNotSelectedMonth(date: Date) {
      return date.getUTCMonth() != this.calendar_start_date.getUTCMonth();
    },
  },
};
</script>
