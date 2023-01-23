<template>
  <div>
    <calendar
      v-if="screen == 'calendar'"
      v-bind:availability="availability"
      v-bind:availability_mode="availability_mode"
      @pick-date="pickDate"
    />
    <TimeSched
      v-if="screen == 'time'"
      v-bind:date="selected_date"
      v-bind:timeslots="timeslots"
      @pick-timeslot="pickTimeSlot"
    />
  </div>
</template>

<style scoped src="@/assets/styles/visit.css"></style>

<script lang="ts">
import Calendar from "@/components/CalendarPicker.vue";
import TimeSched from "@/components/TimePicker.vue";

import type { PropType } from 'vue'


declare interface ComponentData {
  availability_mode: boolean,
  screen: string,
  selected_date: Date | null,
  timeslots: Record<string, boolean> | null
}

export default {
  components: { Calendar, TimeSched },
  data(): ComponentData {
    return {
      availability_mode: true,
      screen: "calendar",
      selected_date: null,
      timeslots: null,
    };
  },
  props: {
    availability: {
      type: Object as PropType<Record<string, Record<string, boolean>>>,
      required: true,
    },  // temporary -  see if composition api would work https://vuejs.org/guide/extras/composition-api-faq.html#can-i-use-both-apis-together
  },
  methods: {
    pickDate(x: Date) {
      console.log("Picked date", x);
      const _date = new Date(x);
      this.selected_date = _date;
      const date = this.selected_date.toISOString().split("T")[0];

      this.timeslots = this.availability[date];
      this.screen = "time";
    },
    pickTimeSlot(x: Date) {
      console.log("Picked timeslot", x);
      this.$emit("select-datetime", this.selected_date, x);
    },
  },
};
</script>
