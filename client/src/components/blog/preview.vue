<template>
    <div class="content">
        <div class="search">
            <img src="/logo.png" draggable="false" @click="$router.push('/index')">
            <div class="nav-list">
                <a class="nav-item" @click="go('/website')">导航网</a>
                <a class="nav-item" @click="go('/blog')">博客</a>
                <a class="nav-item" @click="go('/console')">控制台</a>
            </div>
        </div>
        <div class="title">
            <h1>{{ title }}</h1>
        </div>
        <div class="div-editor">
            <Toolbar id="toolbar" :editor="editorRef" :defaultConfig="defaultConfig" :mode="mode" v-if="false" />
            <Editor id="editor" v-model="content" :defaultConfig="editorConfig" :mode="mode" @onCreated="handleCreated" :style="editorStyle" />
        </div>
    </div>
</template>

<script setup lang="ts">
import { get_blog_single } from "@/api/blog";
import { useRoute} from "vue-router";
import "@wangeditor/editor/dist/css/style.css";
import { userinfo } from '@/utils/session/index'
import { API_BASE_URL } from '@/utils/config/index'
import { Boot } from '@wangeditor/editor'
import linkCardModule from '@wangeditor/plugin-link-card'
import markdownModule from '@wangeditor/plugin-md'
import attachmentModule from '@wangeditor/plugin-upload-attachment'
import { type IEditorConfig } from '@wangeditor/editor'
import { Editor, Toolbar } from "@wangeditor/editor-for-vue";
import formulaModule from '@wangeditor/plugin-formula'
import { ref, type Ref, reactive, shallowRef, onBeforeUnmount, onBeforeMount, onMounted} from 'vue'
import { public_elmsg_error, public_elmsg_success, public_elmsg_warning } from "@/utils/elmsg";
import router from "@/routes/index";

const route = useRoute();
// const type:any = route.params.type
const id:any = route.params.id

const title:Ref<string|any> = ref('')
const content:Ref<string|any> = ref('');

const editorStyle = reactive({height: '300px'})
const mode = "default"
const defaultConfig = {
    insertKeys: {
        index: 0, // 自定义插入的位置
        keys: ['uploadAttachment', 'insertFormula'], // “上传附件”菜单
    }
}
const editorRef = shallowRef() // 编辑器实例，必须用 shallowRef
const readOnly:any = true
const edit_image_list:Ref<Set<string>> = ref(new Set()) 
const edit_video_list:Ref<Set<string>> = ref(new Set())

// 编辑器配置
const editorConfig: Partial<IEditorConfig> = {
    placeholder: '请输入内容...',
    readOnly: readOnly,
    hoverbarKeys: {
        attachment: {
            menuKeys: ['downloadAttachment'], // “下载附件”菜单
        },
        formula: {
            menuKeys: ['editFormula'], // “编辑公式”菜单
        },
    },
    MENU_CONF: {
        viewLink: {
            getLinkCardData(linkUrl: string) {
                console.log(`获取链接卡片数据: ${linkUrl}`)
            }
        },
        uploadImage: {
            server: `${API_BASE_URL}/file/uploadimg`, // 上传接口 URL
            fieldName: "file", // 图片字段名称
            withCredentials: true,
            allowedFileTypes: ['image/*'],
            headers: {
                Authorization: userinfo().token
            },
            onSuccess(file: File, res: any) {
                console.log(`${file.name} 上传成功`, res)
            }
        },
        insertImage: {
            onInsertedImage(imageNode:any){
                if (imageNode == null) return
                const { src, alt, url, href} = imageNode
                edit_image_list.value.add(src)
                console.log(`插入图片`, src, alt, url, href)
            }
        },
        editImage: {
            onUpdatedImage(imageNode:any){
                if (imageNode == null) return
                const { src, alt, url, href} = imageNode
                console.log(`更新图片`, src, alt, url, href)
            }
        },
        uploadVideo: {
            server: `${API_BASE_URL}/file/uploadfile`, // 上传接口 URL
            fieldName: "file", // 视频字段名称
            withCredentials: true,
            allowedFileTypes: ['video/*'],
            headers: {
                Authorization: userinfo().token
            },
            onSuccess(file: File, res: any) {
                console.log(`${file.name} 上传成功`, res);
                const { url } = res.data || {}
                edit_video_list.value.add(url.split("/")[JSON.parse(res.data).url.split("/").length - 1]);
            },
            customInsert(res: any, insertFn: any) {
                const { url } = res.data || {}
                insertFn(url, "")
            }
        },
        uploadAttachment: {
            server: `${API_BASE_URL}/file/uploadfile`,
            fieldName: "file",
            withCredentials: true,
            allowedFileTypes: ['*'],
            maxFileSize: 500 * 1024 * 1024, // 10M
            headers: {
                Authorization: userinfo().token
            },
            onSuccess(file: File, res: any) {
                public_elmsg_success(`${file.name} 上传成功`)
                console.log(`${file.name} 上传成功`, file, res);
            },
            onFailed(file: File, res: any) {
                public_elmsg_error(res.message)
                console.log('onFailed', file, res)
            },
            onError(file: File, err: Error, res: any) {
                public_elmsg_error(err.message)
                console.error('onError', file, err, res)
            },
            customInsert(res: any, file: File, insertFn: Function) {
                console.log('customInsert', res)
                const { url } = res.data || {}
                if (!url) throw new Error(`url is empty`)
                insertFn(`customInsert-${file.name}`, url)
            },
        }
    }
}

