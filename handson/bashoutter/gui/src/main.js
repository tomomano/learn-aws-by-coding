import Vue from 'vue'
import Vuex from 'vuex'
import App from './App.vue'
import vuetify from './plugins/vuetify';
import 'roboto-fontface/css/roboto/roboto-fontface.css'
import '@mdi/font/css/materialdesignicons.css'

Vue.config.productionTip = false
Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    url: ""
  },
  mutations: {
    set_url (state, url) {
      state.url = url;
    }
  }
})

new Vue({
  vuetify,
  store: store,
  render: h => h(App)
}).$mount('#app')
