<template>
  <div class="box">
    <button
      v-for="worker in workers.workers"
      :key="worker.worker_id"
      @click="emitWorker(worker)"
    >
      <img src="../assets/worker-photo.jpg" />
      <span id="name">{{ worker.name }} </span>
      <br /><br /><span id="job">{{ worker.job_title }}</span
      ><br />
      <br />{{ worker.description }}
    </button>
  </div>
</template>

<style scoped src="@/assets/styles/worker.css"></style>

<script lang="ts">
import { Workers } from "@/models/Workers";
import type { Worker } from "@/models/Worker";

export default {
  components: {},
  data() {
    return {};
  },
  methods: {
    emitWorker: function (x: Worker) {
      this.$emit("select-worker", x);
    },
  },
  props: {
    workers: {
      type: Workers,
      required: true,
    },
  },
};
</script>
