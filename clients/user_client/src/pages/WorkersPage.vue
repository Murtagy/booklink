<template>
  <CreateWorker
    v-if="show_createWorker"
    @created-worker="
      show_createWorker = false;
      fetchWorkers();
    "
    @close="show_createWorker = false"
  />
  <input
    type="button"
    v-show="!show_createWorker"
    :value="'Создать юнит'"
    @click="show_createWorker = !show_createWorker"
  />
  <div v-if="user_has_no_workers_created && !show_createWorker">
    <center>
      <h2>У вас нет созданных юнитов</h2>
      <p>Нажмите создать юнит</p>
    </center>
  </div>
  <div v-if="!show_createWorker">
    <WorkersCardMin
      v-for="worker in workers"
      :worker="worker"
      :key="worker.worker_id"
      @click="
        $router.push({
          name: 'worker',
          params: {
            worker_id: worker.worker_id,
            workerCached: JSON.stringify(worker),
          },
        })
      "
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
  loaded_workers: boolean;
  show_createWorker: boolean;
  workers: OutWorker[];
}

export default {
  components: { WorkersCardMin, CreateWorker },
  computed: {
    user_has_no_workers_created(): boolean {
      if (this.loaded_workers && this.workers.length == 0) {
        return true
      }
      return false
    }
  },

  data(): ComponentData {
    return {
      workers: [],
      loaded_workers: false,
      show_createWorker: false,
    };
  },
  mounted() {
    this.fetchWorkers();
  },
  methods: {
    async fetchWorkers() {
      this.workers = (await DefaultService.getWorkers()).workers;
      this.loaded_workers = true
    },
  },
};
</script>
