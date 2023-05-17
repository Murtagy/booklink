<template>
  <div class="border_main1" style="">
    Время {{ visit.from_datetime.split("T")[1] }} -
    {{ visit.to_datetime.split("T")[1] }} Телефон {{ visit.phone }}
    {{ worker.name }}
    <img
      src="@/assets/edit.svg"
      @click="
        $router.push({
          name: 'visit.edit',
          params: { visit_id: visit.slot_id },
        })
      "
      style="float: right"
    />
  </div>
  <div>...</div>
</template>

<script lang="ts">
import type { OutService, OutVisit, OutWorker } from "@/client";
import type { PropType } from "vue";

export default {
  props: {
    visit: {
      type: Object as PropType<OutVisit>,
      required: true,
    },
    worker: {
      type: Object as PropType<OutWorker>,
      required: true,
    },
    services: {
      type: Array<OutService>,
      required: true,
    },
  },
};
</script>
