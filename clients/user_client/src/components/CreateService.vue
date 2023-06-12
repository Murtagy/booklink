<!-- TODO: DRY with Service Page -->
<template>
  <div>
    <form
      @submit.prevent="createService"
      class="border_main1"
      style="display: flow-root"
    >
      <p class="bold"><label for="name">Название</label></p>
      <input
        id="name"
        class="wide"
        v-model.trim="name"
        placeholder="Название (например: Мойка)"
        required
      />
      <p class="bold"><label for="minutes">Длительность в минутах</label></p>
      <input
        id="minutes"
        v-model="minutes"
        type="range"
        class="wide"
        min="0"
        max="100"
        step="5"
        required
      />
      <br />
      <input id="minutes" v-model="minutes" type="number" required />
      <p class="bold"><label for="price">Стоимость</label></p>
      <input id="price" v-model="price" type="number" step="0.01"/>
      <p class="bold">
        <label for="price_to"
          >Верхняя стоимость (если услуга оценивается диапазоном от-до)</label
        >
      </p>
      <input id="price_to" v-model="price_to" type="number" />
      (необязательно)
      <button class="save" type="submit">Создать</button>
    </form>
  </div>
</template>

<style scoped>
input {
  width: 5em;
}
input.wide {
  width: fit-content;
  min-width: 30%;
}
</style>

<script lang="ts">
import { DefaultService, type OutService } from "@/client";

declare interface ComponentData {
  name: string;
  minutes: number;
  price?: number;
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
        minutes: this.minutes,
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
