import React from 'react';
import { View, TouchableOpacity, Image, StyleSheet } from 'react-native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import Ionicons from 'react-native-vector-icons/Ionicons';
import { icons } from '../../icons';
import { colors } from '../../colors';

const Tab = createBottomTabNavigator();

export default function CustomTabBar({ state, descriptors, navigation }) {
  return (
    <View style={styles.tabContainer}>
      {state.routes.map((route, index) => {
        const { options } = descriptors[route.key];
        const isFocused = state.index === index;
        let iconName;

        if (route.name === 'Home') {
          iconName = 'home-outline';
        } else if (route.name === 'Chat') {
          iconName = 'chatbubble-outline';
        }

        return (
          <TouchableOpacity
            key={index}
            onPress={() => navigation.navigate(route.name)}
            style={styles.tabButton}
          >
            <Ionicons name={iconName} size={30} color={isFocused ? '#ffffff' : '#b0b0b0'} />
          </TouchableOpacity>
        );
      })}

      {/* ORTADAKİ LOGO */}
      <View style={styles.logoContainer}>
        <Image  source={icons.Icon} style={styles.logo} />
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  tabContainer: {
    flexDirection: 'row',
    backgroundColor: colors.navyDark, // Lacivert tab bar
    height: 80,
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 20,
    paddingBottom: 20,
    borderTopWidth:5,
    borderColor:"white"
  },
  tabButton: {
    flex: 1,
    alignItems: 'center',
  },
  logoContainer: {
    position: 'absolute',
    top: -40, // Logoyu yukarı almak için
    left: '50%',
    transform: [{ translateX: -20 }], // Tam ortaya hizalama (70 / 2)
    width: 80, // Logo genişliği
    height: 80, // Logo yüksekliği
    borderRadius: 40, // Yuvarlak yapmak için
    borderColor:"#0a0f24",
    borderWidth:2,
    borderBottomWidth:0,
    backgroundColor: 'white',
    justifyContent: 'center',
    alignItems: 'center',
  },
  
  logo: {
    width: 50,
    height: 50,
    resizeMode: 'contain',
  },
});
