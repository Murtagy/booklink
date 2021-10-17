import Vue from 'vue'

import axios from 'axios'
import App from './App.vue'
import router from './router/router_main'


Vue.config.productionTip = false

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
  render: h => h(App)
}).$mount('#app')
