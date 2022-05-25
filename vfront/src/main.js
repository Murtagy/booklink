import { createApp } from "vue";

import axios from "axios";
import { createPinia } from "pinia";

import App from "./App.vue";
import router from "./router/router_main";
import useStore from "./app_store";

const app = createApp(App);
// Vue.config.productionTip = false;

const apiPlugin = {
  install(app) {
    // configure the app
    app.config.globalProperties.$api = axios.create({
      baseURL: "http://localhost:8000/",
    });
  },
};

const authPlugin = {
  install(app) {
    // configure the app
    app.config.globalProperties.$authStore = useStore();
  },
};

app.use(createPinia())
app.use(apiPlugin);
app.use(authPlugin);
app.use(router);

app.mount("#app");
