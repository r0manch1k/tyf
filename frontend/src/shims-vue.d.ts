/* eslint-disable */
declare module "*.vue" {
  import type { DefineComponent } from "vue";
  const component: DefineComponent<{}, {}, any>;
  export default component;
}

declare module "*.css" {
  const value: string;
  export default value;
}

declare module "@/assets/styles/js/main.js" {
  const value: any;
  export default value;
}

declare module "@/assets/styles/bootstrap/js/bootstrap.bundle.js" {
  const value: any;
  export default value;
}
