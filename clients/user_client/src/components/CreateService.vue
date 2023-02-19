<template>
  <div>
    <form @submit.prevent="createService" class="border_main1">
      <p class="bold"><label for="name">Название</label></p>
      <input
        id="name" 
        v-model.trim="name"
        placeholder="Название (например: Мойка)" 
        required
      />
      <p class="bold"><label for="minutes">Длительность в минутах</label></p>
      <input
        id="minutes"
        v-model="minutes"
        type="number"
        placeholder="Длительность в минутах"
        required
      />
      <p class="bold"><label for="price">Стоимость</label></p>
      <input
        id="price"
        v-model="price"
        type="number"
        placeholder="Стоимость ( например 35,5 )"
        required
      />
      <p class="bold"><label for="price_to">Верхняя стоимость (если услуга оценивается диапазоном от-до)</label></p>
      <input
        id="price_to"
        v-model="price_to"
        type="number"
        placeholder="(например 50)"
      />
      <div style="margin-top:1em; float: right;">
        <button type="submit">Создать</button>
      </div>
    </form>
  </div>
</template>

<style scoped>
</style>

<script lang="ts">
import { DefaultService, type OutService } from "@/client";

declare interface ComponentData {
  name: string;
  price: number;
  minutes: number;
  price_to?: number | undefined;
  description?: string;
}

export default {
  data(): ComponentData {
    return {
      name: "",
      minutes: 30,
      price: 0.0,
      price_to: undefined,
    };
  },
  methods: {
    async createService() {
      if (!this.name) {
        alert("Поле название не может быть пустым");
        return;
      }
      if (!this.minutes) {
        alert("Поле длительность не может быть пустым");
        return;
      }
      const service = await DefaultService.createService({
        name: this.name,
        price: this.price,
        price_to: this.price_to,
        seconds: this.minutes * 60,
      });
      this.$emit("createdService", { service: service });
    },
  },
  emits: {
    createdService(payload: { service: OutService }) {
      return true;
    },
  },
};
</script>
