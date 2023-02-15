import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "Home",
      component: () => import("../pages/HomePage.vue"),
    },
    {
      path: "/visit",
      name: "Visit",
      component: () => import("../pages/VisitPage.vue"),
    },
    {
      path: "/blank",
      name: "Blank",
      component: () => import("../pages/BlankPage.vue"),
    },
    {
      path: "/calendar",
      name: "Calendar",
      component: () => import("../components/CalendarPicker.vue"),
    },
    {
      path: "/time",
      name: "Time",
      component: () => import("../components/TimePicker.vue"),
    },
  ],
});
export default router;
