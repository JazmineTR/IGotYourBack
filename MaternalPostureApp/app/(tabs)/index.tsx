import React, { useState } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  ScrollView,
  StyleSheet,
  Dimensions
} from 'react-native';
import { Image } from 'expo-image';
import { ThemedText } from '@/components/themed-text';
import { ThemedView } from '@/components/themed-view';
import { Link } from 'expo-router';
import { useRouter } from 'expo-router'; //Use for nav

// Color palette for nurturing/motherly theme
const colors = {
  primary: '#E8B4CB', // Soft pink
  secondary: '#F4D1AE', // Warm peach
  accent: '#B8E6B8', // Gentle mint green
  background: '#FFF8F3', // Cream white
  surface: '#FFFFFF',
  text: '#5D4E75', // Soft purple-gray
  textLight: '#8B7B9B',
  border: '#F0E6D6',
  success: '#A8D5A8',
  warning: '#F4D1AE',
  danger: '#F2B5B5',
  info: '#C8E3F0'
};

const { width } = Dimensions.get('window');

interface ButtonProps {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary' | 'outline' | 'success';
  size?: 'small' | 'medium' | 'large';
  onPress?: () => void;
  icon?: string;
  disabled?: boolean;
  style?: any;
}

const Button: React.FC<ButtonProps> = ({
  children,
  variant = 'primary',
  size = 'medium',
  onPress,
  disabled = false,
  style
}) => {
  const getButtonStyle = () => {
    const baseStyle = {
      borderRadius: 25,
      alignItems: 'center' as const,
      justifyContent: 'center' as const,
      flexDirection: 'row' as const,
      shadowOffset: { width: 0, height: 2 },
      shadowOpacity: 0.1,
      shadowRadius: 4,
      elevation: 2,
    };

    const sizeStyles = {
      small: { paddingHorizontal: 16, paddingVertical: 8 },
      medium: { paddingHorizontal: 24, paddingVertical: 12 },
      large: { paddingHorizontal: 32, paddingVertical: 16 }
    };

    const getBackgroundColor = () => {
      switch (variant) {
        case 'primary': return colors.primary;
        case 'secondary': return colors.secondary;
        case 'success': return colors.success;
        case 'outline': return 'transparent';
        default: return colors.primary;
      }
    };

    return {
      ...baseStyle,
      ...sizeStyles[size],
      backgroundColor: getBackgroundColor(),
      borderWidth: variant === 'outline' ? 2 : 0,
      borderColor: variant === 'outline' ? colors.primary : 'transparent',
      opacity: disabled ? 0.5 : 1,
      ...style
    };
  };

  const getTextColor = () => {
    return variant === 'outline' ? colors.text : '#FFFFFF';
  };

  return (
    <TouchableOpacity
      onPress={disabled ? undefined : onPress}
      style={getButtonStyle()}
      disabled={disabled}
    >
      <Text style={{ color: getTextColor(), fontWeight: '600', fontSize: size === 'small' ? 14 : 16 }}>
        {children}
      </Text>
    </TouchableOpacity>
  );
};

interface CardProps {
  children: React.ReactNode;
  style?: any;
  padding?: 'small' | 'medium' | 'large';
}

const Card: React.FC<CardProps> = ({ children, style, padding = 'medium' }) => {
  const paddingStyles = {
    small: 16,
    medium: 24,
    large: 32
  };

  return (
    <View
      style={[{
        backgroundColor: colors.surface,
        borderRadius: 16,
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.05,
        shadowRadius: 8,
        elevation: 2,
        borderWidth: 1,
        borderColor: colors.border,
        padding: paddingStyles[padding]
      }, style]}
    >
      {children}
    </View>
  );
};

const PostureIndicator: React.FC<{ status: 'good' | 'fair' | 'poor' }> = ({ status }) => {
  const getIndicatorColor = () => {
    switch (status) {
      case 'good': return colors.success;
      case 'fair': return colors.warning;
      case 'poor': return colors.danger;
      default: return colors.textLight;
    }
  };

  const getStatusText = () => {
    switch (status) {
      case 'good': return 'Excellent Posture ✓';
      case 'fair': return 'Need Adjustment ⚠️';
      case 'poor': return 'Poor Posture ⚠️';
      default: return 'Unknown';
    }
  };

  return (
    <Text style={{ color: getIndicatorColor(), fontWeight: '600', fontSize: 16 }}>
      {getStatusText()}
    </Text>
  );
};

