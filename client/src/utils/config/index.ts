const ip = import.meta.env.BASE_IP;
const envhost = import.meta.env.VITE_API_BASE_URL;

export const API_URL = envhost || `http://${ip}:8080`;
export const API_BASE_URL = API_URL;