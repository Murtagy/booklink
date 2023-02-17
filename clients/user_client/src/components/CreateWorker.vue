<template>
  <div>
    <form @submit.prevent="createWorker">
      <input v-model.trim="name" placeholder="Имя (например: Мария)" />
      <input
        v-model.trim="job_title"
        placeholder="Должность/Роль (например: Визажист)"
      />
      <button type="submit">Создать</button>
    </form>
  </div>
</template>

<style scoped></style>

<script lang="ts">
import { DefaultService, type OutWorker } from "@/client";

export default {
  data() {
    return {
      job_title: "",
      name: "",
      use_company_schedule: false,
    };
  },
  methods: {
    async createWorker() {
      if (!this.name) {
        alert("Поле имя не может быть пустым");
        return;
      }
      if (!this.job_title) {
        alert("Поле должность не может быть пустым");
        return;
      }
      const worker = await DefaultService.createWorker({
        name: this.name,
        job_title: this.job_title,
      });
      this.$emit("createdWorker", { worker: worker });
    },
  },
  emits: {
    createdWorker(payload: { worker: OutWorker }) {
      return true;
    },
  },
};
</script>
