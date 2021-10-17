<template>
  <div>
    <wide-header title="Онлайн-запись" />

    <form>
      <ul>
        <li>
          <button><img src="../assets/list-icon.png">Услуга</button>
        </li>
        <li>
          <button><img src="../assets/worker-icon.jpg">Сотрудник</button>
        </li>
        <li>
          <button><img src="../assets/calendar-icon.png">Дата и время</button>
        </li>
      </ul>
          <input type="button" value="Сформировать запись" name="create-visit" id="create-visit">
    </form>
  </div>
</template>

<style scoped src="@/assets/styles/visit.css"></style>

<script>
import WideHeader from "../components/WideHeader.vue";
export default {
  components: { WideHeader },
};
</script>
