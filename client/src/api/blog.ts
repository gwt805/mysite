import http from "@/utils/axios";

interface get_blog_single_rep {
    code: number,
    status: string,
    msg: string,
    data ?: {
        "title": string,
        "content": string
    }
}
export const get_blog_single = async (id: number):Promise<get_blog_single_rep> => {
    return await http.post('api/blog/getblog_single/', {id: id});
};

interface get_blog_all_rep {
    code: number,
    status: string,
    msg: string,
    data ?: {
        "id": number,
        "title": string,
        "content": string
        "created_at": string,
        "updated_at": string
    },
    count?: number
}
export const get_blog_all = async (currentPage: number, pageSize: number, search: string):Promise<get_blog_all_rep> => {
    return await http.post("api/blog/getblog/", {currentPage: currentPage, pageSize: pageSize, search: search});
};

interface blog_rep {
    code: number,
    status: string,
    msg: string
}
export const createblog = async (title: string, content: string, filelist: Array<string>):Promise<blog_rep> => {
    return await http.post("api/blog/create_blog/", {"title": title, "content": content, "filelist": filelist});
};

export const updateblog = async (id: number, title: string, content: string, filelist: Array<string>):Promise<blog_rep> => {
    return await http.post("api/blog/update_blog/", {id: id, title: title, content: content, filelist: filelist});
};

export const deleteblog = async (id: number):Promise<blog_rep> => {
    return await http.post("api/blog/delete_blog/", {id: id});
};

export const getfile = async (currentPage: number, pageSize: number) => {
    return await http.post("api/blog/getfile/", {currentPage: currentPage, pageSize: pageSize});
}
export const removefile = async () => {
    return await http.post("api/blog/removefile/");
};