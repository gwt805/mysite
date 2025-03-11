import axios from "axios";
import router from "@/routes/index";
import { API_BASE_URL } from "@/utils/config/index";

const http = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        AUTHORIZATION: window.localStorage.getItem("token"),
    },
});

http.interceptors.response.use(
    (res) => {
        if (res.data.code == -2) {
            window.localStorage.clear();
            router.push(`/login?redirect=${router.currentRoute.value.fullPath}`)
            // window.location.href = `/login?redirect=${router.currentRoute.value.fullPath}`;
        } else return res.data;
    },
    (error) => {
        return Promise.reject(error);
    }
);

export default http;
