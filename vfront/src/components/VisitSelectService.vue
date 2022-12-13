<template>
  <div v-if="services">
    <form>
      <ul>
        {{
          checkedServices
        }}
        <PickServiceInput 
          v-for="service in services.services"
          v-model="checkedServices"
          :key="service.service_id"
          :service="service"
        />
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
import { Services } from "@/models/Services"
import PickServiceInput from "@/components/PickServiceInput.vue"

export default {
  components: {PickServiceInput},
  data() {
    return {
      checkedServices: [],
    };
    // TODO get services in online mode
  },
  methods: {
    emitServices: function () {
      this.$emit("check-services", this.checkedServices);
      console.log(this.checkedServices);
    },
  },
  props: {
    "services": Services,
  },
};
</script>
