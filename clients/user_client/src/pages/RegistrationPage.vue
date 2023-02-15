<template>
  <div>
    <wide-header title="Регистрация"></wide-header>
    <form>
      <ul>
        <li>
          <label for="company">Компания</label>
          <input
            type="text"
            v-model="company"
            id="company"
            placeholder="Введите наименование юр. лица"
            required
          />
        </li>
        <li>
          <label for="email">E-mail</label>
          <input
            type="email"
            v-model="email"
            id="email"
            placeholder="Введите адрес электронной почты"
            required
          />
        </li>
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
        <li>
          <label for="password-confirmation">Подтвердите пароль</label>
          <input
            type="password"
            v-model="password_confirmation"
            id="password-confirmation"
            placeholder="Введите пароль"
            required
          />
        </li>
        <input
          type="button"
          value="Создать пользователя"
          @click="Register"
          id="submit"
        />
      </ul>
    </form>
  </div>
</template>

<script lang="ts">
import { DefaultService } from "@/client/services/DefaultService";
import type { AxiosError, AxiosResponse } from "axios";
import { OpenAPI } from "@/client";

import WideHeader from "../components/WideHeader.vue";

export default {
  components: { WideHeader },
  data() {
    return {
      email: "",
      company: "",
      username: "",
      password: "",
      password_confirmation: "",
    };
  },
  methods: {
    async Register() {
      console.log("REGISTER");
      if (this.password != this.password_confirmation) {
        alert("Пароль не совпадает");
      } else if (this.password == "") {
        alert("Форма не заполнена");
      } else if (this.email == "") {
        alert("Форма не заполнена");
      } else if (this.username == "") {
        alert("Форма не заполнена");
      } else if (this.company == "") {
        alert("Форма не заполнена");
      } else {
        try {
          const response = await DefaultService.createUser({
            username: this.username,
            email: this.email,
            company: this.company,
            password: this.password,
          });
          let token = response.access_token;
          if (token) {
            this.$authStore.setJwt(token);
            OpenAPI.TOKEN = token;
            this.$router.push("/my_user");
          } else {
            this.DisplayError("Произошла ошибка");
          }
        } catch (e: any) {
          if (e.response) {
            this.DisplayErrorFromResponse(e.response);
          } else {
            this.DisplayError(e);
          }
          throw e;
        }
      }
    },
    DisplayError(e: any) {
      alert("Произошла ошибка" + e);
    },
    DisplayErrorFromResponse(response: AxiosResponse<any>) {
      let details = response.data.detail;
      let msg;
      if (details) {
        switch (details) {
          case "User email already exists":
            msg = "User email already exists";
            break;
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
