import http from "@/utils/axios";

interface login_rep {
    code: number,
    status: string,
    msg: string,
    token: string
}
export const login = async (username: string, password: string):Promise<login_rep> => {
    return await http.post("/api/auth/login/", {username: username, password: password});
};
