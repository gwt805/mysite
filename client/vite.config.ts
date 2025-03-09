const os = require("os")
import { resolve } from "path";
import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import { webUpdateNotice } from "@plugin-web-update-notification/vite";

function getNetWorkIp() {
  let needHost = ""
  try {
    let network = os.networkInterfaces()
    for (const dev in network) {
      let iface = network[dev]
      for (let i = 0; i < iface.length; i++) {
        const alias = iface[i]
        if (alias.family === "IPv4" && alias.address !== "127.0.0.1" && !alias.internal && alias.address.indexOf("172") == "-1") {
          needHost = alias.address
        }
      }
    }
  } catch (error) {
    needHost = "localhost"
  }
  return needHost
}
// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    webUpdateNotice({
      versionType: "build_timestamp",
      checkInterval: 1000,
      checkOnWindowFocus: true,
      locale: "zh_CN",
      localeData: {
        en_US: {
          title: "📢 system update",
          description: "System update, please refresh the page",
          buttonText: "refresh",
          dismissButtonText: "dismiss",
        },
        zh_CN: {
          title: "📢 系统更新",
          description: "有新版本发布, 请刷新页面",
          buttonText: "好的",
          dismissButtonText: "取消",
        }
      }
    })
  ],
  resolve: {
    extensions: ['.js', '.ts', '.jsx', '.tsx', '.json', '.vue'],
    alias:{
      '@': resolve(__dirname,'src/'),
      'components': resolve(__dirname,'src/components/'),
      'utils': resolve(__dirname,'src/utils/'),
      'api': resolve(__dirname,'src/api/'),
    }
  },
  server: {
    host: "0.0.0.0",
    port: 5173,
    open: true,
  },
  define: {
    'import.meta.env.BASE_IP': JSON.stringify(getNetWorkIp())
  }
})