const ProgressRing: React.FC<{ progress: number; size: number; label?: string }> = ({
  progress,
  size,
  label
}) => {
  return (
    <View style={{ alignItems: 'center' }}>
      <View
        style={{
          width: size,
          height: size,
          borderRadius: size / 2,
          backgroundColor: colors.border,
          alignItems: 'center',
          justifyContent: 'center',
          position: 'relative'
        }}
      >
        <View
          style={{
            width: size - 8,
            height: size - 8,
            borderRadius: (size - 8) / 2,
            backgroundColor: colors.surface,
            alignItems: 'center',
            justifyContent: 'center'
          }}
        >
          <Text style={{ fontSize: 18, fontWeight: 'bold', color: colors.text }}>
            {progress}%
          </Text>
          {label && (
            <Text style={{ fontSize: 10, color: colors.textLight, textAlign: 'center' }}>
              {label}
            </Text>
          )}
        </View>
      </View>
    </View>
  );
};

export default function HomeScreen() {
  const [currentPosture, setCurrentPosture] = useState<'good' | 'fair' | 'poor'>('fair');
  const [todayProgress] = useState(78);
  const [weekProgress] = useState(24);

  const router = useRouter(); //Initialize router for navigation

  const openCamera = () => {
    // Navigate to your camera feature
    console.log('Opening camera for posture analysis...');
    // Add your navigation logic here, e.g.:
    router.push('/camera');
  };

  return (
    <ScrollView style={{ backgroundColor: colors.background }}>
      {/* Header */}
      <View style={[styles.header, { backgroundColor: colors.primary }]}>
        <View style={styles.headerContent}>
          <View style={styles.headerTop}>
            <View>
              <Text style={styles.headerTitle}>I Got Your Back!</Text>
              <Text style={styles.headerSubtitle}>Track and Improve Your Posture</Text>
            </View>
            <TouchableOpacity style={styles.notificationButton}>
              <Text style={styles.notificationIcon}>🔔</Text>
            </TouchableOpacity>
          </View>

          {/* Current Status Card */}
          <Card style={styles.statusCard}>
            <View style={styles.statusContent}>
              <View>
                <Text style={styles.statusTitle}>Current Status</Text>
                <PostureIndicator status={currentPosture} />
              </View>
              <Button
                variant="outline"
                size="small"
                onPress={openCamera}
                style={{ backgroundColor: 'rgba(255,255,255,0.9)' }}
              >
                Open Camera
              </Button>
            </View>
          </Card>
        </View>
      </View>

      {/* Main Content */}
      <View style={styles.mainContent}>
        {/* Daily Progress */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Today's Progress</Text>
          <View style={styles.progressGrid}>
            <Card style={styles.progressCard}>
              <ProgressRing progress={todayProgress} size={60} />
              <Text style={styles.progressLabel}>Good Posture Time</Text>
            </Card>

            <Card style={styles.progressCard}>
              <View style={[styles.iconContainer, { backgroundColor: colors.accent }]}>
                <Text style={styles.icon}>🎯</Text>
              </View>
              <Text style={styles.progressValue}>12</Text>
              <Text style={styles.progressLabel}>Reminders</Text>
            </Card>

            <Card style={styles.progressCard}>
              <View style={[styles.iconContainer, { backgroundColor: colors.secondary }]}>
                <Text style={styles.icon}>⏰</Text>
              </View>
              <Text style={styles.progressValue}>6.2</Text>
              <Text style={styles.progressLabel}>Hours Active</Text>
            </Card>
          </View>
        </View>

        {/* Daily Tip */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Tip</Text>
          <Card>
            <View style={styles.tipContent}>
              <View style={[styles.tipIcon, { backgroundColor: colors.warning }]}>
                <Text style={styles.icon}>📱</Text>
              </View>
              <View style={styles.tipInfo}>
                <Text style={styles.tipTitle}>Mind Your Screen Time</Text>
                <Text style={styles.tipDescription}>
                  Keep your phone at eye level to avoid "text neck." When looking down at your phone,
                  your neck supports up to 60 pounds of pressure!
                </Text>
              </View>
            </View>
          </Card>
        </View>

        {/* Weekly Achievement */}
        <View style={[styles.section, { marginBottom: 32 }]}>
          <Text style={styles.sectionTitle}>This Week's Achievement</Text>
          <Card>
            <View style={styles.achievementContent}>
              <View style={[styles.achievementIcon, { backgroundColor: colors.primary }]}>
                <Text style={styles.icon}>🏆</Text>
              </View>
              <View style={styles.achievementInfo}>
                <Text style={styles.achievementTitle}>Posture Champion! 🏆</Text>
                <Text style={styles.achievementDescription}>
                  You maintained good posture for 5 days this week. Keep up the excellent work!
                </Text>
              </View>
            </View>
          </Card>
        </View>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  header: {
    position: 'relative',
    paddingBottom: 32,
    minHeight: 250, // <-- Add this line or increase as needed
  },
  headerImage: {
    height: 120,
    width: '100%',
    opacity: 0.3,
  },
  headerContent: {
    position: 'absolute',
    top: 60,
    left: 0,
    right: 0,
    paddingHorizontal: 24,
  },
  headerTop: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 24,
  },
  headerTitle: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#FFFFFF',
    marginBottom: 4,
  },
  headerSubtitle: {
    fontSize: 16,
    color: 'rgba(255,255,255,0.8)',
  },
  notificationButton: {
    width: 48,
    height: 48,
    borderRadius: 24,
    backgroundColor: 'rgba(255,255,255,0.2)',
    alignItems: 'center',
    justifyContent: 'center',
  },
  notificationIcon: {
    fontSize: 24,
  },
  statusCard: {
    backgroundColor: 'rgba(255,255,255,0.1)',
    borderColor: 'rgba(255,255,255,0.2)',
  },
  statusContent: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  statusTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#FFFFFF',
    marginBottom: 8,
  },
  mainContent: {
    paddingHorizontal: 24,
    paddingVertical: 24,
  },
  section: {
    marginBottom: 24,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: '600',
    color: colors.text,
    marginBottom: 16,
  },
  progressGrid: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    gap: 12,
  },
  progressCard: {
    flex: 1,
    alignItems: 'center',
    paddingVertical: 16,
  },
  progressLabel: {
    fontSize: 12,
    color: colors.textLight,
    textAlign: 'center',
    marginTop: 8,
    fontWeight: '500',
  },
  progressValue: {
    fontSize: 24,
    fontWeight: 'bold',
    color: colors.text,
    marginVertical: 4,
  },
  iconContainer: {
    width: 48,
    height: 48,
    borderRadius: 24,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 8,
  },
  icon: {
    fontSize: 24,
  },
  exerciseCard: {
    marginBottom: 12,
  },
  exerciseContent: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    gap: 16,
  },
  exerciseIcon: {
    width: 64,
    height: 64,
    borderRadius: 16,
    alignItems: 'center',
    justifyContent: 'center',
  },
  exerciseInfo: {
    flex: 1,
    gap: 8,
  },
  exerciseTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: colors.text,
  },
  exerciseDescription: {
    fontSize: 14,
    color: colors.textLight,
  },
  exerciseStatus: {
    alignItems: 'flex-end',
  },
  statusBadge: {
    fontSize: 12,
    fontWeight: '500',
  },
  tipContent: {
    flexDirection: 'row',
    gap: 16,
  },
  tipIcon: {
    width: 48,
    height: 48,
    borderRadius: 24,
    alignItems: 'center',
    justifyContent: 'center',
  },
  tipInfo: {
    flex: 1,
    gap: 12,
  },
  tipTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: colors.text,
  },
  tipDescription: {
    fontSize: 14,
    color: colors.textLight,
    lineHeight: 20,
  },
  achievementContent: {
    flexDirection: 'row',
    gap: 16,
  },
  achievementIcon: {
    width: 64,
    height: 64,
    borderRadius: 16,
    alignItems: 'center',
    justifyContent: 'center',
  },
  achievementInfo: {
    flex: 1,
    gap: 8,
  },
  achievementTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: colors.text,
  },
  achievementDescription: {
    fontSize: 14,
    color: colors.textLight,
    lineHeight: 20,
  },
});