<template>
  <div>
    <input type="text" v-model="client_id" id="client_id" required />

    <form @submit="create_service">
      <span>Услуга</span>
      <br /><br />
      <label for="service_name">Наименование услуги</label>
      <input type="text" v-model="service.name" id="service_name" required />
      <br /><br />
      <label for="price">Цена</label>
      <input type="number" v-model="service.price" id="price" required />
      <label for="price">бел.руб.</label>
      <br /><br />
      <label for="duration">Длительность</label>
      <input type="number" v-model="service.seconds" id="duration" required />
      <label for="description">сек.</label>
      <br /><br />
      <label for="description">Описание</label>
      <input type="text" v-model="service.description" id="description" />
      <br /><br />
      <button >Создать</button>
    </form>
    <br /><br /><br />
    <form>
      <span>Сотрудник</span>
      <br /><br />
      <label for="worker_name">Имя сотрудника</label>
      <input type="text" v-model="worker.name" id="worker_name" required />
      <br /><br />
      <label for="job_title">Должность</label>
      <input type="text" v-model="worker.job_title" id="price" required />
      <br /><br />
      <input type="checkbox" v-model="worker.use_company_schedule" id="use_company_schedule" />
      <label for="use_company_schedule">Использовать расписание компании</label>
      <br /><br />
      <button>Создать</button>
    </form>
    <br /><br /><br />
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
export default {
  data() {
    return {
      worker: {
        name: '',
        job_title: '',
        use_company_schedule: false,
      },
      service: {
        name: '',
        price: null,
        price_lower_bound: null,
        price_higher_bound: null,
        seconds: 300,
        description: null,
      },
      client_id: 1,
    };
  },
  methods: {
    async create_service(event: Event) {
      console.log(event)
      event.preventDefault();
      let path = `/my_service`;
      const service = {...this.service, client_id: this.client_id}
      try {
        const response = await this.$api.post(path, service)
      } catch (err) {
        console.log(err)
      }
    }
  },
};
</script>
