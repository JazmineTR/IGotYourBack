import { Tabs } from 'expo-router';
import React from 'react';

import { HapticTab } from '@/components/haptic-tab';
import { IconSymbol } from '@/components/ui/icon-symbol';
import { Image } from 'react-native';
import { Colors } from '@/constants/theme';
import { useColorScheme } from '@/hooks/use-color-scheme';

export default function TabLayout() {
  const colorScheme = useColorScheme();

  return (
    <Tabs
      screenOptions={{
        tabBarActiveTintColor: Colors[colorScheme ?? 'light'].tint,
        headerShown: false,
        tabBarButton: HapticTab,
      }}>
      <Tabs.Screen
        name="index"
        options={{
          title: 'Home',
          tabBarIcon: ({ color }) => <IconSymbol size={28} name="house.fill" color={color} />,
        }}
      />
      <Tabs.Screen
        name="explore"
        options={{
          title: 'Ask Gemini questions',
          tabBarIcon: ({ color }) => (
            <Image
              source={require('@/assets/images/Icon-round-Question_mark.svg.png')}
              style={{ width: 28, height: 28 }}
              resizeMode="contain"
            />
          ),
        }}
      />
      <Tabs.Screen
        name="camera"
        options={{
          title: 'Camera',
          tabBarIcon: ({ color }) => (
            <Image
              source={require('@/assets/images/cameraVector.png')}
              style={{ width: 28, height: 28, tintColor: 'white' }}
              resizeMode="contain"
            />
          ),
        }}
      />
    </Tabs>
  );
}
