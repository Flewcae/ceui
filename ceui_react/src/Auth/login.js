import React, { useState } from 'react';
import { View, Text, StyleSheet, TextInput, TouchableOpacity, Image, Alert } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { BlurView } from 'expo-blur';
import { Ionicons } from '@expo/vector-icons';
import { icons } from '../../icons';
import { useDispatch } from 'react-redux';
import { login } from '../redux/Actions/user';
import { colors } from '../../colors';

export default function LoginScreen({ navigation }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [secureTextEntry, setSecureTextEntry] = useState(true);
  const dispatch = useDispatch() 

  const handleLogin = () => {
    dispatch(login({ email, password }, (e, res) => {
      if (!e) {
        Alert.alert('Hatalı Giriş', res);
      }
    }));
  };

  return (
    <LinearGradient colors={[colors.navyDark, colors.navySoft]} style={styles.container}>
      <View style={styles.logoContainer}>
        <Image
            source={icons.MonoLogoTransparent}
            resizeMode="cover"
            style={[styles.logo, { tintColor: 'white' }]} 
        />
        </View>
      <BlurView intensity={30} style={styles.blurView}>
        <Text style={styles.title}>Giriş Yap</Text>

        <TextInput
          style={styles.input}
          placeholder="E-posta"
          placeholderTextColor="#ccc"
          keyboardType="email-address"
          autoCapitalize="none"
          value={email}
          onChangeText={setEmail}
        />

        <View style={styles.passwordContainer}>
          <TextInput
            style={styles.passwordInput}
            placeholder="Şifre"
            placeholderTextColor="#ccc"
            secureTextEntry={secureTextEntry}
            value={password}
            onChangeText={setPassword}
          />
          <TouchableOpacity onPress={() => setSecureTextEntry(!secureTextEntry)}>
            <Ionicons
              name={secureTextEntry ? 'eye-off' : 'eye'}
              size={24}
              color="#ccc"
            />
          </TouchableOpacity>
        </View>

        <TouchableOpacity onPress={()=>{handleLogin()}} style={styles.button}>
          <Text style={styles.buttonText}>Giriş Yap</Text>
        </TouchableOpacity>
        <Text style={styles.forgot}>Şifremi unuttum!</Text>
        <View style={styles.branded}>
          <TouchableOpacity onPress={()=>{handleLogin()}} style={styles.brandedButton}>
              <Ionicons
                name={'logo-google'}
                size={20}
                color="#ccc"
              />
            <Text style={styles.brandedButtonText}>Google ile{"\n"}Oturum Aç</Text>

          </TouchableOpacity>
          <TouchableOpacity onPress={()=>{handleLogin()}} style={styles.brandedButton}>
              <Ionicons
                name={'logo-facebook' }
                size={20}
                color="#ccc"
              />
            <Text style={styles.brandedButtonText}>Facebook ile{"\n"}Oturum Aç</Text>
          </TouchableOpacity>
        </View>
        <TouchableOpacity onPress={()=>{handleLogin()}} style={{...styles.button, marginTop:5}}>
          <Text style={styles.buttonText}>Kayıt Ol</Text>
        </TouchableOpacity>

      </BlurView>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'flex-end',
    alignItems: 'center',
    paddingBottom:60,
  },
  blurView: {
    padding: 20,
    margin: 16,
    justifyContent: 'center',
    alignItems: 'center',
    overflow: 'hidden',
    borderRadius: 10,
    width:"85%"
  },
  logoContainer: {
    marginBottom:30
  },
  
  logo: {
    width: 150,
    height: 150,
    resizeMode: 'contain',
  },
  title: {
    fontSize: 24,
    fontWeight: '400',
    color: '#fff',
    marginBottom: 20,
  },
  forgot: {
    fontSize: 18,
    fontWeight: '300',
    color: '#ccc',
    marginTop: 10,
    marginRight: 7,
    alignSelf:"flex-end"
  },
  input: {
    width: '100%',
    height: 50,
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
    borderRadius: 5,
    paddingHorizontal: 15,
    color: '#fff',
    marginBottom: 15,
  },
  passwordContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    width: '100%',
    height: 50,
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
    borderRadius: 10,
    paddingHorizontal: 15,
    marginBottom: 15,
  },
  passwordInput: {
    flex: 1,
    color: '#fff',
  },
  button: {
    marginTop: 10,
    padding: 15,
    backgroundColor: '#1e1e2d',
    borderRadius: 5,
    width: '100%',
    alignItems: 'center',
  },
  branded: {
    marginTop: 5,
    padding: 10,
    width: '100%',
    flexDirection: 'row',
    justifyContent:"center",
    alignItems: 'center',
    gap:10,
  },
  brandedButton: {
    backgroundColor: 'rgba(0, 0, 0, 0.2)',
    padding: 10,
    borderRadius: 5,
    width: '50%',
    justifyContent:"center",
    alignItems: 'center',
    gap:5,
  },
  buttonText: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: '300',
  },
  brandedButtonText: {
    color: '#ffffff',
    fontSize: 14,
    fontWeight: '300',
    textAlign: 'center',
  },
});
