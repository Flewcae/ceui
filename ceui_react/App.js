import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { GestureHandlerRootView } from 'react-native-gesture-handler'; // Eklenen kısım
import MyTabs from './MyRouter';
import CustomHeader from './src/Components/CustomHeader';
import { Provider } from 'react-redux';
import { store } from './src/redux/store'


const App = () => {
  return (
    <Provider store={store}>
      <GestureHandlerRootView style={{ flex: 1 }}> {/* Eklenen kısım */}
          <MyTabs />
      </GestureHandlerRootView>
    </Provider>

  );
}

export default App;
