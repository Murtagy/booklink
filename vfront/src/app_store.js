// import Vue from "vue";
import { defineStore } from "pinia";

// Vue.use(Vuex);

function getCookie(cname) {
  let name = cname + "=";
  let decodedCookie = decodeURIComponent(document.cookie);
  let ca = decodedCookie.split(";");
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

function setCookie(cname, cvalue, exdays) {
  const d = new Date();
  d.setTime(d.getTime() + exdays * 24 * 60 * 60 * 1000);
  let expires = "expires=" + d.toUTCString();
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function checkAuthCookie() {
  return getCookie("jwtAuth");
}

const useStore = defineStore("auth", {
  state: () => {
    return { jwt_auth: checkAuthCookie() };
  },
  actions: {
    setJwt(state, jwt) {
      console.log("Setting token");
      setCookie("jwtAuth", jwt, 14);
      state.jwt_auth = jwt;
    },
  },
});
// const initialized_store = store()
export default useStore;
