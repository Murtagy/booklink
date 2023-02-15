<template>
  <div>
    <wide-header title="Войти"></wide-header>
    <form>
      <ul>
        <li>
          <label for="username">Логин</label>
          <input
            type="text"
            v-model="username"
            id="username"
            placeholder="Введите имя пользователя"
            required
          />
        </li>
        <li>
          <label for="password">Пароль</label>
          <input
            type="password"
            v-model="password"
            id="password"
            placeholder="Введите пароль"
            required
          />
        </li>
        <input type="button" value="Войти" @click="Login" id="submit" />
      </ul>
    </form>
  </div>
</template>

<script lang="ts">
import WideHeader from "../components/WideHeader.vue";
import { DefaultService, OpenAPI } from "@/client";

export default {
  components: { WideHeader },
  data() {
    return {
      username: "",
      password: "",
    };
  },
  methods: {
    async Login() {
      console.log("Login");
      if (this.username == "") {
        alert("Логин не указан");
      } else {
        try {
          const response = await DefaultService.loginForAccessToken({
            username: this.username,
            password: this.password,
          });
          let token = response.access_token;
          this.$authStore.setJwt(token);
          OpenAPI.TOKEN = token;
          this.$router.push("/my_user");
        } catch (e: any) {
          if (e.response) {
            this.DisplayErrorFromResponse(e.response);
          } else {
            console.log(e);
            this.DisplayError(e);
          }
          throw e;
        }
      }
    },
    DisplayError(e: any) {
      alert("Произошла ошибка" + e);
    },
    DisplayErrorFromResponse(response: any) {
      let details = response.data.detail;
      let msg;
      if (details) {
        switch (details) {
          default:
            msg = details;
        }
        alert(msg);
      }
    },
  },
};
</script>

<style scoped src="@/assets/styles/registration.css"></style>
