<template>
  <footer>
    <p>I am a footer {{ counter }}</p>
    <!-- <button @click="counter++">KNOPKA</button> -->
  </footer>
</template>

<script lang="ts">
export default {
  props: {
    counter: Number,
  },
};
</script>
