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
          value="Создать пользователя"
          @click="Login"
          id="submit"
        />
      </ul>
    </form>
  </div>
</template>

<script lang="ts">
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
    Login() {
      console.log("Login");
      if (this.username == "") {
        alert("Логин не указан");
      } else {
        this.$api
          .post("/token", this.make_form())
          .then((response) => {
            let token = response.data.access_token as string;
            if (token) {
              this.$authStore.setJwt(token);
              this.$router.push("/my_user");
            } else {
              this.DisplayError("Ошибка");
            }
          })
          .catch((e) => {
            if (e.response) {
              this.DisplayErrorFromResponse(e.response);
            } else {
              console.log(e);
              this.DisplayError(e);
            }
          });
      }
    },
    DisplayError(e) {
      alert("Произошла ошибка", e);
    },
    DisplayErrorFromResponse(response) {
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
