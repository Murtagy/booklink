<template>
  <CreateWorker
    v-if="show_createWorker"
    @created-worker="
      show_createWorker = false;
      fetchWorkers();
    "
  />
  <input
    type="button"
    :value="show_createWorker ? 'Закрыть' : 'Создать сотрудника'"
    @click="show_createWorker = !show_createWorker"
  />
  <div>
    <WorkersCardMin
      v-for="worker in workers"
      :worker="worker"
      :key="worker.worker_id"
      @click="$router.push({
        name: 'worker',
        params: {
          worker_id: worker.worker_id,
          workerCached: JSON.stringify(worker)
        }
      })"
    >
    </WorkersCardMin>
  </div>
</template>

<style scoped></style>

<script lang="ts">
import { DefaultService, type OutWorker } from "@/client";
import WorkersCardMin from "@/components/WorkersCardMin.vue";
import CreateWorker from "@/components/CreateWorker.vue";

declare interface ComponentData {
  workers: OutWorker[];
  show_createWorker: boolean;
}

export default {
  components: { WorkersCardMin, CreateWorker },
  data(): ComponentData {
    return {
      workers: [],
      show_createWorker: false,
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
