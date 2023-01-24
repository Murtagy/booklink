<template>
  <div v-if="user">My user: {{ user }}</div>
</template>

<script lang="ts">
import type { AxiosError, AxiosResponse } from "axios";

export default {
  data(): { user: number | null } {
    return { user: null };
  },
  methods: {
    async getUser() {
      console.log("Getting user for jwt", this.$authStore.jwt_auth);
      const response: AxiosResponse<{ user_id: number }> = await this.$api.get(
        "/my_user",
        {
          headers: { Authorization: "bearer " + this.$authStore.jwt_auth },
        }
      );
      if (response.data == null) {
        alert("Not logged in");
      } else {
        let user_id = response.data.user_id;
        console.log("GOT USER", response);
        this.user = user_id;
      }
    },
    created() {
      console.log("CREATED");
      this.getUser();
    },
  },
};
</script>
