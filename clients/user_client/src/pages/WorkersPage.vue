<template>
  <div>
    <WorkersCardMin
      v-for="worker in workers"
      :worker="worker"
      :key="worker.worker_id"
    >
    </WorkersCardMin>
  </div>
</template>

<style scoped></style>

<script lang="ts">
import { DefaultService, type OutWorker } from "@/client";
import WorkersCardMin from "@/components/WorkersCardMin.vue";

declare interface ComponentData {
  workers: OutWorker[];
}

export default {
  components: { WorkersCardMin },
  data(): ComponentData {
    return {
      workers: [],
    };
  },
  mounted() {
    this.fetchWorkers();
  },
  methods: {
    async fetchWorkers() {
      this.workers = (await DefaultService.getWorkers()).workers;
    },
  },
};
</script>
