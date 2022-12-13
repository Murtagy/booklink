<!-- 
https://stackoverflow.com/questions/58187290/vue-binding-with-v-model-in-custom-checkbox-component-doesnt-work 
-->
<template>
  <li>
    <input
      type="checkbox"
      class="checkbox"
      name="service"
      :id="service.service_id"
      :value="service"
      v-model="model"
    />
      <label class="service_name" :for="service.service_id">{{
        service.name
      }}</label>
      <span class="price">{{ service.price }} {{ service.currency }}</span>
  </li>
</template>

<script lang="ts">
import { Service } from "@/models/Service"

export default {
  props: {
    service: Service,  // how to make required?
    value: {
      type: Array
    },
    inputValue: {
      type: Service
    }
  },
  computed: {
    model: {
      get() {
        return this.value
      },
      set(value) {
        this.$emit('input', value)
      }
    },
  },
};
</script>
