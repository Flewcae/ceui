import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import api from '../taskApiRoot';

// 📌 1. Tüm Görevleri Getir
export const fetchTasks = createAsyncThunk('tasks/fetchTasks', async (_, { rejectWithValue }) => {
  try {
    const response = await api.get('/tasks/');
    return response.data;
  } catch (error) {
    return rejectWithValue(error.response.data);
  }
});

// 📌 2. Yeni Görev Ekle
export const createTask = createAsyncThunk('tasks/createTask', async (taskData, { rejectWithValue }) => {
  try {
    const response = await api.post('/', taskData);
    return response.data;
  } catch (error) {
    return rejectWithValue(error.response.data);
  }
});

// 📌 3. Görev Güncelleme
export const updateTask = createAsyncThunk('tasks/updateTask', async ({ id, updatedData }, { rejectWithValue }) => {
  try {
    const response = await api.put(`/${id}/`, updatedData);
    return response.data;
  } catch (error) {
    return rejectWithValue(error.response.data);
  }
});

// 📌 4. Görev Silme
export const deleteTask = createAsyncThunk('tasks/deleteTask', async (id, { rejectWithValue }) => {
  try {
    await api.delete(`/${id}/`);
    return id;
  } catch (error) {
    return rejectWithValue(error.response.data);
  }
});

// 📌 5. Görev Durum Güncelleme
export const updateTaskStatus = createAsyncThunk('tasks/updateStatus', async ({ id, status }, { rejectWithValue }) => {
  try {
    const response = await api.patch(`/${id}/update_status/`, { status });
    return response.data;
  } catch (error) {
    return rejectWithValue(error.response.data);
  }
});

// 📌 6. Revize Ekle
export const addRevise = createAsyncThunk('tasks/addRevise', async ({ id, reviseData }, { rejectWithValue }) => {
  try {
    const response = await api.post(`/${id}/add_revise/`, reviseData);
    return response.data;
  } catch (error) {
    return rejectWithValue(error.response.data);
  }
});

// 📌 7. Revize Güncelle
export const updateRevise = createAsyncThunk('tasks/updateRevise', async ({ id, reviseData }, { rejectWithValue }) => {
  try {
    const response = await api.patch(`/${id}/update_revise/`, reviseData);
    return response.data;
  } catch (error) {
    return rejectWithValue(error.response.data);
  }
});

// 📌 8. Revize Sil
export const deleteRevise = createAsyncThunk('tasks/deleteRevise', async ({ id, reviseId }, { rejectWithValue }) => {
  try {
    await api.delete(`/${id}/delete_revise/`, { data: { revise_id: reviseId } });
    return reviseId;
  } catch (error) {
    return rejectWithValue(error.response.data);
  }
});

// 📌 9. Dosya Ekle
export const addFile = createAsyncThunk('tasks/addFile', async ({ id, fileData }, { rejectWithValue }) => {
  try {
    const response = await api.post(`/${id}/add_file/`, fileData);
    return response.data;
  } catch (error) {
    return rejectWithValue(error.response.data);
  }
});

// 📌 Task Slice
const taskSlice = createSlice({
  name: 'tasks',
  initialState: {
    tasks: [],
    status: 'idle',
    error: null,
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      // Tüm görevleri getir
      .addCase(fetchTasks.pending, (state) => {
        state.status = 'loading';
      })
      .addCase(fetchTasks.fulfilled, (state, action) => {
        state.status = 'succeeded';
        state.tasks = action.payload;
      })
      .addCase(fetchTasks.rejected, (state, action) => {
        state.status = 'failed';
        state.error = action.payload;
      })
      // Yeni görev ekle
      .addCase(createTask.fulfilled, (state, action) => {
        state.tasks.push(action.payload);
      })
      // Görev güncelle
      .addCase(updateTask.fulfilled, (state, action) => {
        const index = state.tasks.findIndex((task) => task.id === action.payload.id);
        if (index !== -1) {
          state.tasks[index] = action.payload;
        }
      })
      // Görev sil
      .addCase(deleteTask.fulfilled, (state, action) => {
        state.tasks = state.tasks.filter((task) => task.id !== action.payload);
      })
      // Görev durumu güncelle
      .addCase(updateTaskStatus.fulfilled, (state, action) => {
        const index = state.tasks.findIndex((task) => task.id === action.payload.id);
        if (index !== -1) {
          state.tasks[index] = action.payload;
        }
      })
      // Revize ekle
      .addCase(addRevise.fulfilled, (state, action) => {
        const index = state.tasks.findIndex((task) => task.id === action.payload.id);
        if (index !== -1) {
          state.tasks[index] = action.payload;
        }
      })
      // Revize sil
      .addCase(deleteRevise.fulfilled, (state, action) => {
        const index = state.tasks.findIndex((task) => task.id === action.meta.arg.id);
        if (index !== -1) {
          state.tasks[index].revises = state.tasks[index].revises.filter(
            (revise) => revise.id !== action.payload
          );
        }
      });
  },
});

export default taskSlice.reducer;
