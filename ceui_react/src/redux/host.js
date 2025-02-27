export const BASE_URL = 'http://192.168.1.9:8000';
export const API_URL = 'http://192.168.1.9:8000';
export const IMAGE_URL = 'http://127.0.0.1:8000'
export const MAIN_URL = 'http://127.0.0.1:8000'
export const SOCKET_URL = 'http://127.0.0.1:3000'
export const MEDIA_URL = 'http://127.0.0.1:8000/media/'


export const tokenConfig = getState => {
    const token = getState().User.token
    const csrf = getState().User.csrf
    const config = {
        headers: {
            'Content-Type': 'application/json',
            'X-Csrftoken':csrf,
            "Referer": BASE_URL,
        }
    }

    if (token) {
        config.headers['Authorization'] = `Token ${token}`
    }

    return config
}

export const getUserID = getState => {
    const id = getState().User.user.id

    return id
}

export const tokenConfigMultiPart = getState => {
    const token = getState().User.token
    const csrf = getState().User.csrf
    const config = {
        headers: {
            'accept':'application/json',
            'content-type': 'multipart/form-data',
            'X-Csrftoken':csrf,
            "Referer": BASE_URL,
        }
    }

    if (token) {
        config.headers['Authorization'] = `Token ${token}`
    }

    return config
}