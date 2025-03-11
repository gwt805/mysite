<template>
  <div class="login-box" id="demo" v-loading="loading" element-loading-text="正在登录请稍后...">
    <div class="input-content">
      <div class="login_tit">
        <div><i class="tit-bg left"></i>Everyday · 博客系统<i class="tit-bg right"></i></div>
        <p>Notes&nbsp;&nbsp;&nbsp;&nbsp;Everyday</p>
      </div>
      <p class="p user_icon">
        <input type="text" placeholder="用户名" autocomplete="off" class="login_txtbx" v-model="loginform.username">
      </p>
      <p class="p pwd_icon">
        <input type="password" placeholder="密码" autocomplete="off" class="login_txtbx" v-model="loginform.password">
      </p>
      <div class="signup">
        <a class="gv" @click="backup">返&nbsp;&nbsp;回</a>
        <a class="gv" @click="loginfn()" v-if="!is_resiter">登&nbsp;&nbsp;录</a>
      </div>
    </div>
    <div class="canvaszz"> </div>
    <canvas id="canvas"></canvas>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";
import '@/assets/js/login_canvas.js';
import { login } from '@/api/auth';
import router from "@/routes/index";
import { public_elmsg_success, public_elmsg_warning } from "@/utils/elmsg/index";

document.title = "登录";

const is_resiter = ref(false);
const loginform = ref({ 'username': '', 'password': '', 'password1': '' });
const loading = ref(false);

watch(is_resiter, () => { loginform.value = { 'username': '', 'password': '', 'password1': '' }; });

const loginfn = () => {
  loading.value = true;
  if (loginform.value.username.trim() == "") {
    public_elmsg_warning("用户名不能为空");
    return;
  }
  if (loginform.value.password.trim() == "") {
    public_elmsg_warning("密码不能为空");
    return;
  }
  login(loginform.value.username.trim(), loginform.value.password.trim()).then((res: any) => {
    loading.value = false;
    if (res.code == 0) {
      window.localStorage.setItem("token", JSON.stringify(res.token));
      public_elmsg_success("登录成功");
      setTimeout(() => {
        if (router.currentRoute.value.query.redirect) {
          const redirect: any = router.currentRoute.value.query.redirect;
          window.location.href = redirect;
        }
        else {
          window.location.href = "/index";
        }
      }, 2000);
    } else public_elmsg_warning(res.msg);
  })
};
const backup = () => window.history.back();
if (localStorage.getItem("token") != null) window.location.href = "/index";
</script>

<style scoped>
#error {
  color: red;
  font-size: 16px;
}

.login-box {
  margin: auto;
  width: 100%;
  height: 100%;
  background-color: #000;
  position: fixed;
}

.login-box canvas {
  width: 100%;
  height: auto;
  display: inline-block;
  vertical-align: baseline;
  position: absolute;
  z-index: -1;
}

.login-box .canvaszz {
  width: 100%;
  background-image: url("../assets/imgs/in_top_bj.png");
  height: 800px;
  position: absolute;
  z-index: 10;
  filter: alpha(opacity=40);
  -moz-opacity: 0.4;
  -khtml-opacity: 0.4;
  opacity: 0.4;
}

.login_tit {
  position: absolute;
  top: -60px;
  left: -5px;
  width: 420px;
  color: #fff;
  text-align: center;

}

.tit-bg {
  position: absolute;
  top: 50%;
  display: inline-block;
  width: 90px;
  height: 1px;
  background: url("../assets/imgs/login-tit.png")
}

.tit-bg.left {
  left: 0;
  transform: rotate(180deg)
}

.tit-bg.right {
  right: 0
}

.login_tit>div {
  position: relative;
  font-size: 22px;
  font-weight: bold;
}

.login_tit>p {
  font-size: 18px;
  font-family: "arial";
  margin: 10px 0;
}

.login-box .signup {
  margin-top: 40px;
  text-align: center
}

.login-box .signup a.gv {
  text-decoration: none;
  background: url("../assets/imgs/nav_gv.png") repeat 0px 0px;
  width: 130px;
  height: 43px;
  display: inline-block;
  text-align: center;
  /*姘村钩灞呬腑*/
  line-height: 43px;
  /*涓婁笅灞呬腑*/
  cursor: pointer;
  margin: 8px 20px 8px 20px;
  font: 18px/43px 'microsoft yahei';
  color: #066197;
}

.login-box .signup a.gv span {
  display: none;

}

.login-box .signup a.gv:hover {
  background: url("../assets/imgs/nav_gv.png") repeat 0px -43px;
  color: #1d7eb8;
  --webkit-box-shadow: 0 0 6px #1d7eb8;
  transition-duration: 0.5s;
}

.login-box .topcn {
  width: 980px;
  top: 200px;
  left: 50%;
  margin-left: -490px;
  position: absolute;
  z-index: 20;

}

/*登录界面*/
#demo {
  user-select: none;
}

.input-content {
  position: absolute;
  z-index: 9999;
  padding: 30px;
  width: 350px;
  left: 50%;
  margin-left: -205px;
  top: 25%
}

.input-content .p {
  margin: 10px 0;
  height: 44px;
  position: relative;
}

.input-content .p .login_txtbx {
  font-size: 14px;
  height: 26px;
  line-height: 26px;
  padding: 8px 9%;
  width: 81%;
  text-indent: 1em;
  border: 1px solid #1d7eb8;
  background: rgba(0, 0, 0, .1);
  color: white;
}

.login_txtbx::-webkit-input-placeholder {
  color: rgba(255, 255, 255, .9);
}

.login_txtbx:-moz-placeholder {
  /* Mozilla Firefox 4 to 18 */
  color: rgba(255, 255, 255, .9);
}

.login_txtbx::-moz-placeholder {
  /* Mozilla Firefox 19+ */
  color: rgba(255, 255, 255, .9);
}

.login_txtbx:-ms-input-placeholder {
  /* Internet Explorer 10+ */
  color: rgba(255, 255, 255, .9);
}

.input-content .p .login_txtbx:focus,
.input-content p .login_txtbx:hover {
  --webkit-box-shadow: 0 0 6px #1d7eb8;
  transition-duration: 0.5s;
}

.input-content .p.user_icon:before {
  content: "u";
}

.input-content .p.pwd_icon:before {
  content: "p";
}

.input-content .p.email_icon:before {
  content: "e";
}

.input-content .p:before {
  font-family: 'adminthemesregular';
  position: absolute;
  top: 0;
  left: 14px;
  height: 42px;
  line-height: 42px;
  font-size: 20px;
  color: #fff;
}

.input-content .p .checkcode {
  float: left;
  width: 205px;
  height: 44px;
  overflow: hidden;
}

.input-content .p .checkcode input {
  float: left;
  width: 120px;
  height: 36px;
  line-height: 36px;
  border: 1px solid #1d7eb8;
  padding: 3px;
  color: white;
  outline: none;
  text-indent: 3.1em;
}

.input-content .p .checkcode canvas {
  float: right;
  width: 85px;
  height: 38px;
  padding: 3px;
  z-index: 0;
  background: rgba(28, 122, 178, .3);
}

.input-content .p .ver_btn {
  color: #f4f4f4;
  height: 42px;
  line-height: 42px;
  margin: 0;
  z-index: 1;
  position: relative;
  float: right;
  cursor: pointer;
  font-size: 14px;
}
</style>
