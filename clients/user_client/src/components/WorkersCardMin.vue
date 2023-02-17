<template>
  <div class="card">
    <div class="border_main1" style="padding: 1em">
      <div>{{ worker.name }}, {{ worker.job_title }}</div>
    </div>
  </div>
</template>

<script lang="ts">
import type { OutWorker } from '@/client';
import type { PropType } from 'vue';

export default {
  props: {
    worker: {
      type: Object as PropType<OutWorker>,
      required: true
    }
  }
}
</script>