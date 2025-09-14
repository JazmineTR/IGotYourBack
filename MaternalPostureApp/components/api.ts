export async function sendPostureData(imageUri: string) {
  const formData = new FormData();
  formData.append('image', {
    uri: imageUri,
    name: 'photo.jpg',
    type: 'image/jpeg',
  } as any);

  const res = await fetch('http://10.203.67.159:5000/detect', {
    method: 'POST',
    body: formData,
    headers: { 'Content-Type': 'multipart/form-data' },
  });

  return res.json(); // returns { annotated_image: "base64..." }
}
