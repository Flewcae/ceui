import React, { useEffect } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ActivityIndicator, FlatList } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { useDispatch, useSelector } from 'react-redux';
import { fetchTasks } from '../redux/Actions/task';
import { BlurView } from 'expo-blur';
import { colors } from '../../colors';

export default function HomeScreen({ navigation }) {

  const dispatch = useDispatch();
  const { tasks, status, error } = useSelector((state) => state.tasks);
  const permissions = useSelector((state) => state.User.permissions);
  

  const reload = ()=>{
    dispatch(fetchTasks()); // Redux'tan görevleri kiyoruz
  }



  useEffect(() => {
    reload();
  }, [dispatch]);

  const renderTask = ({ item }) => (
    <TouchableOpacity >
      <BlurView intensity={35} experimentalBlurMethod='dimezisBlurView' tint='systemMaterialLight' style={styles.taskItem}>
        <Text style={styles.taskName}>{item.name}</Text>
        <Text style={styles.taskStatus}>Durum: {item.status}</Text>
      </BlurView>
    </TouchableOpacity>
  );

  if (status === 'loading') {
    return (
      <View style={styles.centered}>
        <ActivityIndicator size="large" color="#3498db" />
      </View>
    );
  }

  if (status === 'failed') {
    return (
      <View style={styles.centered}>
        <Text style={styles.errorText}>Hata: {error}</Text>
      </View>
    );
  }

  return (
    <LinearGradient colors={[colors.navyDark, colors.navySoft]} style={styles.container}>
      {permissions.task?.view&&(
        <View style={{flex:0.8, width:"100%", paddingHorizontal:10}}>
          <Text style={styles.title}>Görevlerim</Text>
          
          <FlatList
            data={tasks}
            keyExtractor={(item) => item.id.toString()}
            renderItem={renderTask}
            ListEmptyComponent={<Text style={styles.emptyText}>Henüz görev yok.</Text>}
          />
        </View>
      )}
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
  title: {
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
  taskItem: {
    flex: 1,
    padding: 20,
    marginVertical: 5,
    textAlign: 'center',
    justifyContent: 'center',
    overflow: 'hidden',
    borderRadius: 20,
  },
  taskName: {
    fontSize: 18,
    fontWeight: 'bold',
    color:"white",
  },
  taskStatus: {
    fontSize: 14,
    color:"white",
  },
});
