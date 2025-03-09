import http from "@/utils/axios/index";

export const getlabel = async (type: string, search: string, currentPage: number, pageSize: number) => {
    return await http.post("/webnavlabel_get/", { type: type, search: search, currentPage: currentPage, pageSize: pageSize });
}

export const webnavlabel_get_single = async (id: number) => {
    return await http.post("/webnavlabel/webnavlabel_get_single/", { id: id });
}
export const webnavlabel_upd_single = async (id: number, tag: string) => {
    return await http.post("/webnavlabel/webnavlabel_upd_single/", { id: id, tag: tag });
}
export const webnavlabel_del_single = async (id: number) => {
    return await http.post("/webnavlabel/webnavlabel_del_single/", { id: id });
}
export const webnavlabel_add = async (tag: string) => {
    return await http.post("/webnavlabel/webnavlabel_add/", { tag: tag });
}

// ---------------------------------------------------------------------------

export const getdata = async (search: string) => {
    return await http.post("/webnav/", { search: search });
};

export const cgetdata = async (search: string, currentPage: number, pageSize: number) => {
    return await http.post("/cwebnav/", { search: search, currentPage: currentPage, pageSize: pageSize });
};

export const cwebsite_add = async (name: string, weburl: string, imgurl: string, tooltip: string, tag: string) => {
    return await http.post("/cwebnav/cwebnav_add/", { name: name, weburl: weburl, imgurl: imgurl, tooltip: tooltip, tag: tag });
}

export const cwebnav_get_single = async (id: number) => {
    return await http.post("/cwebnav/cwebnav_get_single/", { id: id });
}

export const cwebnav_upd_single = async (id: number, name: string, weburl: string, imgurl: string, tooltip: string, tag: string) => {
    return await http.post("/cwebnav/cwebnav_upd_single/", { id: id, name: name, weburl: weburl, imgurl: imgurl, tooltip: tooltip, tag: tag });
}
export const cwebnav_del_single = async (id: number) => {
    return await http.post("/cwebnav/cwebnav_del_single/", { id: id });
}