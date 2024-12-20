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

declare module "*.js" {
  const value: js;
  export default value;
}

declare module "axios" {
  const value: any;
  export default value;
}
