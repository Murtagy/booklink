import { createApp } from "vue";

import axios from "axios";
import { createPinia } from "pinia";

import App from "./App.vue";
import router from "./router/router_main";
import authStore from "./auth_store";

const app = createApp(App);
// Vue.config.productionTip = false;

const apiPlugin = {
  install(app: any) {
    // configure the app
    app.config.globalProperties.$api = axios.create({
      baseURL: "http://localhost:8000/",
    });
  },
};

const _auth = authStore();

const authPlugin = {
  install(app: any) {
    // configure the app
    app.config.globalProperties.$authStore = _auth;
  },
};

app.use(createPinia());
app.use(apiPlugin);
app.use(authPlugin);
app.use(router);

declare module "vue" {
  interface ComponentCustomProperties {
    $api: typeof axios;
    $authStore: typeof _auth;
  }
}

app.mount("#app");
