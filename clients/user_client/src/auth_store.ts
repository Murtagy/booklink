// import Vue from "vue";
import { defineStore } from "pinia";

// Vue.use(Vuex);

function getCookie(cname: string) {
  const name = cname + "=";
  const decodedCookie = decodeURIComponent(document.cookie);
  const ca = decodedCookie.split(";");
  for (let i = 0; i < ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == " ") {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

function setCookie(cname: string, cvalue: string, exdays: number) {
  const d = new Date();
  d.setTime(d.getTime() + exdays * 24 * 60 * 60 * 1000);
  const expires = "expires=" + d.toUTCString();
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function checkAuthCookie() {
  return getCookie("jwtAuth");
}

const authStore = defineStore("auth", {
  state: () => ({
    jwt_auth: checkAuthCookie(),
  }),
  actions: {
    setJwt(jwt: string) {
      console.log("Setting token");
      setCookie("jwtAuth", jwt, 14);
      this.jwt_auth = jwt;
    },
  },
});
// const initialized_store = store()
export default authStore;