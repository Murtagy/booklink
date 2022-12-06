<template>
  <div class="box">
    <!-- <p>{{services}}</p> -->
    <p class="bold">Выбранные услуги:</p>
    <li v-for="service in services" :key="service.service_id">
      <label :for="service.service_id">{{ service.name }}</label>
      <span class="price">{{ service.price }} {{ service.currency }}</span>
    </li>

    <!-- <p>{{visit_time}}</p> -->
    <p class="bold">Время:</p>
    <p class="border_main1" style="padding: 1em">
      {{ this.parse_date(visit_time) }}
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
    <input type="button" value="Подтвердить запись" class="sticky_button" />
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
</style>

<script lang="ts">
export default {
  components: {},
  data() {
    return {};
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
  },
  props: ["worker", "visit_time", "services"],
};
</script>
