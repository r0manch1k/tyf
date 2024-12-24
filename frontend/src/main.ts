import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./stores";
import { Tabs, Tab } from "vue3-tabs-component";

createApp(App)
  .component("Tabs", Tabs)
  .component("Tab", Tab)
  .use(store)
  .use(router)
  .mount("#app");
