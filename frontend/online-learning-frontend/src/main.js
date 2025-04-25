import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
// Bootstrap CSS and JS
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';

createApp(App).use(store).use(router).mount('#app');
