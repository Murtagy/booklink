<template>
  <div class="box">
    <button
      v-for="worker in workers"
      :key="worker.worker_id"
      @click="emitWorker(worker)"
    >
      <img src="../assets/worker-photo.jpg" />
      <span id="name">{{ worker.name }} </span>
      <br /><br /><span id="job">{{ worker.job_title }}</span
      ><br />
      <br />
      <!-- {{ worker.description }} -->
      <input
        type="button"
        class="sticky_button"
        @click="emitWorker(null)"
        value="Сбросить"
      />
    </button>
  </div>
</template>

<style scoped src="@/assets/styles/worker.css"></style>

<script lang="ts">
import type { OutWorker } from "@/client/models/OutWorker";

export default {
  components: {},
  methods: {
    emitWorker: function (x: OutWorker | null) {
      this.$emit("select-worker", x);
    },
  },
  props: {
    workers: {
      type: Array<OutWorker>,
      required: true,
    },
  },
};
</script>
