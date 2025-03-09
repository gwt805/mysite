export const userinfo:any = () => {
    const user:any = localStorage.getItem("userinfo");
    return user ? JSON.parse(user) : {"id": "", "username": "", "avatar": null, "is_admin": false, "token": "", "create_at": "", "update_at": ""};
};

export const setuseravatar = (avatar: string) => {
    const user:any = userinfo();
    user.avatar = avatar;
    localStorage.setItem("userinfo", JSON.stringify(user));
}