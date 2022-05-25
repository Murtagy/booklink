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
      path: "/registration",
      name: "Registration",
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      // component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
      component: () => import("../pages/RegistrationPage.vue"),
    },
    {
      path: "/visit",
      name: "Visit",
      component: () => import("../pages/VisitPage.vue"),
    },
    {
      path: "/my_user",
      name: "User",
      component: () => import("../pages/MyUser.vue"),
    },
    {
      path: "/dev",
      name: "Dev",
      component: () => import("../pages/DevPage.vue"),
    },
    {
      path: "/blank",
      name: "Blank",
      component: () => import("../pages/BlankPage.vue"),
    },
    {
      path: "/calendar",
      name: "Calendar",
      component: () => import("../pages/CalendarPicker.vue"),
    },
    {
      path: "/time",
      name: "Time",
      component: () => import("../pages/TimePicker.vue"),
    },
  ],
});
export default router;
