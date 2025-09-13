import axios from 'axios';
import Constants from 'expo-constants';

const GEMINI_API_KEY = Constants.expoConfig?.extra?.GEMINI_API_KEY;

const GEMINI_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent';

export async function askGemini(question: string): Promise<string> {
  if (!GEMINI_API_KEY) return 'Missing API key';

  try {
    const prompt = `
      Q: ${question}
      A: Provide a concise, helpful answer for me as a mom.
    `;

    const response = await axios.post(
      `${GEMINI_URL}?key=${GEMINI_API_KEY}`,
      { contents: [{ parts: [{ text: prompt }] }] }
    );

    const text = response.data.candidates?.[0]?.content?.parts?.[0]?.text;
    return text?.trim() || 'No answer received.';
  } catch (err: any) {
    console.error('Gemini API error:', err.message);
    return 'Could not get an answer. Try again.';
  }
}
