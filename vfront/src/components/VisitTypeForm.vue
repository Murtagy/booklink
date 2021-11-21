<template>
    
    <form>
      <ul>
        <li>
          <button v-on:click="$emit('visit-select', 'visit-select-service')" ><img src="../assets/list-icon.jpg">Услуга</button>
          <div class="selected">
            <span class="service">Услуга 1</span>
            <span class="price">25 бел.руб.</span>
          </div>
        </li>
        <li>
          <button v-on:click="$emit('visit-select', 'visit-select-worker')" ><img src="../assets/worker-icon.png">Сотрудник</button>
          <div class="selected">
            Сотрудник
          </div>
        </li>
        <li>
          <button v-on:click="$emit('visit-select', 'visit-select-datetime')" ><img src="../assets/calendar-icon.png">Дата и время</button>
          <div class="selected">
            Дата и время
          </div>
        </li>
      </ul>
          <input type="button" value="Сформировать запись" name="create-visit" id="create-visit">
    </form>

</template>

<style scoped src="@/assets/styles/visit.css"></style>

<script>

export default {}

</script>
