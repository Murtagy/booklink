<template>
  <div>
    <VisitsCarusel 
    v-if="show_carusel"
    :date_from=date_from
    :date_to=date_to
    @day-picked="focusOnDay"
    />

    <VisitsDay :day=day v-if="day"/>
  </div>
</template>

<style scoped></style>

<script lang="ts">
import type { VisitDay } from "@/client";
import VisitsCarusel from "@/components/VisitsCarusel.vue"
import VisitsDay from "@/components/VisitsDay.vue"

declare interface Data {
  day?: VisitDay,
  date_from: Date,
  date_to: Date,
  show_carusel: boolean,
  show_day: boolean,
}

export default {
  components: { VisitsCarusel, VisitsDay},
  data(): Data {
    const today = new Date();
    const today_plus_7 = new Date(today.getTime() + 1000 * 60 * 60 * 24 * 7);
    return {
      day: undefined,
      date_from: today,
      date_to: today_plus_7,
      show_carusel: true,
      show_day: true,
    };
  },
  mounted() {
    // this.fetchServices();
  },
  methods: {
    async fetchVisits() {
      //   this.days = (await DefaultService.getVisitsDays()).days;
    },
    focusOnDay(x: VisitDay) {
      this.show_carusel = false;
      this.show_day = true;
      this.day = x
    }
  },
};
</script>
