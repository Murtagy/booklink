<template>
  <div id="app">
    <img alt="Vue logo" src="./assets/logo.png">
    <times timess=1234></times>
    <cal/>
    <example msg="Hello Masha"/>
    <FooterTest/>
  </div>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'
import FunctionalCalendar from './components/Calendar.vue'
import FooterTest from './components/FooterTest.vue'
import TimeSlots from './components/TimeSlots.vue'

export default {
  name: 'App',
  components: {
    'example': HelloWorld,
    'cal': FunctionalCalendar,
    'times': TimeSlots,
    FooterTest,
  },

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
