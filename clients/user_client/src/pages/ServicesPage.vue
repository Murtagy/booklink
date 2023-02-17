<template>
  <CreateService
    v-if="show_createService"
    @created-service="
      show_createService = false;
      fetchServices();
    "
  />
  <input
    type="button"
    value="Создать услугу"
    @click="show_createService = true"
  />
  <div>
    <ServiceCardMin
      v-for="service in services"
      :service="service"
      :key="service.service_id"
    />
  </div>
</template>

<style scoped></style>

<script lang="ts">
import { DefaultService, type OutService } from "@/client";
import ServiceCardMin from "@/components/ServiceCardMin.vue";
import CreateService from "@/components/CreateServiceTODO.vue";

declare interface ComponentData {
  services: OutService[];
  show_createService: boolean;
}

export default {
  components: { ServiceCardMin, CreateService },
  data(): ComponentData {
    return {
      services: [],
      show_createService: false,
    };
  },
  mounted() {
    this.fetchServices();
  },
  methods: {
    async fetchServices() {
      this.services = (await DefaultService.getServicesByUser()).services;
    },
  },
};
</script>
