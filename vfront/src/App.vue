<script>
import "./assets/styles/main.css";

import HomePage from "./components/Home.vue";
import RegistrationPage from "./components/Registration.vue";
import NotFoundPage from "./components/404.vue";

const routes = {
  "/": HomePage,
  "/registration": RegistrationPage,
};

export default {
  name: "App",
  components: {},
  computed: {
    CurrentComponent() {
      return routes[window.location.pathname] || NotFoundPage;
    },
  },
  render(h) {
    return h(this.CurrentComponent);
  },
};
</script>