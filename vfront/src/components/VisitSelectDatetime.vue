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

export default {
  components: { Calendar, TimeSched },
  data() {
    return {
      availability_mode: true,
      screen: "calendar",
      selected_date: null,
      timeslots: null,
    };
  },
  props: ["availability"],
  methods: {
    pickDate(x) {
      console.log("Picked date", x);
      const _date = new Date(x);
      this.selected_date = _date;
      const date = this.selected_date.toISOString().split("T")[0];

      this.timeslots = this.availability[date];
      this.screen = "time";
    },
    pickTimeSlot(x) {
      console.log("Picked timeslot", x);
      this.$emit("select-datetime", this.selected_date, x);
    },
  },
};
</script>
