<template>
    <div class="container">
        <div class="tools">
            <el-input v-model="search" placeholder="博客名字" autocomplete clearable @change="get_data"></el-input>
            <el-button type="info" round @click="go('/console/blog/add')">添加博客</el-button>
        </div>
        <div class="middle">
            <el-table :data="tableData" border style="width: 100%" height="800">
                <el-table-column prop="id" label="ID" align="center" width="150" />
                <el-table-column prop="title" label="标题" align="center" />
                <el-table-column prop="content" label="内容" align="center" show-overflow-tooltip />
                <el-table-column prop="created_at" label="创建时间" align="center" width="200" />
                <el-table-column prop="updated_at" label="更新时间" align="center" width="200" />
                <el-table-column fixed="right" label="操作" align="center" width="150">
                    <template #default="scope">
                        <el-button link type="primary" size="small"
                            @click.prevent="go(`/console/blog/edit/${scope.row.id}`)">编辑</el-button>
                        <el-popconfirm title="你确定要删除这份数据嘛" confirm-button-text="确定" cancel-button-text="取消"
                            @confirm="deleteRow(scope.row.id)">
                            <template #reference>
                                <el-button link type="danger" size="small" @click="">删除</el-button>
                            </template>
                        </el-popconfirm>
                    </template>
                </el-table-column>
            </el-table>
        </div>
        <div class="pagenum">
            <el-pagination v-model:current-page="currentPage" v-model:page-size="pageSize" :page-sizes="[20, 50]"
                :background="true" layout="total, sizes, prev, pager, next, jumper" :total="count" size="default"
                @size-change="handleSizeChange" @current-change="handleCurrentChange" />
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, type Ref, onMounted } from 'vue'
import { public_elmsg_error, public_elmsg_success } from '@/utils/elmsg';
import { get_blog_all, deleteblog } from "@/api/blog";

const currentPage = ref(1);
const pageSize = ref(20);
const count: Ref<number | any> = ref(0);
const search = ref('')
const tableData:any = ref([])

const get_data = () => {
    get_blog_all(currentPage.value, pageSize.value, search.value.trim()).then((res: any) => {
        tableData.value = res.data;
        count.value = res.count;
    })
}
const go = (url: string) => { window.location.href = url }

const handleCurrentChange = (val: number) => {
    currentPage.value = val;
    get_data();
}
const handleSizeChange = (val: number) => {
    pageSize.value = val;
    get_data();
}

const deleteRow = (index: number) => {
    deleteblog(index).then((res: any) => {
        if (res.code == 0) {
            public_elmsg_success(res.msg);
            get_data();
        } else {
            public_elmsg_error(res.msg);
        }
    })
}

onMounted(() => {
    get_data();
})
</script>

<style scoped lang="less">
.container {
    width: calc(100% - 200px);
    height: calc(100% - 50px);
    position: absolute;
    top: 50px;
    left: 200px;
    display: flex;
    flex-direction: column;

    .tools {
        width: 100%;
        display: flex;
        justify-content: space-between;

        .el-input {
            width: 430px;
        }
    }
}

.el-drawer:first-child {
    h3 {
        text-align: center;
        margin-bottom: 20px;
    }

    .el-button-group {
        width: 100%;

        .el-button {
            width: 50%;
        }
    }
}
</style>