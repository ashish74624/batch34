export const getCsrfToken = async () => {
    const response = await fetch("http://127.0.0.1:8000/api/csrf/", {
        credentials: "include",
    });
    const data = await response.json();
    return data.csrfToken;
};