<template>
  <div v-if="services">
    <form>
      <ul>
        {{
          checkedServices
        }}
        <li v-for="service in services" :key="service.service_id">
          <input
            type="checkbox"
            class="checkbox"
            name="service"
            :id="String(service.service_id)"
            :value="service"
            v-model="checkedServices"
          />
          <label class="service_name" :for="String(service.service_id)">{{
            service.name
          }}</label>
          <span class="price">{{ service.price }} {{ service.currency }}</span>
        </li>
      </ul>

      <input
        type="button"
        class="sticky_button"
        @click="emitServices"
        value="Далее"
      />
      <!-- <img src="../assets/arrow.png" /> -->
    </form>
  </div>
</template>

<style scoped src="@/assets/styles/services.css"></style>

<script lang="ts">
import type { OutService } from "@/client/models/OutService";

declare interface ComponentData {
  checkedServices: OutService[];
}

export default {
  components: {},
  data(): ComponentData {
    return {
      checkedServices: [],
    };
  },
  mounted() {
    console.log("Mounted");
    this.checkedServices = this.alreadyCheckedServices;
  },
  computed: {},
  methods: {
    emitServices: function () {
      this.$emit("check-services", this.checkedServices);
      console.log(this.checkedServices);
    },
  },
  props: {
    services: Array<OutService>,
    alreadyCheckedServices: {
      type: Array<OutService>,
      required: true,
    },
  },
};
</script>
