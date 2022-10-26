<template>
  <div>
    <button class="left" @click="moveToPrevMonth">
      <img class="left" src="../assets/arrow2.png" />
    </button>
    <!-- TODO: remove hard code and make arrows work -->
    <div class="chosen_date">22 сентября 2022</div>
    <button class="right" @click="moveToNextMonth">
      <img class="right" src="../assets/arrow2.png" />
    </button>
    <!-- {{ getRowsHours() }} -->
    <!-- {{ filterRowTimeslots(13) }}  -->
    <table>
      <tr v-for="row in getRowsHours()" :key="row">
        <th>{{ row }}</th>
        <td
          v-for="time in filterRowTimeslots(row)"
          :key="time"
          @click="emitTimeSlot(time)"
        >
          <button>{{ formatTimeSlot(time) }}</button>
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
    <button class="choose">Выбрать</button>
  </div>
</template>

<script>
export default {
  components: {},
  data() {
    return {};
  },
  methods: {
    formatTimeSlot(x) {
      // hour + padded with leading zero minute
      return x.getHours() + ":" + ("0" + x.getMinutes()).slice(-2);
    },
    getRowsHours() {
      const ts = Object.keys(this.timeslots);
      const hours = ts.map((_ts) => {
        const x = new Date(_ts);
        return x.getHours();
      });
      const _hours_no_duplicated = new Set(hours);
      return Array.from(_hours_no_duplicated);
    },
    filterRowTimeslots(hour) {
      const ts = Object.keys(this.timeslots);
      const hours = ts.map((_ts) => new Date(_ts));
      return hours.filter((_ts) => _ts.getHours() == hour);
    },
    emitTimeSlot(timeslot) {
      console.log("Emit ts", timeslot);
      this.$emit("pick-timeslot", timeslot);
    },
  },
  props: ["date", "timeslots"],
};
</script>

<style scoped src="@/assets/styles/time.css"></style>
