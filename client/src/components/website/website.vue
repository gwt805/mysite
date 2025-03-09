<template>
    <el-container>
        <div class="search">
            <img src="/logo.png" draggable="false" @click="$router.push('/index')">
            <el-input :prefix-icon="Search" :placeholder="placeholder" v-model="search" @change="init"></el-input>
            <div class="nav-list">
                <a class="nav-item">导航网</a>
                <a class="nav-item" @click="go('/blog')">博客</a>
                <a class="nav-item" @click="go('/console')">控制台</a>
            </div>
        </div>
        <div class="div-body">
            <el-aside>
                <el-menu default-active="" class="el-menu-vertical-demo" :collapse="false" :collapse-transition="false">
                    <el-menu-item :index="item.tag" @click="scrollToDiv(item.tag)" v-for="item in data">
                        <el-icon>
                            <CaretRight />
                        </el-icon><template #title>{{ item.tag }}</template>
                    </el-menu-item>
                </el-menu>
            </el-aside>
            <div id="bodyRef">
                <el-main>
                    <div class="main-body" v-for="item in data" :id="item.tag">
                        <div class="card-title">
                            <el-icon :size="20"><Paperclip /></el-icon><span>{{ item.tag }}</span>
                        </div>
                        <div class="div-card">
                            <el-tooltip :content="db.tooltip" :hide-after="0" raw-content v-for="db in item.body">
                                <div class="div-card-body" @click="npage(db.weburl)"><img :src="db.imgurl"><a>
                                        <p>{{ db.name }}</p>
                                    </a></div>
                            </el-tooltip>
                        </div>
                    </div>
                </el-main>
            </div>
        </div>
    </el-container>
</template>

<script setup lang="ts">
import { CaretRight, Search } from "@element-plus/icons-vue";
import { ref, onMounted } from "vue";
import { getdata } from "@/api/website";
import { ElLoading } from "element-plus";
import { Paperclip } from "@element-plus/icons-vue";

const data: any = ref([])
const search = ref("");
const placeholder = ref("");
const loadingService = ElLoading.service({ fullscreen: true, text: "正在加载资源 ~" });


const scrollToDiv = (id: string) => {
    const testDiv = document.getElementById(id);
    if (testDiv) { testDiv.scrollIntoView(true) }
};

const npage = (url: string) => { window.open(url) };

const init = () => {
    getdata(search.value.trim()).then(
        (res: any) => {
            data.value = res.data;
            placeholder.value = res.data[Math.floor(Math.random()*res.data.length)]['tag']
            loadingService.close();
        },
        (err:any)=>{
            console.log(err);
            loadingService.close();
        }
    );
}
const go = (url: string) => { window.location.href = url;}
onMounted(() => {init()})
</script>

<style scoped lang="less">
.el-container {
    width: 100%;
    height: 100%;
    position: absolute;
    user-select: none;
    top: 0;
    left: 0;
    display: flex;
    flex-direction: column;
    .search {
        width: 100%;
        height: 30px;
        margin: 0 auto;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        justify-content:space-around;
        img {
            width: 34px;
            margin-top: 10px;
        }
        .el-input {
            width:  50%;
            margin: 10px 0 0 0;
        }
        
        @media screen and (max-width: 768px) {
            width: 100% !important;
        }
        .nav-list {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 10px;

            .nav-item {
                margin-left: 20px;
                color: #fff;
                cursor: pointer;

                &:hover {
                    color: #8d8d8d;
                }
            }
            .nav-item:first-child {
                color: #8d8d8d;
            }
        }
    }
    .div-body {
        display: flex;
        flex-direction: row;
        width: 100%;
        height: calc(100% - 42px);
        border-top: 1px solid gray;
        margin-top: 1px;
        .el-aside {
            width: 200px;
            height: 100%;
            border-right: 1px solid gray;
            transition: width 0.3s;
            position: relative;
            
            &:deep(.el-menu--collapse) {
                width: 64px;
            }
            
            &:deep(.el-menu) {
                border-right: none;
            }
        }
        #bodyRef {
            flex: 1;
            height: 100%;
            transition: all 0.3s ease;
            overflow: hidden;

            .el-main {
                width: 100%;
                height: 100%;
                padding: 10px;
                overflow-y: auto;
                overflow-x: hidden;
                scrollbar-width: none;

                .main-body {
                    width: 100%;
                    margin-bottom: 20px;

                    .card-title {
                        height: 25px;
                        font-size: 20px;
                        color: skyblue;
                        margin-bottom: 10px;

                        .el-icon {
                            position: relative;
                            top: 3px;
                        }
                    }

                    .div-card {
                        margin-top: 10px;
                        display: grid;
                        grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
                        grid-gap: 15px;
                        
                        @media screen and (max-width: 450px) {
                            grid-template-columns: 1fr;
                        }

                        .div-card-body {
                            height: 50px;
                            display: flex;
                            align-items: center;
                            overflow: hidden;
                            background-color: rgba(255, 255, 255, 0.2);
                            opacity: 0.6;
                            border-radius: 10px;
                            backdrop-filter: blur(10px);
                            transition: all 0.3s ease;
                            cursor: pointer;

                            img {
                                width: 30px;
                                height: 30px;
                                margin: auto 0;
                                padding-left: 10px;
                            }

                            a {
                                flex: 1;
                                text-decoration: none;
                                padding-left: 10px;
                                
                                p {
                                    margin: 0;
                                    white-space: nowrap;
                                    overflow: hidden;
                                    text-overflow: ellipsis;
                                }
                            }
                        }

                        .div-card-body:hover {
                            opacity: 0.9;
                            transform: translateY(-2px);
                            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
                        }
                    }
                }

                .main-body:first-child {
                    margin-top: 0;
                }
            }
        }
    }
}
</style>