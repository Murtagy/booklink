<!-- TODO: DRY with Service Page -->

<template>
  <div v-if="service">
    <form @submit.prevent="updateService" class="border_main1">
      <p class="bold"><label for="name">Название</label></p>
      <input
        id="name"
        class="wide"
        v-model.trim="service.name"
        placeholder="Название (например: Мойка)"
        required
      />
      <p class="bold"><label for="minutes">Длительность в минутах</label></p>

      <!-- seconds are multiplied ! -->
      <input
        id="minutes"
        :value="service.seconds / 60"
        @input="(event) => (service.seconds = event.target.value)"
        type="range"
        class="wide"
        min="0"
        max="100"
        step="5"
        required
      />
      <br />
      <input id="minutes" v-model="service.seconds" type="number" required />

      <p class="bold"><label for="price">Стоимость</label></p>
      <input id="price" v-model="service.price" type="number" required />
      <p class="bold">
        <label for="price_to"
          >Верхняя стоимость (если услуга оценивается диапазоном от-до)</label
        >
      </p>
      <input id="price_to" v-model="service.price_to" type="number" />
      (необязательно)
      <button
        style="margin-top: 1em; margin-bottom: 1em; float: right"
        type="submit"
      >
        Сохранить
      </button>
    </form>
  </div>
</template>

<script lang="ts">
import { DefaultService, type OutService } from "@/client";

declare interface Data {
  service?: OutService;
}

export default {
  components: {},

  data(): Data {
    return { 
      service: undefined 
    };
  },
  methods: {
    async fetchService() {
      this.service = await DefaultService.getService(this.service_id);
    },
    async updateService() {
      if (!this.service) {
        return;
      }
      // const worker = this.service;
      // this.service = undefined;
      // this.service = await DefaultService.updateWorker(this.service_id, {name: worker.name, job_title: worker?.job_title})
    },
  },
  mounted() {
    this.fetchService();
  },
  props: {
    service_id: {
      type: Number,
      required: true,
    },
  },
};
</script>
