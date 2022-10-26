<template>
  <p>{{services}}</p>
  <p>{{visit_time}}</p>
  <p>{{worker}}</p>
</template>

<!-- <style scoped src="@/assets/styles/worker.css"></style> -->

<script>
export default {
  components: {},
  data() {
    return {};
  },
  methods: {},
  props: ["worker", "visit_time", "services"],
};
</script>
