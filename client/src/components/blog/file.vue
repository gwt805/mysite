<template>
    <div class="container">
        <div class="tools">
            <el-button type="info" round @click="deleteRow">删除冗余附件</el-button>
        </div>
        <div class="middle">
            <el-table :data="tableData" border style="width: 100%" height="800">
                <el-table-column prop="id" label="ID" align="center" width="150" />
                <el-table-column prop="bid" label="博客ID" align="center" width="150" />
                <el-table-column prop="file" label="附件列表" align="center" show-overflow-tooltip />
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
import { getfile, removefile } from "@/api/blog";

const currentPage = ref(1);
const pageSize = ref(20);
const count: Ref<number | any> = ref(0);
const tableData: any = ref([])

const get_data = () => {
    getfile(currentPage.value, pageSize.value).then((res: any) => {
        tableData.value = res.data;
        count.value = res.count;
    })
}

const handleCurrentChange = (val: number) => {
    currentPage.value = val;
    get_data();
}
const handleSizeChange = (val: number) => {
    pageSize.value = val;
    get_data();
}

const deleteRow = () => {
    removefile().then((res: any) => {
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
        justify-content: end;

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