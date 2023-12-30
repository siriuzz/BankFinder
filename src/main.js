/**
 * main.js
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Components
import App from './App.vue'

// Composables
import { createApp } from 'vue'

// Plugins
import { registerPlugins } from '@/plugins'
import axios from 'axios';
import VueCookies from 'vue-cookies'


axios.defaults.withCredentials = true;
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

const app = createApp(App)
app.use(VueCookies)
app.config.globalProperties.$axios = axios;

registerPlugins(app)

app.mount('#app')
