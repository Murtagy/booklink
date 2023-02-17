<template>
  <div class="card">
    <div class="border_main1" style="padding: 1em">
      <label :for="String(service.service_id)">{{ service.name }}</label>
      <span class="price"
        >{{ service.price }} {{ service.currency }}</span
      >
    </div>
  </div>
</template>

<script lang="ts">
import type { OutService } from "@/client";
import type { PropType } from "vue";

export default {
  props: {
    service: {
      type: Object as PropType<OutService>,
      required: true,
    },
  },
};
</script>
