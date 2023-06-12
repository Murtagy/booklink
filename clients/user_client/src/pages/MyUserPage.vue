<template>
  <todo>
    <div> Описание и редактирование клиента, </div>
    <div> 
      Редактирование юзера,
    </div>
    <div> 
      Редактирование онлайн записи
    </div>
 </todo>
  <div v-if="user">My user: {{ user }}</div>
  <div v-if="user">My user: {{ user2 }}</div>
</template>

<script lang="ts">
import { DefaultService, type UserOut } from "@/client";

export default {
  data(): { user: number | null; user2: null | UserOut } {
    return { user: null, user2: null };
  },

  async mounted() {
    this.getUser();
    this.user2 = await this.getUser2();
  },
  methods: {
    async getUser() {
      console.log("Getting user for jwt", this.$authStore.jwt_auth);
      this.user = (await DefaultService.readUsersMe2()).user_id;
    },
    async getUser2() {
      const user = await this.$authStore.getUserMust();
      return user;
    },
  },
};
</script>
