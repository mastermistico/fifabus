export const xhr = (
    method: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'OPTIONS' = 'GET',
    url: string,
    headers: { [key: string]: any },
    body = null,
    files: File[] = []
): Promise<any> => {
    return new Promise((resolve, reject) => {
        const formData: FormData = new FormData();
        const params = body !== null ? body : {};
        for (let i = 0; i < files.length; i++) {
            formData.append('files'+i, files[i], files[i].name);
        }
        Object.keys(params).forEach(key => formData.append(key, params[key]));
        const req = new XMLHttpRequest();
        req.onreadystatechange = () => {
            if (req.readyState === 4) {
                if (req.status >= 200 && req.status <= 299) {
                    resolve(JSON.parse(req.response));
                } else {
                    reject(req.response);
                }
            }
        };
        req.onerror = () => reject(null);
        req.onabort = () => reject(null);
        req.open(method, url, true);
        Object.keys(headers).forEach(key => req.setRequestHeader(key, headers[key]));
        req.send(formData);
    });
};