<template>
  <div id="app">
    <TopPanel v-if="!skipPanel" />
    <router-view />
  </div>
</template>

<script lang="ts">
import "@/assets/styles/main.css";
import TopPanel from "@/components/TopPanel.vue";

export default {
  components: { TopPanel },
  computed: {
    skipPanel() {
      const path = this.$router.currentRoute.value.path;
      if (path == "/login") {
        return true;
      }
      if (path == "/registration") {
        return true;
      }
      return false;
    },
  },
  data() {
    return {};
  },
};
</script>
