import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { colors } from '../../colors';

export default function ChatScreen({ navigation }) {
  return (
    <LinearGradient colors={[colors.navyDark, colors.navySoft]} style={styles.container}>
      <Text style={styles.text}>Chats</Text>
      <TouchableOpacity onPress={() => navigation.navigate('Detail')} style={styles.button}>
        <Text style={styles.buttonText}>Detay Sayfasına Git</Text>
      </TouchableOpacity>
    </LinearGradient>
  );
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
