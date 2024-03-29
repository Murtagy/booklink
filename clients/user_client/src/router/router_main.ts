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
      path: "/login",
      name: "Login",
      component: () => import("../pages/LoginPage.vue"),
    },
    {
      path: "/services",
      name: "Services",
      component: () => import("../pages/ServicesPage.vue"),
    },
    {
      path: "/service/:service_id",
      name: "service",
      component: () => import("../pages/ServicePage.vue"),
      props: true,
    },
    {
      path: "/workers",
      name: "Workers",
      component: () => import("../pages/WorkersPage.vue"),
    },
    {
      path: "/worker/:worker_id",
      name: "worker",
      component: () => import("../pages/WorkerPage.vue"),
      props: (route) => {
        let workerCached = undefined;
        if (route.params.workerCached) {
          workerCached = JSON.parse(route.params.workerCached as string);
        }
        return {
          worker_id: route.params.worker_id,
          workerCached: workerCached,
        };
      },
    },
    {
      path: "/worker/:worker_id/job_hours",
      name: "worker.job_hours",
      component: () => import("../pages/WorkerAvailabilityPage.vue"),
      props: true,
    },
    {
      path: "/vcalendar",
      name: "VCalendar",
      component: () => import("../pages/WorkersCalendarPage.vue"),
    },
    {
      path: "/visits",
      name: "Visits",
      component: () => import("../pages/VisitsPage.vue"),
    },
    {
      path: "/visits/day/:date",
      name: "visits.day",
      component: () => import("../components/VisitsDay.vue"),
      props: true,
    },
    {
      path: "/visit/create/:date",
      name: "visit.create",
      component: () => import("../pages/CreateVisitPage.vue"),
      props: true,
    },
    {
      path: "/visit/:visit_id",
      name: "visit.edit",
      component: () => import("../pages/EditVisit.vue"),
      props: true,
    },
    {
      path: "/visit",
      name: "Visit",
      component: () => import("../pages/VisitPage.vue"),
    },
    {
      path: "/my_user",
      name: "User",
      component: () => import("../pages/MyUserPage.vue"),
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
      component: () => import("../components/CalendarPicker.vue"),
    },
    {
      path: "/calendar_base",
      name: "CalendarBase",
      component: () => import("../components/BaseCalendar.vue"),
    },
    {
      path: "/time",
      name: "Time",
      component: () => import("../components/TimePicker.vue"),
    },
  ],
});
export default router;
