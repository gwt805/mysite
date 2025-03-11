import "./style.css";
import App from "./App.vue";
import { createApp } from "vue";
import router from "@/routes/index";
import "element-plus/dist/index.css";
import ElementPlus from "element-plus";
import disableDevtool from'disable-devtool';
import "element-plus/theme-chalk/dark/css-vars.css";
import zhCn from "element-plus/es/locale/lang/zh-cn";
import * as ElementPlusIconsVue from "@element-plus/icons-vue";

// disableDevtool({
//     url: "https://www.baidu.com/",
//     timeOutUrl: "https://www.baidu.com/",
//     interval: 10
// });

const app = createApp(App);
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component);
}
app.use(ElementPlus, {
    locale: zhCn,
});
app.use(router);
app.mount("#app");