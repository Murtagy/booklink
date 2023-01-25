<template>
  <div class="box">
    <form id="inputs">
      <p class="bold"><label for="phone">Номер телефона (мобильный): </label></p>
      <input
        id="phone" name="phone"
        placeholder="375-29-1234567"
        v-model="phone"
      /> 
      <label v-show="bad_phone" class="danger" > Телефон РБ с кодом</label>

      <p class="bold"><label for="email">Email</label></p>
      <input
        id="email" name="email"
        placeholder="email@example.com"
        v-model.trim="email"
      /> 

      <p class="bold"><label for="remind_me"> Напомнить о записи? </label></p>
      <input type="checkbox" v-model="remind_me" input-value="1"/>

    </form>
    <!-- <p>{{services}}</p> -->
    <p class="bold">Выбранные услуги:</p>
    <li v-for="service in services" :key="service.service_id">
      <label :for="String(service.service_id)">{{ service.name }}</label>
      <span class="price">{{ service.price }} {{ service.currency }}</span>
    </li>

    <!-- <p>{{visit_time}}</p> -->
    <p class="bold">Время:</p>
    <p class="border_main1" style="padding: 1em">
      {{ parse_date() }}
    </p>
    <!-- <p>{{worker}}</p> -->
    <p class="bold">Запись к:</p>
    <div class="cards">
      <div class="card">
        <p class="border_main1" style="padding: 1em">
          {{ worker.name }}, {{ worker.job_title }}
        </p>
      </div>
    </div>

    <input type="button" value="Подтвердить запись" class="sticky_button" @click="submit_visit"/>
  </div>
</template>

<style scoped>
li {
  display: block;
  margin: 0px;
  margin-top: 1px;
  padding: 5px;
  padding-top: 15px;
  padding-bottom: 15px;
  border: 2px solid var(--color1);
  position: relative;
}
p.bold {
  font-weight: bold;
}

.danger {
  color: rgb(255, 162, 0);
}

#inputs {
  border: 2px solid var(--color1);
  padding: 0.5em;
}
</style>

<script lang="ts">
import { Worker } from "@/models/Worker"
import type { Service } from "@/models/Service"
import {sanitize_phone} from "@/sanitize_phone";
import {validate_phone} from "@/validate_phone";

export default {
  components: {},
  data() {
    return {
      phone: "",
      email: "",
      remind_me: true
    };
  },
  computed: {
    bad_phone(): boolean {
      const phone = sanitize_phone(this.phone);
      return !validate_phone(phone)
    }
  },
  methods: {
    parse_date() {
      if (this.visit_time != null) {
        const date = new Date(this.visit_time);
        const day = `${String(date.getFullYear())}-${String(
          date.getMonth()
        ).padStart(2, "0")}-${String(date.getDay()).padStart(2, "0")}`;
        const time = `${String(date.getHours())}:${String(
          date.getMinutes()
        ).padStart(2, "0")}`;
        return `${day} ${time}`;
      }
      return "-";
    },
    async submit_visit() {
      // todo
    }
  },
  props: {
    worker: {
      type: Worker, required: true
    },
    visit_time: {
      type: String, required: true
    },
    services: {
      type: Array<Service>, required: true
    },
    client_id: {
      type: Number, required: true
    }
  },
};
</script>
