import App from "@/App.vue";
import router from "@/router";
import store from "@/stores";
import { createApp } from "vue";

import * as moment from "moment";
import "moment/locale/ru";

createApp(App).provide("moment", moment).use(store).use(router).mount("#app");
