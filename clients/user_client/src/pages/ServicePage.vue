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
      <input
        id="price"
        v-model="service.price"
        type="number"
        step="0.01"
        required
      />
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
      <input v-if="!show_deleteService" type="button" value="Удалить" @click="show_deleteService=!show_deleteService" /> 
      <div v-if="show_deleteService">
        <p class="bold">Вы уверены?</p>
        <input type="button" value="Да, удалить услугу" @click="deleteService" /> 
        <input type="button" value="Нет, не удалять" @click="show_deleteService=!show_deleteService"  /> 
        </div>
    </form>
  </div>
</template>

<script lang="ts">
import { DefaultService, type OutService } from "@/client";

declare interface Data {
  show_deleteService: boolean,
  service?: OutService;
}

export default {
  components: {},

  data(): Data {
    return {
      show_deleteService: false,
      service: undefined,
    };
  },
  methods: {
    async fetchService() {
      this.service = await DefaultService.getService(parseInt(this.service_id));
    },
    async deleteService() {
      if (!this.service) {
        return
      }
      this.service = undefined
      await DefaultService.deleteService(parseInt(this.service_id))
      this.$router.back()
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
