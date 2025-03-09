<template>
    <div class="container">
        <div class="nav">
            <div class="nav-left"><img src="../../assets/logo.png" draggable="false" @click="$router.push('/index')">
            </div>
            <div class="nav-list">
                <a class="nav-item" @click="go('/website')">导航网</a>
                <a class="nav-item" @click="go('/blog')">博客</a>
                <a class="nav-item">控制台</a>
            </div>
        </div>
        <div class="div-body">
            <el-aside>
                <el-menu :default-active="$route.path" class="el-menu-vertical-demo" :collapse="false" :router="true" :default-openeds="['1', '2']">
                    <el-sub-menu index="1">
                        <template #title><el-icon><Position /></el-icon><span>导航网</span></template>
                        <el-menu-item index="/console" class="gs2"><el-icon><Position /></el-icon>站点管理</el-menu-item>
                        <el-menu-item index="/console/webnav/label" class="gs2"><el-icon><Position /></el-icon>标签管理</el-menu-item>
                    </el-sub-menu>
                    <el-sub-menu index="2">
                        <template #title><el-icon><Memo /></el-icon><span>博客</span></template>
                        <el-menu-item index="/console/blog" class="gs2"><el-icon><Memo /></el-icon>文章管理</el-menu-item>
                        <el-menu-item index="/console/blog/file" class="gs2"><el-icon><Memo /></el-icon>附件管理</el-menu-item>
                    </el-sub-menu>
                    <el-menu-item index="/console/system"><el-icon><Monitor /></el-icon><span>系统资源</span></el-menu-item>
                </el-menu>
            </el-aside>
            <div id="bodyRef">
                <router-view></router-view>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
const go = (path: string) => {window.location.href = path}
</script>

<style scoped lang="less">
.container {
    width: 100%;
    height: 100%;
    position: absolute;
    user-select: none;
    top: 0;
    left: 0;
    display: flex;
    flex-direction: column;

    .nav {
        height: 35px;
        width: 100%;
        display: flex;
        justify-content: space-between;
        margin-top: 10px;

        .nav-left {
            width: auto;
            margin: auto 0;
            padding-left: 50px;

            img {
                height: 30px;
                cursor: pointer;
            }
        }

        .nav-list {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-right: 50px;

            .nav-item {
                margin-left: 20px;
                color: #fff;
                cursor: pointer;

                &:hover {
                    color: #8d8d8d;
                }
            }

            .nav-item:last-child {
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