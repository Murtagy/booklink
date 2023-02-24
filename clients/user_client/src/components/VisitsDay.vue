<template>
    <div class="border_main1" style="">
        {{ day.date }}
        Визитов {{ day.visits_n }}
        <VisitCard v-for="visit in day.visits" :visit="visit" :key="visit.from_datetime"/>

    </div>
</template>

<script lang="ts">
import type { VisitDay } from "@/client";
import type { PropType } from "vue";
import VisitCard from "@/components/VisitCard.vue"


export default {
  components: { VisitCard },
  computed: {
    date() {
      return this.$route.params.date
    },
  },
  props: {
    day: {
      type: Object as PropType<VisitDay>,
      required: true,
    },
  },
};
</script>
