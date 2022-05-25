<template>
  <table>
    <tr v-for="time in timess" :key="time">
      {{
        time
      }}
    </tr>
  </table>
</template>

<script>
export default {
  props: {
    timess: Array,
  },
};
</script>
