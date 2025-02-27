import React, { useEffect, useState } from 'react';
import { createStackNavigator } from '@react-navigation/stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { NavigationContainer } from '@react-navigation/native';
import Ionicons from 'react-native-vector-icons/Ionicons';
import HomeScreen from './src/Home';
import DetailScreen from './src/Home/detail';
import ChatScreen from './src/Chat';
import CustomTabBar from './src/Components/CustomTabBar';
import { StatusBar, StyleSheet, Text, View } from 'react-native';
import { useDispatch, useSelector } from 'react-redux';
import LoginScreen from './src/Auth/login';
import { getCSRF, getUser } from './src/redux/Actions/user';
import AsyncStorage from '@react-native-async-storage/async-storage'; // AsyncStorage'ı ekledik
import SplashView from './src/splash';
import CustomHeader from './src/Components/CustomHeader';

const Stack = createStackNavigator();
const Tab = createBottomTabNavigator();

const BottomTabNavigator = () => {
  return (
    <Tab.Navigator
      screenOptions={{ headerShown: false }}
      tabBar={(props) => <CustomTabBar {...props} />}
    >
      <Tab.Screen name="Home" component={HomeScreen} />
      <Tab.Screen name="Chat" component={ChatScreen} />
    </Tab.Navigator>
  );
};

const RootNavigator = () => {
  const dispatch = useDispatch();
  const user = useSelector((state) => state.User.user);
  const tokenState = useSelector((state) => state.User.token);
  const [page, setPage] = useState(tokenState?"home":"splash");
  const [token, setToken] = useState("");


  useEffect(()=>{
    console.log('tokenchange',token);
    
  },[token])

  

  useEffect(() => {
    const fetchToken = async () => {
      try {
        const value = await AsyncStorage.getItem("token");
        console.log('value',value);
        
        if (value) {
          dispatch(getUser(value));
        } else {
            setPage("login");
        }
      } catch (e) {
        setToken("login");
      }
    };

    dispatch(getCSRF());
    setTimeout(() => {
      fetchToken();
    }, 1000);
  }, [dispatch]);

  useEffect(() => {
    console.log(user);
    
    if (user) {
      let newPage = "login";
      if (user && user.user_type === 'admin') newPage = "home"
      setPage(newPage);
    } else {
      setPage('login')
    }
  }, [user]);

  const renderItems = () => {
    if (page === "splash") {
      return (
        <Stack.Navigator
          screenOptions={{
            headerShown: false,
          }}
        >
          <Stack.Screen name="Splash" component={SplashView} />
        </Stack.Navigator>

      );
    }

    if (!user) {
      return (
        <Stack.Navigator
          screenOptions={{
            headerShown: false,
          }}
        >
          <Stack.Screen name="Login" component={LoginScreen}>
          </Stack.Screen>
        </Stack.Navigator>
      );
    } else {
      return (
        <Stack.Navigator screenOptions={{ headerShown: false }}>
        <Stack.Screen name="Main" component={BottomTabNavigator} />
        <Stack.Screen name="Detail" component={DetailScreen} />
      </Stack.Navigator>
      );
    }

  };

    return (
      <NavigationContainer>
      <CustomHeader/>
      {renderItems()}
      <StatusBar  hidden/>
      </NavigationContainer>

    );
 
};

export default RootNavigator;
