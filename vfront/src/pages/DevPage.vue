<template>
  <div>
    <h3>ID клиента, сотрудника</h3>
    <input type="text" v-model="client_id" id="client_id" required />
    <input type="text" v-model="worker_id" id="worker_id" required />
    <hr />

    <form @submit="create_service">
      <h3>Создать сервис</h3>
      <span>Услуга</span>
      <br /><br />
      <label for="service_name">Наименование услуги</label>
      <input
        type="text"
        v-model="created_service.name"
        id="service_name"
        required
      />
      <br /><br />
      <label for="price">Цена</label>
      <input type="number" v-model="created_service.price" id="price" />
      <label for="price">бел.руб.</label>
      <br /><br />
      <label for="price_lower_bound">Цена от</label>
      <input
        type="number"
        v-model="created_service.price_lower_bound"
        id="price_lower_bound"
      />
      <label for="price_lower_bound">бел.руб.</label>
      <br /><br />
      <label for="price_higher_bound">Цена до</label>
      <input
        type="number"
        v-model="created_service.price_higher_bound"
        id="price_higher_bound"
      />
      <label for="price_higher_bound">бел.руб.</label>
      <br /><br />
      <label for="duration">Длительность</label>
      <input
        type="number"
        v-model="created_service.seconds"
        id="duration"
        required
      />
      <label for="description">сек.</label>
      <br /><br />
      <label for="description">Описание</label>
      <input
        type="text"
        v-model="created_service.description"
        id="description"
      />
      <br /><br />
      <button>Создать</button>
    </form>
    <hr />
    <form @submit="create_worker">
      <h3>Создать сотрудника</h3>
      <span>Сотрудник</span>
      <br /><br />
      <label for="worker_name">Имя сотрудника</label>
      <input type="text" v-model="worker.name" id="worker_name" required />
      <br /><br />
      <label for="job_title">Должность</label>
      <input type="text" v-model="worker.job_title" id="price" required />
      <br /><br />
      <!-- <input
        type="checkbox"
        v-model="worker.use_company_schedule"
        id="use_company_schedule"
      />
      <label for="use_company_schedule">Использовать расписание компании</label>
      <br /><br /> -->
      <button>Создать</button>
    </form>
    <hr />
    <h3>Добавить сервис сотруднику</h3>
    <button @click="get_worker_services()">Обновить</button>
    <li v-for="service in services.services" :key="service.service_id">
      <!-- {{service}} -->
      <input type="checkbox" value="{{service.service_id}}" />
      <label :for="String(service.service_id)">{{ service.name }}</label>
    </li>
    <hr />
    <h3>Создать визит</h3>
    <form>
      <span>Визит</span>
      <br /><br />
      <label for="from">С:</label>
      <input type="text" v-model="visit" id="from" required />
      <input type="text" v-model="visit" id="from" required />
      <br /><br />
      <label for="to">До:</label>
      <input type="text" v-model="visit" id="to" required />
      <input type="text" v-model="visit" id="to" required />
      <br /><br />
      <label for="phone">Номер телефона</label>
      <input type="text" v-model="visit" id="phone" required />
      <br /><br />
      <label for="e-mail">E-mail</label>
      <input type="email" v-model="visit" id="e-mail" required />
      <br /><br />
      <label for="client">Клиент</label>
      <input type="text" v-model="visit" id="client" required />
      <br /><br />
      <label for="worker">Сотрудник</label>
      <input type="text" v-model="visit" id="worker" required />
      <br /><br />
      <input type="checkbox" v-model="visit" id="reminder" />
      <label for="reminder">Напоминание</label>
      <br /><br />
      <button>Создать</button>
    </form>
  </div>
</template>

<script lang="ts">
import { CreateWorker } from "@/models/CreateWorker";
import { Services } from "@/models/Services";
import { CreateService } from "@/models/CreateService";
import type { AxiosError, AxiosResponse } from "axios";

export default {
  data() {
    return {
      services: new Services([]),
      worker: new CreateWorker(
        "", // name
        "" // title
      ),
      created_service: new CreateService(
        "", // name
        0, // seconds
        undefined, // price
        undefined,
        undefined,
        undefined
      ),
      client_id: 1,
      worker_id: 1,
      // visit: {
        // client_id: 1,
        // from_
      // }
    };
  },
  methods: {
    async create_service(event: Event) {
      console.log(event);
      event.preventDefault();
      let path = `/my_service`;
      const service = { ...this.created_service, client_id: this.client_id };
      try {
        const response = await this.$api.post(path, service);
      } catch (err) {
        console.log(err);
      }
    },
    async get_worker_services() {
      let path = `/client/${this.client_id}/picker/services?worker_id=${this.worker_id}`;
      try {
        const response: AxiosResponse<Services> = await this.$api.get(path);
        this.services = new Services(response.data.services);
      } catch (err) {
        console.log(err);
      }
    },
  },
};
</script>
