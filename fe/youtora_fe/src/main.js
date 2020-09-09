import Vue from 'vue'
import router from './router'
import App from './App.vue'
import Vuex from 'vuex'
import store from './store/index';

import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'

import { library } from '@fortawesome/fontawesome-svg-core'
import {
  faLanguage, faClosedCaptioning, faArchive, faFilter, faThumbsDown, faThumbsUp, faBookmark, faEye
} from '@fortawesome/free-solid-svg-icons'

import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(faLanguage, faClosedCaptioning, faArchive, faFilter, faThumbsDown, faThumbsUp, faBookmark, faEye)
Vue.component('font-awesome-icon', FontAwesomeIcon)

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
