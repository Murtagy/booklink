<template>

  <div v-if="worker">
    <form @submit.prevent="updateWorker" class="border_main1">
      <p class="bold"> Имя / Название </p>
      <input v-model="worker.name">
      <p class="bold"> Должность / Роль </p>
        <input v-model="worker.job_title">
      <button style="margin-top: 1em; margin-bottom: 1em; float: right" type="submit"> Сохранить </button>
    </form>
  </div>

</template>

<script lang="ts">

import { DefaultService, type OutWorker } from '@/client';


declare interface Data {
  worker?: OutWorker
}

export default {
  components: {},
  data(): Data {
    return {worker: undefined}
  },
  methods: {
    async fetchWorker() {
      this.worker = (await DefaultService.getWorker(this.worker_id));
    },
    async updateWorker() {
      if (!this.worker) { 
        return
      }
      const worker = this.worker;
      this.worker = undefined;
      this.worker = await DefaultService.updateWorker(this.worker_id, {name: worker.name, job_title: worker?.job_title})
    },
  },
  mounted() {
    this.fetchWorker();
  },
  props: {
    worker_id: {
      type: String,
      required: true
    },
  },
};
</script>
