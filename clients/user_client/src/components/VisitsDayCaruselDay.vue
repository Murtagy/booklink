<template>
  <div class="border_main1" style="">
    {{ day.date }}
    <br />
    Визитов {{ day.visits_n }}
  </div>
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