onBeforeMount(()=> {
    Boot.registerModule(linkCardModule)
    Boot.registerModule(attachmentModule)
    Boot.registerModule(markdownModule)
    Boot.registerModule(formulaModule)
    // if (["show", "edit"].indexOf(type) < 0) router.push({name: "empty"})
})
onMounted(() => {
    get_blog_single(id).then((res)=>{
        if (res.code == 0){
            content.value = res.data?.content
            title.value = res.data?.title
        }else public_elmsg_warning(res.msg)
    })
})
// 组件销毁时，也及时销毁编辑器
onBeforeUnmount(() => {
    const editor = editorRef.value
    if (editor == null) return
    editor.destroy()
})

const handleCreated = (editor:any) => {editorRef.value = editor}
const go = (url: string) => { router.push(url) }//window.location.href = url;}
window.addEventListener('load', () => {
    const toolbar:any = document.getElementById("toolbar")
    const windowHeight = window.innerHeight;
    if (toolbar) {
        const toolbarHeight = toolbar.offsetHeight;
        const newEditorHeight = windowHeight - toolbarHeight - 76;
        editorStyle.height = `${newEditorHeight}px`;
    }else {
        const newEditorHeight = windowHeight - 0 - 76;
        editorStyle.height = `${newEditorHeight}px`;
    }
})
window.addEventListener('resize', () => {
    const toolbar:any = document.getElementById("toolbar")
    const windowHeight = window.innerHeight;
    const toolbarHeight = toolbar.offsetHeight;
    const newEditorHeight = windowHeight - toolbarHeight - 76;
    editorStyle.height = `${newEditorHeight}px`;
});
</script>

<style scoped lang='less'>

.content {
    width: calc(100% - 1px);
    height: 100%;
    background-color: transparent;

    .search {
        width: 90%;
        height: 30px;
        margin: 0 auto;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        justify-content:space-between;
        img {
            width: 30px;
            margin-top: 10px;
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
            .nav-item:nth-child(2) {
                color: #8d8d8d;
            }
        }
    }
    .title {
        height: 35px;
        display: flex;
        justify-content: space-around;
        align-items: center;
        h1,.el-input {
            width: 100%;
            height: 35px;
            border: none;
            background-color: transparent;
            border-right: 1px solid #ccc;
            font-size: larger;
            text-indent: 1em;
            line-height: 34px;
        }
        .el-input {
        background-color: transparent !important;
        }
        
        .el-button {
            margin-left: 10px;
        }
    }
    .title::v-deep .el-input {
        background-color: transparent !important;
    }
    .div-editor {
        height: calc(100% - 65px) !important;
        width: 100%;
        z-index: 1;
        #toolbar {
            border-top: 1px solid #ccc;
        }
        #editor {
            border-top: 1px solid #ccc;
            overflow: auto;
            width: 100%;
        }
    }
}
</style>