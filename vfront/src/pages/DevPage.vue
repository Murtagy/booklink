<template>
  <div>
    <form>
      <span>Услуга</span>
      <br /><br />
      <label for="service_name">Наименование услуги</label>
      <input type="text" v-model="company" id="service_name" required />
      <br /><br />
      <label for="price">Цена</label>
      <input type="text" v-model="company" id="price" required />
      <label for="price">бел.руб.</label>
      <br /><br />
      <label for="duration">Длительность</label>
      <input type="text" v-model="company" id="duration" required />
      <label for="description">сек.</label>
      <br /><br />
      <label for="description">Описание</label>
      <input type="text" v-model="company" id="description" />
      <br /><br />
      <button>Создать</button>
    </form>
    <br /><br /><br />
    <form>
      <span>Сотрудник</span>
      <br /><br />
      <label for="worker_name">Имя сотрудника</label>
      <input type="text" v-model="company" id="worker_name" required />
      <br /><br />
      <label for="job_title">Должность</label>
      <input type="text" v-model="company" id="price" required />
      <br /><br />
      <input type="checkbox" v-model="company" id="use_company_schedule" />
      <label for="use_company_schedule">Использовать расписание компании</label>
      <br /><br />
      <button>Создать</button>
    </form>
    <br /><br /><br />
    <form>
      <span>Визит</span>
      <br /><br />
      <label for="from">С:</label>
      <input type="text" v-model="company" id="from" required />
      <input type="text" v-model="company" id="from" required />
      <br /><br />
      <label for="to">До:</label>
      <input type="text" v-model="company" id="to" required />
      <input type="text" v-model="company" id="to" required />
      <br /><br />
      <label for="phone">Номер телефона</label>
      <input type="text" v-model="company" id="phone" required />
      <br /><br />
      <label for="e-mail">E-mail</label>
      <input type="email" v-model="company" id="e-mail" required />
      <br /><br />
      <label for="client">Клиент</label>
      <input type="text" v-model="company" id="client" required />
      <br /><br />
      <label for="worker">Сотрудник</label>
      <input type="text" v-model="company" id="worker" required />
      <br /><br />
      <input type="checkbox" v-model="company" id="reminder" />
      <label for="reminder">Напоминание</label>
      <br /><br />
      <button>Создать</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {};
  },
  methods: {},
};
</script>
