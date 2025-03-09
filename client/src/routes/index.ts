import { type RouteRecordRaw, createRouter, createWebHistory } from "vue-router"
import auth from "@/components/auth.vue"
import index from "@/components/index.vue"
import website from "@/components/website/website.vue"
import blog_show from "@/components/blog/show.vue"
import blog_preview from "@/components/blog/preview.vue"
import console_show from "@/components/console/show.vue"
import console_webnav from "@/components/console/cwebsite.vue"
import console_webnav_label from "@/components/console/cwebsitelabel.vue"
import console_blog from "@/components/console/cblog.vue"
import console_blog_add from "@/components/blog/add.vue"
import console_blog_edit from "@/components/blog/edit.vue"
import console_blog_file from "@/components/blog/file.vue"
import connsole_system from "@/components/console/system.vue"
import empty from "@/components/empty.vue"

const routes: RouteRecordRaw[] = [
    {
        path: "/",
        redirect: "/index",
    },
    {
        path: "/login",
        name: "login",
        component: auth, 
    },
    {
        path: "/index",
        name: "index",
        component: index,
    },
    {
        path: "/website",
        name: "website",
        component: website, 
    },
    {
        path: "/blog",
        name: "blog_show",
        component: blog_show,
    },
    {
        path: "/blog/preview/:id",
        name: "blog_preview",
        component: blog_preview, 
    },
    {
        path: "/console",
        name: "console_show",
        component: console_show,
        children: [
            {
                path: "",
                name: "console_webnav",
                component: console_webnav,
            },
            {
                path: "webnav/label",
                name: "console_webnav_label",
                component: console_webnav_label,
            },
            {
                path: "blog",
                name: "console_blog",
                component: console_blog,
            },
            {
                path: "blog/file",
                name: "console_blog_file",
                component: console_blog_file,
            },
            {
                path: "system",
                name: "console_system",
                component: connsole_system,
            }
        ]
    },
    {
        path: '/console/blog/add',
        name: 'blog-add',
        component: console_blog_add
    },
    {
        path: '/console/blog/edit/:id',
        name: 'blog-update',
        component: console_blog_edit
    },
    { path: "/:pathMatch(.*)*", name: "NotFound", component: empty },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router