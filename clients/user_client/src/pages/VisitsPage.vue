<template>
  <h2> Ближайшие визиты </h2>
  <div>
    <VisitsCarusel :date_from="date_from" :date_to="date_to" />
  </div>
</template>

<style scoped></style>

<script lang="ts">
import VisitsCarusel from "@/components/VisitsCarusel.vue";

declare interface Data {
  date_from: Date;
  date_to: Date;
}

export default {
  components: { VisitsCarusel },
  data(): Data {
    const today = new Date();
    const today_plus_7 = new Date(today.getTime() + 1000 * 60 * 60 * 24 * 7);
    return {
      date_from: today,
      date_to: today_plus_7,
    };
  },
};
</script>
