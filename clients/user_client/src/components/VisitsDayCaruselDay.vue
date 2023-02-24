<template>
    <span class="border_main1">
        День {{ day.date }}.
        Визитов {{ day.visits_n }}
    </span>
</template>

<script lang="ts">
import type { VisitDay } from "@/client";
import type { PropType } from "vue";

export default {
  props: {
    day: {
      type: Object as PropType<VisitDay>,
      required: true,
    },
  },
};
</script>
