<template>
  <div class="card">
    <div class="border_main1" style="padding: 1em">
      <label :for="String(service.service_id)">{{ service.name }}</label>
      <span> , </span>
      <span v-if="service.price != null" class="price">
        {{ service.price }} 
        <span v-if="service.price_to != null"> - {{ service.price_to }} </span>
        {{ service.currency }}
      </span>
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
