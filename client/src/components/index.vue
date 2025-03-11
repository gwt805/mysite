<template>
    <div class="container">
        <video src="../assets/background.mp4" autoplay="true" loop="true" muted="true"></video>
        <div class="nav">
            <div class="logo"><img src="/logo.png" draggable="false"></div>
            <div class="nav-list">
                <a class="nav-item" @click="go('/website')">导航网</a>
                <a class="nav-item" @click="go('/blog')">博客</a>
                <a class="nav-item" @click="go('/console')">控制台</a>
            </div>
        </div>
        <div class="yiyan" @mousemove="mousemove" @mouseout="mouseup">{{ displayedText }}
            <el-tooltip content="换一条" :hide-after="0"><el-icon @click="refresh"><Refresh /></el-icon></el-tooltip>
        </div>
        <div class="footer">
            <el-tooltip content="Github" :hide-after="0"><span><a onclick="window.open('https://github.com/gwt805')" target="_blank"><img src="../assets/github.svg"></a></span></el-tooltip>
            <el-tooltip content="Gitee" :hide-after="0"><span><a onclick="window.open('https://gitee.com/gwt805')" target="_blank"><img src="../assets/gitee.svg"></a></span></el-tooltip>
            <el-tooltip content="GitCode" :hide-after="0"><span><a onclick="window.open('https://gitcode.com/gwt805')" target="_blank"><img src="../assets/gitcode.svg"></a></span></el-tooltip>
            <el-tooltip content="<img src='/gzh.jpg' style='width:100px;' />" raw-content :hide-after="0"><span><img src="../assets/gzh.svg"></span></el-tooltip>
            <span>Copyright © gwt805</span>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";
import router from "@/routes/index";
const yiyan = ref("");
const displayedText = ref("");
const typingInterval = ref();
const isTyping = ref(false);

const getYiyan = () => {
    clearInterval(typingInterval.value);
    isTyping.value = false;
    displayedText.value = "";
    const httml = new XMLHttpRequest(); 
    httml.open("GET", "https://api.nnxv.cn/api/yiyan.php", true);
    httml.send();
    httml.onreadystatechange = function () {
        if (httml.readyState == 4 && httml.status == 200) {
            yiyan.value = JSON.parse(httml.responseText).content;
            startTyping();
        }
    };
    httml.onerror = function () {
        yiyan.value = "如果你有梦想，就要守护它。";
        startTyping();
    };
};

const startTyping = () => {
    if (isTyping.value) {
        clearInterval(typingInterval.value);
    }
    
    let index = 0;
    displayedText.value = "";
    isTyping.value = true;
    
    typingInterval.value = setInterval(() => {
        if (index < yiyan.value.length) {
            displayedText.value += yiyan.value[index];
            index++;
        } else {
            clearInterval(typingInterval.value);
            isTyping.value = false;
            setTimeout(() => {
                if (!isTyping.value) {
                    displayedText.value = "";
                    startTyping();
                }
            }, 1000);
        }
    }, 150);
};

const refresh = () => {
    clearInterval(typingInterval.value);
    getYiyan();
}

const mousemove = () => {
    if (isTyping.value) {
        clearInterval(typingInterval.value);
        isTyping.value = false;
    }
    displayedText.value = yiyan.value;
}

const mouseup = () => {
    if (!isTyping.value) {
        startTyping();
    }
}
const go = (url: string) => { router.push(url) }//window.location.href = url;}
onMounted(() => { getYiyan(); });
onUnmounted(() => {
    clearInterval(typingInterval.value);
});
</script>

<style scoped lang="less">
.container {
    width: 100vw;
    height: 100vh;
    user-select: none;

    video {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        object-fit: cover;
        z-index: -1;
    }

    .nav {
        width: 100%;
        height: 40px;
        background-color: rgba(0, 0, 0, 0.5);
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0 20px;
        box-sizing: border-box;

        .logo {
            width: 34px;
            height: 34px;

            img {
                width: 100%;
                height: 100%;
                object-fit: cover;
            }
        }

        .nav-list {
            display: flex;
            justify-content: space-between;
            align-items: center;

            .nav-item {
                margin-left: 20px;
                color: #fff;
                cursor: pointer;

                &:hover {
                    color: #8d8d8d;
                }
            }
        }
    }

    .yiyan {
        max-width: 80%;
        word-wrap: break-word;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        color: #fff;
        font-size: 20px;
        line-height: 1.5;
        padding: 20px;
        border-radius: 10px;
        background-color: rgba(0, 0, 0, 0.3);
        .el-icon {
            display: none;
            position: relative;
            bottom: -25px;
            right: -20px;
        }
    }
    .yiyan:hover {
        .el-icon {
            display: block;
            float: inline-end;
        }
    }

    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        height: 32px;
        display: flex;
        justify-content: center;
        align-items: center;
        color: #a0a4e5;
        z-index: 2;
        font-weight: bolder;
        span:not(:first-child) {
            margin-left: 10px;
        }
    }

}
</style>