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
        <input
          type="button"
          value="Войти"
          @click="Login"
          id="submit"
        />
      </ul>
      <p style="margin-left:3em;"> 
        <router-link to="/registration" >
        (Перейти к регистрации)
        </router-link>
      </p>
    </form>
  </div>
</template>

<style scoped src="@/assets/styles/registration.css"></style>

<script lang="ts">
import type { TokenOut } from "@/client";
import { OpenAPI } from "@/client/core/OpenAPI";
import type { AxiosResponse } from "axios";
import WideHeader from "../components/WideHeader.vue";

export default {
  components: { WideHeader },
  data() {
    return {
      username: "",
      password: "",
    };
  },
  methods: {
    make_form() {
      var body = new FormData();
      body.append("username", this.username);
      body.append("password", this.password);
      return body;
    },
    async Login() {
      console.log("Login");
      if (this.username == "") {
        alert("Логин не указан");
      } else {
        try {
          const response: AxiosResponse<TokenOut> = await this.$api.post(
            "/token",
            this.make_form()
          );
          const token = response.data.access_token;
          this.$authStore.setJwt(token);
          OpenAPI.TOKEN = token;
          this.$router.push("/my_user");
        } catch (e: any) {
          if (e.response) {
            this.DisplayErrorFromResponse(e.response);
          } else {
            console.log(e);
            throw e;
          }
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
