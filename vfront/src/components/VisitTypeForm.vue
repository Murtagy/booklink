<template>
    
    <form>
      <ul>
        <li>
          <button v-on:click="$emit('visit-select', 'visit-select-service')" ><img src="../assets/list-icon.png">Услуга</button>
        </li>
        <li>
          <button v-on:click="$emit('visit-select', 'visit-select-worker')" ><img src="../assets/worker-icon.jpg">Сотрудник</button>
        </li>
        <li>
          <button v-on:click="$emit('visit-select', 'visit-select-datetime')" ><img src="../assets/calendar-icon.png">Дата и время</button>
        </li>
      </ul>
          <input type="button" value="Сформировать запись" name="create-visit" id="create-visit">
    </form>

</template>

<style scoped src="@/assets/styles/visit.css"></style>

<script>

export default {}

</script>
