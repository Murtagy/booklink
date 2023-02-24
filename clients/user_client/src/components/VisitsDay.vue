<template>
  <div class="border_main1" style="" v-if="day">
    {{ day.date }}
    Визитов {{ day.visits_n }}
    <VisitCard
      v-for="visit in day.visits"
      :visit="visit"
      :key="visit.from_datetime"
    />
  </div>
</template>

<script lang="ts">
import { DefaultService, type VisitDay } from "@/client";
import type { PropType } from "vue";
import VisitCard from "@/components/VisitCard.vue";

export default {
  components: { VisitCard },
  data() {
    return {
      day: this._day,
    };
  },
  mounted() {
    this.fetchDay();
  },
  methods: {
    async fetchDay() {
      if (this.day) {
        return;
      }
      const r = await DefaultService.getVisitsDays({
        date_from: this.date,
        date_to: this.date,
      });
      this.day = r.days[0];
    },
  },
  props: {
    _day: {
      type: Object as PropType<VisitDay>,
    },
    date: {
      type: String,
      required: true,
    },
  },
};
</script>
