import React, { Component } from 'react'
import {View,Image,StyleSheet} from 'react-native'
import {icons} from '../icons'
import { LinearGradient } from 'expo-linear-gradient';
import { colors } from '../colors';

export default class SplashView extends Component {
    render() {
        return (
            <LinearGradient colors={[colors.navyDark, colors.navySoft]} style={styles.container}>
                <Image style={{width:'50%',height:'20%',  tintColor: 'white' }} source={icons.Icon} resizeMode='contain'/>
            </LinearGradient>
          );
       
    }
}



const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  text: {
    color: '#ffffff', // Beyaz metin
    fontSize: 24,
    fontWeight: 'bold',
  },
  button: {
    marginTop: 20,
    padding: 12,
    backgroundColor: '#1e1e2d', // Lacivert tonlarında bir buton rengi
    borderRadius: 10,
  },
  buttonText: {
    color: '#ffffff',
    fontSize: 16,
  },
});
