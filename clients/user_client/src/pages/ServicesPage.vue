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
    v-if="!show_createService"
    @click="show_createService = true"
  />
  <div v-if="user_has_no_services_created && loaded_services && !show_createService">
    <center>
      <h2>У вас нет созданных услуг</h2>
      <p>Нажмите создать услугу</p>
    </center>
  </div>
  <div>
    <ServiceCardMin
      v-for="service in services"
      :service="service"
      :key="service.service_id"
      @click="$router.push(`/service/${service.service_id}`)"
    />
  </div>
</template>

<style scoped></style>

<script lang="ts">
import { DefaultService, type OutService } from "@/client";
import ServiceCardMin from "@/components/ServiceCardMin.vue";
import CreateService from "@/components/CreateService.vue";

declare interface ComponentData {
  loaded_services: boolean;
  services: OutService[];
  show_createService: boolean;
}

export default {
  components: { ServiceCardMin, CreateService },
  computed: {
    user_has_no_services_created(): boolean {
      if (this.loaded_services && this.services.length == 0) {
        return true;
      }
      return false;
    }
  },
  data(): ComponentData {
    return {
      services: [],
      loaded_services: false,
      show_createService: false,
    };
  },
  mounted() {
    this.fetchServices();
  },
  methods: {
    async fetchServices() {
      this.services = (await DefaultService.getServicesByUser()).services;
      this.loaded_services = true
    },
  },
};
</script>
