<template>
  <div
    class="border_main1"
    style=""
    @click="
      $router.push({
        name: 'visit.edit',
        params: { visit_id: visit.slot_id },
      })
    "
    >
    <img
      src="@/assets/edit.svg"

      style="float: right"
    />
    <p>
    Время: {{ visit.from_datetime.split("T")[1] }} -
    {{ visit.to_datetime.split("T")[1] }}
    </p>
    <p> Телефон: {{ visit.phone }} </p>
    <p> Юнит: {{ worker.name }} </p>
    <ul>
      <li v-for="service in services" :key="service.service_id" > {{ service.name }} </li>
    </ul>
  </div>
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
