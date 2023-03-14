<template>
  <div v-if="worker">
    <button
      style="margin-top: 1em; margin-bottom: 1em; float: right"
      @click="show_delete = true"
      v-if="!show_delete"
    >
      Удалить
    </button>
    <div v-if="show_delete">
      <p class="bold">Вы уверены?</p>
      <input type="button" :value="deleteYes" @click="deleteWorker" />
      <input
        type="button"
        value="Нет, не удалять"
        @click="show_delete = !show_delete"
      />
    </div>

    <form @submit.prevent="updateWorker" class="border_main1">
      <p class="bold">Название / Имя</p>
      <input v-model="worker.name" />
      <p class="bold">Тип / Роль</p>
      <input v-model="worker.job_title" />
      <button
        style="margin-top: 1em; margin-bottom: 1em; float: right"
        type="submit"
      >
        Сохранить
      </button>
    </form>
    <WorkerSkills v-if="worker" :worker_id="worker_id" />
    <div class="border_main1">
      <router-link
        :to="{ name: 'worker.job_hours', params: { worker_id: worker_id } }"
      >
        Расписание
        <img
          src="/src/assets/calendar-icon.png"
          style="weight: 2em; height: 2em"
        />
      </router-link>
    </div>
  </div>
</template>

<script lang="ts">
import { DefaultService, type OutWorker } from "@/client";
import WorkerSkills from "@/components/WorkerSkills.vue";
import type { PropType } from "vue";

declare interface Data {
  show_delete: boolean;
  worker?: OutWorker;
}

export default {
  components: { WorkerSkills },
  computed: {
    deleteYes(): string {
      if (!this.worker) {
        return "";
      }
      return `Да, удалить ${this.worker.name}`;
    },
  },
  data(): Data {
    return {
      show_delete: false,
      worker: undefined,
    };
  },
  methods: {
    async fetchWorker() {
      if (this.workerCached != undefined && !this.worker) {
        console.log(this.workerCached);
        this.worker = this.workerCached;
      } else {
        console.log(this.workerCached);
        this.worker = await DefaultService.getWorker(this.worker_id);
      }
    },
    async deleteWorker() {
      this.worker = undefined;
      await DefaultService.deleteWorker(this.worker_id);
      this.$router.back();
    },
    async updateWorker() {
      if (!this.worker) {
        return;
      }
      const worker = this.worker;
      this.worker = undefined;
      this.worker = await DefaultService.updateWorker(this.worker_id, {
        name: worker.name,
        job_title: worker?.job_title,
      });
    },
  },
  mounted() {
    this.fetchWorker();
  },
  props: {
    worker_id: {
      type: String,
      required: true,
    },
    workerCached: {
      type: Object as PropType<OutWorker>,
    },
  },
};
</script>
