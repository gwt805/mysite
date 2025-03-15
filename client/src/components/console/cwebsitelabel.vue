<template>
    <div class="container">
        <div class="tools">
            <el-input v-model="search" placeholder="标签名字" autocomplete clearable @change="get_data"></el-input>
            <el-button type="info" round @click="openaddmodel">添加标签</el-button>
        </div>
        <div class="middle">
            <el-table :data="tableData" border style="width: 100%" height="800">
                <el-table-column prop="id" label="ID" align="center" />
                <el-table-column prop="tag" label="标签" align="center" />
                <el-table-column fixed="right" label="操作" align="center" width="150">
                    <template #default="scope">
                        <el-button link type="primary" size="small"
                            @click.prevent="openupdmodel(scope.row.id)">编辑</el-button>
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
    <el-drawer v-model="addmodel" title="添加站点" :with-header="false">
        <h3>添加标签</h3>
        <el-form ref="ruleFormRef" style="max-width: 600px" :model="add_formdata" label-position="top"
            label-width="auto" class="demo-ruleForm" size="default" status-icon>
            <el-form-item label="标签名字" prop="tag" required>
                <el-input v-model="add_formdata.tag" clearable />
            </el-form-item>
        </el-form>
        <el-button-group class="btn-group">
            <el-button type="info" @click="addmodel = false">取消</el-button>
            <el-button type="primary" @click="addRow">提交</el-button>
        </el-button-group>
    </el-drawer>
    <el-drawer v-model="updmodel" title="修改站点" :with-header="false">
        <h3>修改站点</h3>
        <el-form ref="ruleFormRef" style="max-width: 600px" :model="upd_formdata" label-position="top"
            label-width="auto" class="demo-ruleForm" size="default" status-icon>
            <el-form-item label="ID" prop="id" required>
                <el-input type="number" v-model="upd_formdata.id" disabled />
            </el-form-item>
            <el-form-item label="标签名字" prop="tag" required>
                <el-input v-model="upd_formdata.tag" clearable />
            </el-form-item>
        </el-form>
        <el-button-group class="btn-group">
            <el-button type="info" @click="updmodel = false">取消</el-button>
            <el-button type="primary" @click="editRow">提交</el-button>
        </el-button-group>
    </el-drawer>
</template>

<script setup lang="ts">
import { ref, type Ref, onMounted } from 'vue'
import { public_elmsg_error, public_elmsg_success } from '@/utils/elmsg';
import { getlabel, webnavlabel_get_single, webnavlabel_upd_single, webnavlabel_del_single, webnavlabel_add } from "@/api/website";

const currentPage = ref(1);
const pageSize = ref(20);
const count: Ref<number | any> = ref(0);
const search = ref('')
const tableData:any = ref([])
const addmodel = ref(false)
const updmodel = ref(false)

const add_formdata = ref({ 'tag': '' })
const upd_formdata = ref({ 'id': 0, 'tag': '' })

const openaddmodel = () => {
    addmodel.value = true;
    add_formdata.value = { 'tag': '' }
}
const openupdmodel = (id: number) => {
    updmodel.value = true;
    upd_formdata.value = { 'id': 0, 'tag': '' }
    webnavlabel_get_single(id).then((res: any) => {
        if (res.code == 0) {
            upd_formdata.value = res.data;
        } else {
            public_elmsg_error(res.msg);
        }
    }).catch((err: any) => {
        public_elmsg_error("获取数据失败");
    })
}
const get_data = () => {
    getlabel('label', search.value.trim(), currentPage.value, pageSize.value).then((res: any) => {
        tableData.value = res.data;
        count.value = res.count;
    }).catch((err: any) => {
        public_elmsg_error("获取数据失败");
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
const editRow = () => {
    webnavlabel_upd_single(upd_formdata.value.id, upd_formdata.value.tag.trim()).then((res: any) => {
        if (res.code == 0) {
            public_elmsg_success(res.msg);
            updmodel.value = false;
            get_data();
        } else {
            public_elmsg_error(res.msg);
        }
    }).catch((err: any) => {
        public_elmsg_error("更新数据失败");
    })
}
const deleteRow = (index: number) => {
    webnavlabel_del_single(index).then((res: any) => {
        if (res.code == 0) {
            public_elmsg_success(res.msg);
            get_data();
        } else {
            public_elmsg_error(res.msg);
        }
    }).catch((err: any) => {
        public_elmsg_error("删除数据失败");
    })
}
const addRow = () => {
    webnavlabel_add(add_formdata.value.tag.trim()).then((res: any) => {
        if (res.code == 0) {
            public_elmsg_success(res.msg);
            addmodel.value = false;
            get_data();
        } else {
            public_elmsg_error(res.msg);
        }
    }).catch((err: any) => {
        public_elmsg_error("添加数据失败");
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