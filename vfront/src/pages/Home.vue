<template>
    <div>
    <div id="nav">
      <router-link to="/">Home</router-link> |
      <router-link to="/registration">Registration</router-link> |
      <router-link to="/visit">Visit</router-link> |
      <router-link to="/dev">Dev</router-link> |
      <router-link to="/calendar">Calendar</router-link> |
      <router-link to="/time">Time</router-link>
    </div>
    <h1> Home page</h1>
    <br>
    <span>Multiline message is:</span>
    <p style="white-space: pre-line;">{{ message }}</p>
    <br>
    <textarea v-model="message" placeholder="add multiple lines"></textarea>
    </div>
</template>

<script>
console.log("HARDCODE", process.env.HARDCODE)
export default {
    data() {return {'message': ''}},
}
</script>