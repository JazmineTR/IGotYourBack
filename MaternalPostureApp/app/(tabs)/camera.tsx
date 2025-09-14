import { AntDesign } from '@expo/vector-icons';
import { CameraView, CameraType, useCameraPermissions } from 'expo-camera';
import { useRef, useState, useEffect } from 'react';
import { View, TouchableOpacity, Text, Image, StyleSheet, Alert } from 'react-native';

export default function CameraScreen() {
  const cameraRef = useRef<CameraView | null>(null);
  const [permission, requestPermission] = useCameraPermissions();
  const [facing, setFacing] = useState<CameraType>('back');
  const [photo, setPhoto] = useState<{ uri: string } | null>(null);
  const [uploading, setUploading] = useState(false);
  
  // New state for detection data (minimal addition)
  const [detections, setDetections] = useState([]);
  const [postureStatus, setPostureStatus] = useState('');

  // Request camera permission on mount
  useEffect(() => {
    requestPermission();
  }, []);

  if (!permission?.granted) {
    return (
      <View style={styles.container}>
        <Text style={{ textAlign: 'center' }}>Camera permission needed</Text>
        <TouchableOpacity onPress={requestPermission} style={styles.button}>
          <Text>Grant Permission</Text>
        </TouchableOpacity>
      </View>
    );
  }

  const toggleCameraFacing = () =>
    setFacing(facing === 'back' ? 'front' : 'back');

  const handleTakePhoto = async () => {
    if (!cameraRef.current || uploading) return;

    try {
      setUploading(true);

      // Your original photo capture logic (unchanged)
      const takenPhoto = await cameraRef.current.takePictureAsync({ quality: 1 });

      const formData = new FormData();
      formData.append('image', {
        uri: takenPhoto.uri,
        name: 'photo.jpg',
        type: 'image/jpeg',
      } as any);

      const res = await fetch('http://10.203.67.159:5000/predict_posture', {
  method: 'POST',
  body: formData,
  headers: { 'Content-Type': 'multipart/form-data' },
});// ADD THESE DEBUG LINES:
  console.log('Response status:', res.status);
  console.log('Response headers:', res.headers);
  
  const responseText = await res.text(); // Get as text first
  console.log('Raw response:', responseText.substring(0, 200)); // First 200 chars
  
  // Try to parse as JSON
  let data;
  try {
    data = JSON.parse(responseText);
  } catch (parseError) {
    console.log('JSON parse failed:', parseError);
    Alert.alert('Server Error', 'Server returned invalid response');
    return;
  }

// const data = await res.json();
// console.log('Server response:', data);
// console.log('Response keys:', Object.keys(data));
// console.log('annotated_image exists:', !!data.annotated_image);
// console.log('Image length:', data.annotated_image?.length);

// Try displaying original photo first to test
setPhoto({ uri: takenPhoto.uri }); // Original photo
// setPhoto({ uri: `data:image/jpeg;base64,${data.annotated_image}` }); // Annotated

      // Extract detection data if available (new - but doesn't change your workflow)
      if (data.detections) {
        setDetections(data.detections);
      }
      if (data.posture_status) {
        setPostureStatus(data.posture_status);
      }

      // Show detection summary (optional alert)
      if (data.detections && data.detections.length > 0) {
        Alert.alert(
          'Detection Complete',
          `Found ${data.detections.length} objects\nPosture: ${data.posture_status || 'Unknown'}`,
          [{ text: 'OK' }]
        );
      }

    } catch (err) {
      console.log('Error uploading photo:', err);
    } finally {
      setUploading(false);
    }
  };

  const handleRetakePhoto = () => {
    setPhoto(null);
    // Clear detection data when retaking
    setDetections([]);
    setPostureStatus('');
  };

  // Render annotated photo if exists (your original logic + small detection info)
  if (photo) {
    return (
      <View style={styles.container}>
        <Image
          source={{ uri: photo.uri }}
          style={{ flex: 1, resizeMode: 'contain' }}
        />
        
        {/* Optional: Show posture status overlay on the photo */}
        {postureStatus && (
          <View style={[styles.postureOverlay, {
            backgroundColor: postureStatus.includes('Safe') ? '#00ff0080' : '#ff000080'
          }]}>
            <Text style={styles.postureText}>{postureStatus}</Text>
          </View>
        )}

        {/* Optional: Show detection count at bottom */}
        {detections.length > 0 && (
          <View style={styles.detectionInfo}>
            <Text style={styles.detectionText}>
              📍 {detections.length} objects detected
            </Text>
          </View>
        )}

        <TouchableOpacity onPress={handleRetakePhoto} style={styles.button}>
          <Text>Retake</Text>
        </TouchableOpacity>
      </View>
    );
  }

  // Camera view (your original code - completely unchanged)
  return (
    <View style={styles.container}>
      <CameraView ref={cameraRef} style={{ flex: 1 }} facing={facing} />
      <View style={styles.overlay}>
        <TouchableOpacity style={styles.button} onPress={toggleCameraFacing}>
          <AntDesign name="retweet" size={44} color="black" />
        </TouchableOpacity>
        <TouchableOpacity 
          style={[styles.button, { backgroundColor: uploading ? '#ccc' : 'gray' }]} 
          onPress={handleTakePhoto}
          disabled={uploading}
        >
          <AntDesign name="camera" size={44} color="black" />
        </TouchableOpacity>
      </View>

      {/* Show processing indicator (minimal addition) */}
      {uploading && (
        <View style={styles.loadingOverlay}>
          <Text style={styles.loadingText}>Processing...</Text>
        </View>
      )}
    </View>
  );
}

// Your original styles + minimal additions
const styles = StyleSheet.create({
  container: { flex: 1 },
  overlay: {
    position: 'absolute',
    bottom: 40,
    left: 0,
    right: 0,
    flexDirection: 'row',
    justifyContent: 'space-evenly',
  },
  button: {
    backgroundColor: 'gray',
    padding: 12,
    borderRadius: 10,
    alignItems: 'center',
  },
  // New styles for detection display (minimal)
  postureOverlay: {
    position: 'absolute',
    top: 80,
    left: 20,
    right: 20,
    padding: 12,
    borderRadius: 8,
    alignItems: 'center',
  },
  postureText: {
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
  },
  detectionInfo: {
    position: 'absolute',
    bottom: 120,
    left: 20,
    right: 20,
    backgroundColor: '#00000080',
    padding: 8,
    borderRadius: 6,
    alignItems: 'center',
  },
  detectionText: {
    color: 'white',
    fontSize: 14,
    fontWeight: '500',
  },
  photoControls: {
    position: 'absolute',
    bottom: 40,
    left: 0,
    right: 0,
    alignItems: 'center',
  },
  retakeButton: {
    backgroundColor: '#007AFF',
    padding: 15,
    borderRadius: 10,
    minWidth: 120,
    alignItems: 'center',
  },
  retakeButtonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
  },
  loadingOverlay: {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: [{ translateX: -50 }, { translateY: -50 }],
    backgroundColor: '#00000080',
    padding: 15,
    borderRadius: 10,
    alignItems: 'center',
  },
  loadingText: {
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
  },
});