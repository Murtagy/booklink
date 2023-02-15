<template>
  <div v-if="user">My user: {{ user }}</div>
</template>

<script lang="ts">
import type { AxiosError, AxiosResponse } from "axios";
import { DefaultService } from "@/client";

export default {
  data(): { user: number | null } {
    return { user: null };
  },

  mounted() {
    this.getUser();
  },
  methods: {
    async getUser() {
      console.log("Getting user for jwt", this.$authStore.jwt_auth);
      this.user = (await DefaultService.readUsersMe2()).user_id;
    },
  },
};
</script>
