<template>
  <div class="border_main1" style="">
    Время {{ visit.from_datetime.split("T")[1] }} -
    {{ visit.to_datetime.split("T")[1] }} Телефон {{ visit.phone }}
    Имя TODO
  </div>
  <div>...</div>
</template>

<script lang="ts">
import type { OutVisit } from "@/client";
import type { PropType } from "vue";

export default {
  props: {
    visit: {
      type: Object as PropType<OutVisit>,
      required: true,
    },
  },
};
</script>
