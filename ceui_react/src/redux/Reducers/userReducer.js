import { setAuthToken, setCsrfToken } from '../taskApiRoot';
import {
    REGISTER_SUCCESS,
    REGISTER_FAIL,
    LOGIN_SUCCESS,
    LOGIN_FAIL,
    LOGOUT,
    GET_USER,
    UPDATE_USER,
    AUTH_ERROR,
    CSRF,
    GET_PERMISSION_MAP,
    LOGIN_LOADING,
    LOADING_COMPLETE
} from '../types';
import AsyncStorage from '@react-native-async-storage/async-storage';



const saveToken = async (token) => {
    try {
        console.log('yazıyorm sotragea');
        await AsyncStorage.setItem('token', token);
        console.log('yazdım', token);
        setAuthToken(token);
    } catch (err) {
    }
};

const removeToken = async () => {
    try {
        await AsyncStorage.removeItem('token');
    } catch (err) {
    }
};

const initialState = {
    token: null,
    isAuthenticated: false,
    loading: false,
    user: null,
    csrf: null,
    permissions:null,
};

const authReducer = (state = initialState, action) => {
    switch (action.type) {
        case LOGIN_LOADING:
            return {
                ...state,
                loading: true
            }
        case LOADING_COMPLETE:
            return {
                ...state,
                loading: false
            }
        case CSRF:
            setCsrfToken(action.payload)
            return {
                ...state,
                csrf: action.payload
            }
        case REGISTER_SUCCESS:
        case LOGIN_SUCCESS:
            saveToken(action.payload.token)
            return {
                ...state,
                user:action.payload.user,
                permissions: action.payload.permissions,
                token: action.payload.token,
                isAuthenticated: true,
                loading: false,
            };
        case GET_PERMISSION_MAP:
            return {
                ...state,
                permissions:action.payload
            }
        case GET_USER:
            return {
                ...state,
                user: action.payload.user,
                permissions: action.payload.permissions,
                token:action.payload.token,
                loading: false,
            };
        case UPDATE_USER:
            return {
                ...state,
                user: action.payload,
                loading: false,
            };
        case REGISTER_FAIL:
        case LOGIN_FAIL:
        case LOGOUT:
        case AUTH_ERROR:
            removeToken()
            return {
                ...state,
                token: null,
                isAuthenticated: false,
                loading: false,
                user: null,
            };
        default:
            return state;
    }
};

export default authReducer;
