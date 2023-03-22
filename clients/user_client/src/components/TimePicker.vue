<!-- TODO: in small res time is out of colored button -->
<template>
  <!-- TODO: remove hard code and make arrows work (moveToPrevMonth/moveToNextMonth does not exist)-->
  <div>
    <button class="left">
      <img class="left" src="../assets/arrow2.png" />
    </button>
    <div class="chosen_date">22 сентября 2022</div>
    <button class="right">
      <img class="right" src="../assets/arrow2.png" />
    </button>
    <!-- {{ getRowsHours() }} -->
    <!-- {{ filterRowTimeslots(13) }}  -->
    <table>
      <tr v-for="row in getRowsHours()" :key="row">
        <th>{{ row }}</th>
        <td
          v-for="timeslot in filterRowTimeslots(row)"
          :key="timeslot.from_datetime"
          @click="emitTimeSlot(timeslot)"
        >
          <button>{{ formatTimeSlot(timeslot) }}</button>
        </td>
      </tr>
      <!-- <tr><th>8:00</th><td><button>8:10</button></td><td><button>8:40</button></td></tr>
        <tr><th>9:00</th><td><button>9:15</button></td></tr>
        <tr><th>10:00</th><td><button>10:10</button></td><td><button>10:30</button></td><td><button>10:50</button></td></tr>
        <tr><th>11:00</th></tr>
        <tr><th>12:00</th><td><button>12:15</button></td></tr>
        <tr><th>13:00</th></tr>
        <tr><th>14:00</th><td><button>14:05</button></td><td><button>14:30</button></td><td><button>14:55</button></td></tr>
        <tr><th>15:00</th><td><button>15:10</button></td><td><button>15:50</button></td></tr>
        <tr><th>16:00</th><td><button>16:30</button></td></tr>
        <tr><th>17:00</th><td><button>17:20</button></td><td><button>17:50</button></td></tr>
        <tr><th>18:00</th></tr>
        <tr><th>19:00</th><td><button>19:15</button></td></tr>
        <tr><th>20:00</th><td><button>20:20</button></td><td><button>20:50</button></td></tr> -->
    </table>
  </div>
</template>

<script lang="ts">
import type { TimeSlot } from "@/client";

export default {
  components: {},
  data() {
    return {};
  },
  methods: {
    formatTimeSlot(ts: TimeSlot) {
      const x = new Date(ts.from_datetime);
      // hour + padded with leading zero minute
      return x.getHours() + ":" + ("0" + x.getMinutes()).slice(-2);
    },
    getRowsHours() {
      const hours = this.timeslots.map((ts) => {
        const x = new Date(ts.from_datetime);
        return x.getHours();
      });
      const _hours_no_duplicated = new Set(hours);
      return Array.from(_hours_no_duplicated);
    },
    filterRowTimeslots(target_hour: number): TimeSlot[] {
      const filtered: TimeSlot[] = [];
      for (const timeslot of this.timeslots) {
        const dt_from = timeslot.from_datetime;
        const dt_from_date = new Date(dt_from);
        if (dt_from_date.getHours() != target_hour) {
          continue;
        }
        filtered.push(timeslot);
      }
      return filtered;
    },
    emitTimeSlot(timeslot: TimeSlot) {
      console.log("Emit ts", timeslot);
      this.$emit("pick-timeslot", timeslot);
    },
  },
  props: {
    date: {
      type: String,
      required: true,
    },
    timeslots: {
      type: Array<TimeSlot>,
      required: true,
    },
  },
};
</script>

<style scoped src="@/assets/styles/time.css"></style>
