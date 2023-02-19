<template>
  <div>
    <form @submit.prevent="createWorker" class="border_main1">
      <p class="bold"><label for="name">Имя / Название</label></p>
      <input v-model.trim="name" placeholder="Иван / Номер 1 " />
      <p class="bold"><label for="job_title">Должность / Роль</label></p>
      <input
        v-model.trim="job_title"
        placeholder=" Визажист / Машиноместо"
      />
      <div style="margin-top:1em; float: right;">
        <button type="submit">Создать</button>
      </div>
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
