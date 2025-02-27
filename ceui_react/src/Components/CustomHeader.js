import { useEffect, useState } from "react";
import { StyleSheet, Text, View } from "react-native";
import { colors } from "../../colors";

const CustomHeader = () => {
  const [time, setTime] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => {
      setTime(new Date());
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  const hours = time.getHours().toString().padStart(2, '0');
  const minutes = time.getMinutes().toString().padStart(2, '0');


    return (
      <View style={styles.header}>
        <Text style={styles.headerText}>CEUI</Text>
        <Text style={styles.hourText}> {hours}:{minutes}</Text>
      </View>
    );
  };

export default CustomHeader;

const styles = StyleSheet.create({
    header: {
      zIndex: 10,
      position:'absolute',
      top:0,
      left:0,
      height: 60,
      width:'100%',
      flexDirection: 'row',
      backgroundColor: colors.navyDark, // Lacivert tab bar
      alignItems: 'center',
      justifyContent: 'center',
      paddingHorizontal: 20,
      borderBottomWidth:5,
      borderColor:"white"
    },
    headerText: {
      color: "white",
      fontSize: 20,
      fontWeight: 600,
    },
    hourText: {
      color: "white",
      fontSize: 20,
      fontWeight: 400,
      position:"absolute",
      right:20,
      top:15
    }
    
  });