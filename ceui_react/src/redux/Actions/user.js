import axios from 'axios';
import {
  REGISTER_FAIL,
  REGISTER_SUCCESS,
  LOGIN_FAIL,
  LOGIN_SUCCESS,
  SET_MENU_ITEMS,
  LOGOUT,
  GET_USER,
  UPDATE_USER,
  AUTH_ERROR,
  CSRF,
  LOGIN_LOADING,
  LOADING_COMPLETE,
} from '../types'
import { API_URL, MAIN_URL, tokenConfig, tokenConfigMultiPart } from '../host'
import AsyncStorage from '@react-native-async-storage/async-storage';
import { setAuthToken } from '../taskApiRoot';


export const getUsers = (e = () => { }) => async (dispatch, getState) => {
  try {
    const response = await axios.get(API_URL + '/users/', tokenConfig(getState));
    e(response.data)
  } catch (error) {

  }
};

export const getAnyUser = (id, e = () => { }) => async (dispatch, getState) => {
  try {
    const response = await axios.get(API_URL + '/users/detail/' + id, tokenConfig(getState));
    e(true, response.data)
  } catch (error) {

  }
};

export const getGroupNames = (e = () => { }) => async (dispatch, getState) => {
  try {
    const response = await axios.get(API_URL + '/users/core/groups/?name_list=true', tokenConfig(getState));

    if (response.status === 200) {
      e(true, response.data)
    } {
      e(false, response.data.error)
    }

  } catch (error) {

  }
};


export const search = (text, e = () => { }) => async (dispatch, getState) => {

  let config = tokenConfig(getState)
  try {
    const response = await axios.get(API_URL + '/users/?search=' + text, config);
    e(response.data)
  } catch (error) {
    e(error)
  }
}

export const register = (userData) => async (dispatch) => {
  try {
    dispatch({
      type: LOGIN_LOADING,
    });
    const response = await axios.post(API_URL + '/users/register/', userData);
    dispatch({
      type: REGISTER_SUCCESS,
      payload: response.data,
    });
  } catch (error) {
    dispatch({
      type: REGISTER_FAIL,
    });
  }
};

export const login = (credentials, e = () => { }) => async (dispatch, getState) => {
  try {
    let config = tokenConfig(getState);
    dispatch({
      type: LOGIN_LOADING,
    });

    const response = await axios.post(API_URL + '/api/user/login/', credentials, config);

    console.log('login successful', response.data);

    try {
      await AsyncStorage.setItem('token', response.data.token);
  } catch (err) {
    console.log('ayzmadı amk evladı', err);
    
  }
    

    dispatch({
      type: LOGIN_SUCCESS,
      payload: response.data,
    });


  } catch (error) {
    console.log('errors', error);
  }
};

export const logout = () => async (dispatch, getState) => {
  const config = tokenConfig(getState)
  dispatch({ type: LOGOUT });

  const response = await axios.post(API_URL + '/users/logout/', null, config);

  const responseCSRF = await axios.get(API_URL + '/users/csrf/');
  dispatch({
    type: CSRF,
    payload: responseCSRF.data.csrf,
  });

};

export const getUser = (token, e = () => { }) => async (dispatch, getState) => {
  try {
    dispatch({
      type: LOGIN_LOADING,
    });
    let config = tokenConfig(getState)

    if (token) {
      config.headers['Authorization'] = `Token ${token}`
    }
    const response = await axios.get(API_URL + '/api/user/users/me', config);
    dispatch({
      type: GET_USER,
      payload: response.data,
    });
    e(true)
    console.log('perms', response.data);
    
    setAuthToken(token);

  } catch (error) {
    dispatch({
      type: AUTH_ERROR,
    });
    e(false)
  }
};

export const getCSRF = () => async (dispatch) => {
  console.log("here");
  
  try {
    console.log("here1");
    const response = await axios.get(API_URL + '/api/user/users/csrf/');
    console.log('csrf', response.data.csrf);
    dispatch({
      type: CSRF,
      payload: response.data.csrf,
    });
    


  } catch (error) {
    console.log('error', error);
  }
};

export const updateUser = (userData, e = () => { }) => async (dispatch, getState) => {
  dispatch({
    type: LOGIN_LOADING,
  });
  const config = tokenConfigMultiPart(getState)



  try {
    const response = await axios.post(API_URL + '/users/update_user/', userData, config);
    dispatch({
      type: UPDATE_USER,
      payload: response.data,
    });

    e(true, response.data)


  } catch (error) {
    dispatch({
      type: AUTH_ERROR,
    });
    e(false, error)
  }
};









export const createUser = (userData, e = () => { }) => (dispatch, getState) => {
  try {
    let config = tokenConfigMultiPart(getState)
    const response = axios.post(API_URL + "/users/create-custom-user/", userData, config);
    if (response.status === 201) {
      e(true, response.data)
    } else {
      e(false, response.data.error)
    }
  } catch (error) {
    e(false, error)


  }
};

export const removeUser = (userId, e = () => { }) => async (dispatch, getState) => {
  try {
    let config = tokenConfigMultiPart(getState)
    const response = await axios.delete(API_URL + "/users/delete-user/" + userId + "/", config);
    if (response.status === 200) {
      e(true, response.data)
    } else {
      e(false, response.data.error)
    }
  } catch (error) {
    e(false, error)


  }
};

export const postNotificationToken =
  (credentials, e) =>
    async (dispatch, getState) => {
      try {
        let config = tokenConfig(getState)


        const response = await axios.post(
          API_URL + "/users/notification/",
          credentials,
          config,
        );

        if (response.data.success) {

        } else {

        }

        e(true);
      } catch (error) {

        e(false);
      }
    };

export const changePassword = (userData, e = () => { }) => async (dispatch, getState) => {
  dispatch({
    type: LOGIN_LOADING,
  });
  const config = tokenConfigMultiPart(getState)
  
  try {
    const response = await axios.post(API_URL + '/users/change_password/', userData, config);
    
    if (response.status === 200) {
      dispatch({
        type: LOGOUT,
      });
      e(true, response.data.message)

    } else {
      e(false, response.data.message)
    }

  } catch (error) {
    dispatch({
      type: AUTH_ERROR,
    });
    e(false, error)
  }
};

export const resetPassword = (userData, e = () => { }) => async (dispatch, getState) => {
  const config = tokenConfigMultiPart(getState)
  
  try {
    const response = await axios.post(API_URL + '/users/password-reset-request/', userData, config);
    
    if (response.status === 200) {
      e(true, response.data.message)

    } else {
      e(false, response.data.message)
    }

  } catch (error) {
    
    e(false, error)
  }
};

