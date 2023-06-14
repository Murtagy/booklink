<!-- TODO: DRY with Service Page -->

<template>
  <div v-if="service">

    <div v-if="show_delete">
      <p class="bold">Вы уверены?</p>
      <input type="button" :value="deleteYes" @click="deleteService" />
      <input
        type="button"
        value="Нет, не удалять"
        @click="show_delete = !show_delete"
      />
    </div>
    <form @submit.prevent="updateService" class="border_main1" style="overflow: auto">
      <button
        v-if="!show_delete"
        @click="show_delete = !show_delete"
        style="margin-top: 1em; margin-bottom: 1em; float: right"
      >
        Удалить
      </button>
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
        v-model="service.minutes"
        type="range"
        class="wide"
        min="0"
        max="100"
        step="5"
        required
      />
      <br />
      <input id="minutes" v-model="service.minutes" type="number" required />

      <p class="bold"><label for="price">Стоимость</label></p>
      <input id="price" v-model="service.price" type="number" step="0.01" />
      <p class="bold">
        <label for="price_to"
          >Верхняя стоимость (если услуга оценивается диапазоном от-до)</label
        >
      </p>
      <input id="price_to" v-model="service.price_to" type="number" />
      (необязательно)
      <button class="save" type="submit">Сохранить</button>
    </form>
  </div>
</template>

<script lang="ts">
import { DefaultService, type OutService } from "@/client";

declare interface Data {
  show_delete: boolean;
  service?: OutService;
}

export default {
  components: {},
  computed: {
    deleteYes(): string {
      if (!this.service) {
        return "";
      }
      return `Да, удалить ${this.service.name}`;
    },
  },
  data(): Data {
    return {
      show_delete: false,
      service: undefined,
    };
  },
  methods: {
    async fetchService() {
      this.service = await DefaultService.getService(parseInt(this.service_id));
    },
    async deleteService() {
      if (!this.service) {
        return;
      }
      this.service = undefined;
      await DefaultService.deleteService(parseInt(this.service_id));
      this.$router.back();
    },
    async updateService() {
      if (!this.service) {
        return;
      }
      const service = this.service;
      this.service = undefined;
      this.service = await DefaultService.updateService(
        parseInt(this.service_id),
        service
      );
    },
  },
  mounted() {
    this.fetchService();
  },
  props: {
    service_id: {
      type: String,
      required: true,
    },
  },
};
</script>
