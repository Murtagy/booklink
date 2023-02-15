import { createApp } from "vue";

import { createPinia } from "pinia";

import App from "./App.vue";
import router from "./router/router_main";
import { OpenAPI } from "./client/core/OpenAPI";

const app = createApp(App);
// Vue.config.productionTip = false;

const apiURL = import.meta.env.VITE_APP_API_URL;
if (import.meta.env.DEV) {
  OpenAPI.BASE = apiURL;
}

app.use(createPinia());
app.use(router);

declare module "vue" {
  interface ComponentCustomProperties {
    $authStore: any;
    // {  // tmp - copying the inferred type from VSCode
    //       jwt_auth: string;
    //       setJwt(jwt: string): void;
    //     };
  }
}

app.mount("#app");
