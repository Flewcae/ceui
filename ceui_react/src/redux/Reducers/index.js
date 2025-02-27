import { combineReducers } from '@reduxjs/toolkit';
import taskReducer from '../Actions/task';
import authReducer from './userReducer';



const rootReducer = combineReducers({
  User: authReducer,
  tasks: taskReducer,
});

export default rootReducer;
