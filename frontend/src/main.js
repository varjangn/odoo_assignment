import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import VCalendar from 'v-calendar';
import 'v-calendar/style.css';

const vuetify = createVuetify({
    components,
    directives,
})

const app = createApp(App)

app.use(router)
app.use(vuetify) // vuetify is mainly used for grid systems
app.use(VCalendar, {})

app.mount('#app')
