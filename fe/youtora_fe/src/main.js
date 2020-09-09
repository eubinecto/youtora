import Vue from 'vue'
import router from './router'
import App from './App.vue'
import Vuex from 'vuex'

import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'

import store from './store/index';

// Install BootstrapVue
Vue.use(BootstrapVue)
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin)

Vue.use(Vuex)

Vue.config.productionTip = false

new Vue({
  store,
  router,
  render: h => h(App),
}).$mount('#app')
