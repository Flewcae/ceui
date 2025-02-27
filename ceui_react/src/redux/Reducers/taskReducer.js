import { GET_TASK, GET_TASKS, CREATE_TASK, REMOVE_TASK, UPDATE_TASK, LOADING_TASK } from '../types';



const initialState = {
    tasks: [],
    loading: false
};


const taskReducer = (state = initialState, action) => {
    switch (action.type) {
        case LOADING_TASK:
            return {
                ...state,
                loading: true,
            }
        case GET_TASKS:
            return {
                ...state,
                tasks: action.payload,
                loading: false,
            }
        case CREATE_TASK:
            return {
                ...state,
                tasks: [...state.tasks, action.payload],
                loading: false,
            }
        case UPDATE_TASK:
            const updatedTask = action.payload;
            const updatedTasks = state.tasks.map((_task) =>
                _task.id === updatedTask.id ? updatedTask : _task
            );
            return {
                ...state,
                tasks: updatedTasks,
                loading: false,
            };
        case REMOVE_TASK:
            const removedTaskId = action.payload;
            const remainingTasks = state.tasks.filter(
                (_task) => _task.id !== removedTaskId
            );
            return {
                ...state,
                tasks: remainingTasks,
                loading: false,
            };
        default:
            return state;
    }
};

export default taskReducer;
