<template>
    <div class="content">
        <div class="title">
            <el-input type="text" placeholder="请输入标题" v-model="title"/>
            <el-button round size="small" style="width: 10vw;" @click="submit">保存</el-button>
            <el-button round size="small" style="width: 10vw;" @click="goback">返回</el-button>
        </div>
        <div class="div-editor">
            <Toolbar id="toolbar" :editor="editorRef" :defaultConfig="defaultConfig" :mode="mode" />
            <Editor id="editor" v-model="content" :defaultConfig="editorConfig" :mode="mode" @onCreated="handleCreated" :style="editorStyle" />
        </div>
    </div>
</template>

<script setup lang="ts">
import { get_blog_single, updateblog } from "@/api/blog";
import { useRoute} from "vue-router";
import "@wangeditor/editor/dist/css/style.css";
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


const route = useRoute();
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
const edit_image_list:Ref<Set<string>> = ref(new Set()) 
const edit_video_list:Ref<Set<string>> = ref(new Set())

// 编辑器配置
const editorConfig: Partial<IEditorConfig> = {
    placeholder: '请输入内容...',
    readOnly: false,
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
            server: `${API_BASE_URL}/api/blog/uploadimg/`, // 上传接口 URL
            fieldName: "file", // 图片字段名称
            withCredentials: true,
            base64LimitSize: 5 * 1024, // 5kb
            allowedFileTypes: ['image/*'],
            headers: {
                Authorization: window.localStorage.getItem('token')
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
            server: `${API_BASE_URL}/api/blog/uploadother/`, // 上传接口 URL
            fieldName: "file", // 视频字段名称
            withCredentials: true,
            allowedFileTypes: ['video/*'],
            headers: {
                Authorization: window.localStorage.getItem('token')
            },
            onSuccess(file: File, res: any) {
                console.log(`${file.name} 上传成功`, res);
                const { url } = res.data || {}
                edit_video_list.value.add(url.split("/")[JSON.parse(res.data).url.split("/").length - 1]);
            },
            customInsert(res: any, insertFn: any) {
                const { url } = res.data || {}
                insertFn(url, url.split("/")[url.split("/").length - 1])
            }
        },
        uploadAttachment: {
            server: `${API_BASE_URL}/api/blog/uploadother/`,
            fieldName: "file",
            withCredentials: true,
            allowedFileTypes: ['*'],
            maxFileSize: 500 * 1024 * 1024, // 10M
            headers: {
                Authorization: window.localStorage.getItem('token')
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
                console.log(`插入附件`, file.name)
                insertFn(url.split("/")[url.split("/").length - 1], url)
            },
        },
        codeSelectLang: {
            codeLangs: [
                {
                    "text": "CSS",
                    "value": "css"
                },
                {
                    "text": "HTML",
                    "value": "html"
                },
                {
                    "text": "XML",
                    "value": "xml"
                },
                {
                    "text": "Javascript",
                    "value": "javascript"
                },
                {
                    "text": "Typescript",
                    "value": "typescript"
                },
                {
                    "text": "JSX",
                    "value": "jsx"
                },
                {
                    "text": "Go",
                    "value": "go"
                },
                {
                    "text": "PHP",
                    "value": "php"
                },
                {
                    "text": "C",
                    "value": "c"
                },
                {
                    "text": "Python",
                    "value": "python"
                },
                {
                    "text": "Java",
                    "value": "java"
                },
                {
                    "text": "C++",
                    "value": "cpp"
                },
                {
                    "text": "C#",
                    "value": "csharp"
                },
                {
                    "text": "Visual Basic",
                    "value": "visual-basic"
                },
                {
                    "text": "SQL",
                    "value": "sql"
                },
                {
                    "text": "Ruby",
                    "value": "ruby"
                },
                {
                    "text": "Swift",
                    "value": "swift"
                },
                {
                    "text": "Bash",
                    "value": "bash"
                },
                {
                    "text": "Lua",
                    "value": "lua"
                },
                {
                    "text": "Groovy",
                    "value": "groovy"
                },
                {
                    "text": "Markdown",
                    "value": "markdown"
                }
            ],
        }
    }
}
const goback = () => window.history.back()
onBeforeMount(()=> {
    Boot.registerModule(linkCardModule)
    Boot.registerModule(attachmentModule)
    Boot.registerModule(markdownModule)
    Boot.registerModule(formulaModule)
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

const submit = () => {
    if (title.value.trim() == ""){
        public_elmsg_warning("标题不能为空")
        return
    }
    if (editorRef.value.isEmpty()) {
        public_elmsg_warning("内容不能为空")
        return
    }
    if (editorRef.value.getText().length == 0) {
        public_elmsg_warning("请检查是否有空标题、空表格等")
        return
    }
    updateblog(id, title.value.trim(), editorRef.value.getHtml(), filelist()).then((res)=>{
        if (res.code == 0){
            public_elmsg_success("更新成功")
            setTimeout(() => {
                window.location.href = `/console/blog`
            }, 1000)
        }else public_elmsg_warning(res.msg)
    })
}
const filelist = () => {
    const filelist = [...editorRef.value.getElemsByType("image").map((item:any) => item.alt),
        ...editorRef.value.getElemsByType('video').map((item:any) => item.poster),
        ...editorRef.value.getElemsByType('attachment').map((item:any) => item.fileName)
    ]
    return filelist
}
window.addEventListener('load', () => {
    const toolbar:any = document.getElementById("toolbar")
    const windowHeight = window.innerHeight;
    if (toolbar) {
        const toolbarHeight = toolbar.offsetHeight;
        const newEditorHeight = windowHeight - toolbarHeight - 36;
        editorStyle.height = `${newEditorHeight}px`;
    }else {
        const newEditorHeight = windowHeight - 0 - 36;
        editorStyle.height = `${newEditorHeight}px`;
    }
})
window.addEventListener('resize', () => {
    const toolbar:any = document.getElementById("toolbar")
    const windowHeight = window.innerHeight;
    const toolbarHeight = toolbar.offsetHeight;
    const newEditorHeight = windowHeight - toolbarHeight - 36;
    editorStyle.height = `${newEditorHeight}px`;
});
</script>

<style scoped lang='less'>
.content {
    width: calc(100% - 1px);
    height: 100%;
    background-color: transparent;
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
        height: calc(100% - 35px);
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
.preview {
    width: 100vw;
    height: calc(100vh - 1px);
    .preview-body {
        width: 90%;
        height: 100vh;
        margin: 0 auto;
        .title {
            width: 100%;
            height: auto;
            word-wrap:break-word;
        }
        .main {
            width: 100%;
            height: auto;
            border-top: 1px dashed #ccc;
            margin-top: 10px;
            word-wrap:break-word;
        }
    }
}
</style>