<template>
  <div id="app">
    <img alt="Vue logo" src="./assets/logo.png">
    <FunctionalCalendar
       v-model="calendarData"
       :is-date-picker="true"      
></FunctionalCalendar>
    <HelloWorld msg="Welcome to Your Vue.js App"/>
  </div>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'
import FunctionalCalendar from './components/Calendar.vue'

export default {
  name: 'App',
  components: {
    HelloWorld,
    FunctionalCalendar
  },
  data(){ return {calendarData: {}}}
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
