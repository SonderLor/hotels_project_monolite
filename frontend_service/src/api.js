import axios from 'axios';

const log = (message, data) => {
    console.log(`[API]: ${message}`, data || '');
};

const createAPI = (baseURL) => {
    const API = axios.create({
        baseURL,
        withCredentials: true,
    });

    API.interceptors.request.use(
        async (config) => {
            if (!config.headers['X-CSRFToken']) {
                const csrfToken = await getCSRFToken();
                config.headers['X-CSRFToken'] = csrfToken;
            }
            return config;
        },
        (error) => Promise.reject(error)
    );

    API.interceptors.response.use(
        (response) => {
            log(`Response received from ${baseURL}`, response.data);
            return response;
        },
        (error) => {
            log(`Response error from ${baseURL}`, error.response?.data || error);
            return Promise.reject(error);
        }
    );

    return API;
};

export const BackendAPI = createAPI('http://localhost/api/');

export const getCSRFToken = async () => {
    try {
        const response = await axios.get('http://localhost/api/auth/csrf/', {
            withCredentials: true,
        });
        return response.data.csrfToken;
    } catch (error) {
        console.error('Failed to fetch CSRF token', error);
        throw error;
    }
};

export const login = async (email, password) => {
    log('Attempting login', { email });
    const response = await BackendAPI.post('auth/login/', { email, password });
    log('Login successful');
    return response.data;
};

export const logout = async () => {
    log('Attempting logout');
    const response = await BackendAPI.post('auth/logout/');
    log('Logout successful');
    return response.data;
};

export const fetchCurrentUser = async () => {
    log('Fetching current user');
    const response = await BackendAPI.get('auth/users/me/');
    log('User fetched successfully');
    return response.data;
};
