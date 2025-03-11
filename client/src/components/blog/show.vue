<template>
    <div class="container">
        <div class="nav">
            <div class="nav-left"><img src="../../assets/logo.png" draggable="false" @click="$router.push('/index')"></div>
            <el-input v-model="search_input" placeholder="在此搜索" class="input-with-select" @change="get_data">
                <template #append><el-button :icon="Search" /></template>
            </el-input>
            <div class="nav-list">
                <a class="nav-item" @click="go('/website')">导航网</a>
                <a class="nav-item">博客</a>
                <a class="nav-item" @click="go('/console')">控制台</a>
            </div>
        </div>
        <div class="blog">
            <div v-if="pageData.length === 0" class="empty-data">
                <el-empty description="暂无数据" />
            </div>
            <div class="blog-item" v-for="item in pageData" :key="item.id">
                <div class="blog-title">
                    <h3 @click="goto('show', item.id)">{{ item.title }}</h3>
                </div>
                <div class="blog-content">
                    <p>{{ item.content }}</p>
                </div>
                <div class="blog-footer">
                    <span class="time-info">发布于 {{ formatDate(item.created_at) }} | 更新于 {{ formatDate(item.updated_at)
                        }}</span>
                </div>
            </div>
        </div>
        <div class="pagenum">
            <el-pagination v-model:current-page="currentPage" v-model:page-size="pageSize" :page-sizes="[5, 10, 20]" :background="true"
                layout="total, sizes, prev, pager, next, jumper"  :total="count" size="small"
                @size-change="handleSizeChange" @current-change="handleCurrentChange" />
        </div>
    </div>
</template>

<script setup lang="ts">
import { get_blog_all } from '@/api/blog';
import { ref, type Ref, onMounted } from 'vue';
import { Search } from '@element-plus/icons-vue';
import { public_elmsg_error } from '@/utils/elmsg';

const search_input = ref("");
const currentPage = ref(1);
const pageSize = ref(5);
const count: Ref<number | any> = ref(0);
const pageData: Ref<Map<string, string> | any> = ref([]);
const loading = ref(false);

const handleSizeChange = (val: number) => {
    pageSize.value = val;
    get_data();
};

const handleCurrentChange = (val: number) => {
    currentPage.value = val;
    get_data();
}

const formatDate = (dateString: string) => {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    });
}

const get_data = () => {
    loading.value = true;
    try {
        get_blog_all(currentPage.value, pageSize.value, search_input.value.trim()).then((res)=> {
            if (res.code == 0) {
                count.value = res.count || 0;
                pageData.value = res.data || [];
            } else {
                public_elmsg_error(res.msg);
            }
        });
    } catch (error) {
        public_elmsg_error('获取数据失败');
    } finally {
        loading.value = false;
    }
}
const go = (url: string) => { window.location.href = url;}
const goto = (path: string, id: number) => {
    if (path == "show") window.location.href = `/blog/preview/${id}`;
    else if (path == "create") window.location.href = `/page/create`;
}

onMounted(() => {
    get_data();
});
</script>

<style scoped lang="less">
.container {
    height: 100%;
    width: 100%;
    position: absolute;

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

        .el-input {
            width: 50%;
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
            .nav-item:nth-child(2) {
                color: #8d8d8d;
            }
        }
    }

    .blog {
        height: calc(100% - 120px);
        width: 100%;
        // margin-top: 10px;
        overflow: auto;

        .empty-data {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 200px;
        }

        .blog-item {
            height: auto;
            width: 90%;
            margin: 15px auto;
            padding: 15px;
            border-top: 1px dashed #ccc;
            transition: all 0.3s;

            &:hover {
                box-shadow: 5px 5px 15px 15px rgba(255, 255, 255, 0.1);
                transform: translateY(-2px);
                border: none;
            }

            .blog-title {
                height: auto;
                line-height: 40px;
                width: 100%;

                h3 {
                    cursor: pointer;
                    color: #9d7bd1;
                    margin: 0;
                    display: inline;

                    &:hover {
                        color: #41ABF1;
                    }
                }
            }

            .blog-content {
                height: auto;
                max-height: 100px;
                width: 100%;
                overflow: hidden;
                line-height: 1.8rem;
                color: #666;
                margin: 10px 0;

                p {
                    margin: 0;
                }
            }

            .blog-footer {
                height: auto;
                width: 100%;
                line-height: 35px;
                color: #999;

                .time-info {
                    font-size: 0.9rem;
                }
            }
        }
    }

    .pagenum {
        color: red;
        width: 90%;
        margin: 20px auto;
        display: flex;
        justify-content: center;
    }
}
</style>