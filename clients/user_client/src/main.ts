import { createApp } from "vue";

import axios from "axios";
import { createPinia } from "pinia";

import App from "./App.vue";
import router from "./router/router_main";
import authStore from "./auth_store";
import { OpenAPI } from "./client/core/OpenAPI";

const app = createApp(App);
// Vue.config.productionTip = false;

const apiURL = import.meta.env.VITE_APP_API_URL;
if (import.meta.env.DEV) {
  OpenAPI.BASE = apiURL;
}

const authPlugin = {
  install(app: any) {
    // configure the app
    app.config.globalProperties.$authStore = authStore();
  },
};

const apiPlugin = {
  install(app: any) {
    // configure the app
    // this is no longer used! keeping as global var example
    app.config.globalProperties.$api = axios.create({
      baseURL: apiURL,
    });
  },
};

app.use(createPinia());
app.use(authPlugin);
app.use(apiPlugin);
app.use(router);

// reading token from cookies
const authstore = app.config.globalProperties.$authStore;
OpenAPI.TOKEN = authstore.jwt_auth;

axios.interceptors.response.use(undefined, function (error) {
  if (error) {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      // authstore.dispatch('LogOut')
      return router.push("/login");
    }
  }
  throw error;
});

declare module "vue" {
  interface ComponentCustomProperties {
    $api: typeof axios;
    $authStore: any;
    // {  // tmp - copying the inferred type from VSCode
    //       jwt_auth: string;
    //       setJwt(jwt: string): void;
    //     };
  }
}

app.mount("#app");
