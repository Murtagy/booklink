// import Vue from "vue";
import { defineStore } from "pinia";
import { DefaultService, type UserOut } from "./client";
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

declare interface stateType {
  jwt_auth: string;
  user: null | UserOut;
}

const authStore = defineStore("auth", {
  state: (): stateType => ({
    jwt_auth: checkAuthCookie(),
    user: null,
  }),
  actions: {
    setJwt(jwt: string) {
      // console.log("Setting token");
      setCookie("jwtAuth", jwt, 14);
      this.jwt_auth = jwt;
    },
    async getUserMust(): Promise<UserOut> {
      if (this.user) {
        return this.user;
      }
      try {
        this.user = await DefaultService.readUsersMe();
      } catch (e) {
        console.log(e);
        throw e;
      }
      if (!this.user) {
        throw Error("Could not get user");
      }
      return this.user;
    },
  },
});

export default authStore;
