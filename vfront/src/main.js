import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import App from './App.vue'
import router from './router/router_main'
import store from './app_store'

Vue.config.productionTip = false
Vue.use(Vuex)
Vue.use({
    install (Vue) {
    Vue.prototype.$api = axios.create({
      baseURL: 'http://localhost:8000/'
    })
  }
})


new Vue({
  // data: {http: axios},
  router,
  store,
  render: h => h(App)
}).$mount('#app')
