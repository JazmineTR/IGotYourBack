import React, { useState } from 'react';
import { 
  View, 
  Text, 
  TextInput,
  TouchableOpacity, 
  ScrollView, 
  StyleSheet,
  KeyboardAvoidingView,
  Platform
} from 'react-native';
import { askGemini } from '@/components/gemini';

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
  userMessage: '#E8B4CB',
  botMessage: '#F4F4F4',
};

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'bot';
  timestamp: Date;
}

interface ChatBubbleProps {
  message: Message;
}

const ChatBubble: React.FC<ChatBubbleProps> = ({ message }) => {
  const isUser = message.sender === 'user';
  
  return (
    <View style={[
      styles.messageBubble,
      isUser ? styles.userBubble : styles.botBubble
    ]}>
      <Text style={[
        styles.messageText,
        { color: isUser ? '#FFFFFF' : colors.text }
      ]}>
        {message.text}
      </Text>
      <Text style={[
        styles.messageTime,
        { color: isUser ? 'rgba(255,255,255,0.7)' : colors.textLight }
      ]}>
        {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
      </Text>
    </View>
  );
};

export default function ChatbotScreen() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      text: 'Hello! I\'m your maternity posture assistant. How can I help you today? Also, please be patient with me! 🤗',
      sender: 'bot',
      timestamp: new Date()
    }
  ]);
  const [inputText, setInputText] = useState('');
  const [isTyping, setIsTyping] = useState(false);

  const sendMessage = async() => {
    if (inputText.trim() === '') return;

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputText,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setIsTyping(true);

    try {
    // Call your Gemini helper
    const botReply = await askGemini(inputText);

    const botMessage: Message = {
      id: (Date.now() + 1).toString(),
      text: botReply,
      sender: 'bot',
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, botMessage]);
  } catch (error) {
    console.error('Gemini error:', error);
    const botMessage: Message = {
      id: (Date.now() + 2).toString(),
      text: 'Sorry, I couldn’t get an answer. Please try again.',
      sender: 'bot',
      timestamp: new Date(),
    };
    setMessages(prev => [...prev, botMessage]);
  } finally {
    setIsTyping(false);
  }
};


  const quickQuestions = [
    "How can I improve my posture?",
    "Tips for back pain relief",
    "Best sleeping positions"
  ];

  const handleQuickQuestion = async (question: string) => {
    setInputText(question);
    await sendMessage();
  };

  return (
    <KeyboardAvoidingView 
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
    >
      {/* Header */}
      <View style={styles.header}>
        <View style={styles.botAvatar}>
          <Text style={styles.botAvatarText}>🤖</Text>
        </View>
        <View style={styles.headerInfo}>
          <Text style={styles.headerTitle}>Posture Assistant</Text>
          <Text style={styles.headerSubtitle}>
            {isTyping ? 'Typing...' : 'Online • Ready to help'}
          </Text>
        </View>
      </View>

      {/* Messages */}
      <ScrollView 
        style={styles.messagesContainer}
        showsVerticalScrollIndicator={false}
      >
        {messages.map((message) => (
          <ChatBubble key={message.id} message={message} />
        ))}
        
        {/* Typing Indicator */}
        {isTyping && (
          <View style={[styles.messageBubble, styles.botBubble, styles.typingIndicator]}>
            <Text style={[styles.messageText, { color: colors.text }]}>
              ● ● ● 
            </Text>
          </View>
        )}

        {/* Quick Questions */}
        {messages.length === 1 && (
          <View style={styles.quickQuestionsContainer}>
            <Text style={styles.quickQuestionsTitle}>Quick Questions:</Text>
            {quickQuestions.map((question, index) => (
              <TouchableOpacity
                key={index}
                style={styles.quickQuestionButton}
                onPress={() => handleQuickQuestion(question)}
              >
                <Text style={styles.quickQuestionText}>{question}</Text>
              </TouchableOpacity>
            ))}
          </View>
        )}
      </ScrollView>

      {/* Input Area */}
      <View style={styles.inputContainer}>
        <View style={styles.inputWrapper}>
          <TextInput
            style={styles.textInput}
            placeholder="Ask me about posture, exercises, or maternity tips..."
            placeholderTextColor={colors.textLight}
            value={inputText}
            onChangeText={setInputText}
            multiline
            maxLength={500}
          />
          <TouchableOpacity 
            style={[
              styles.sendButton,
              { backgroundColor: inputText.trim() ? colors.primary : colors.border }
            ]}
            onPress={sendMessage}
            disabled={inputText.trim() === '' || isTyping}
          >
            <Text style={styles.sendButtonText}>
              {isTyping ? '⏳' : '➤'}
            </Text>
          </TouchableOpacity>
        </View>
        <Text style={styles.inputHint}>
          Get personalized advice for your journey
        </Text>
      </View>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingVertical: 16,
    paddingTop: 60, // Account for status bar
    backgroundColor: colors.surface,
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 3,
    elevation: 2,
  },
  botAvatar: {
    width: 48,
    height: 48,
    borderRadius: 24,
    backgroundColor: colors.primary,
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: 12,
  },
  botAvatarText: {
    fontSize: 24,
  },
  headerInfo: {
    flex: 1,
  },
  headerTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: colors.text,
  },
  headerSubtitle: {
    fontSize: 14,
    color: colors.textLight,
    marginTop: 2,
  },
  messagesContainer: {
    flex: 1,
    paddingHorizontal: 16,
    paddingVertical: 12,
  },
  messageBubble: {
    maxWidth: '80%',
    marginVertical: 4,
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderRadius: 20,
  },
  userBubble: {
    alignSelf: 'flex-end',
    backgroundColor: colors.userMessage,
    borderBottomRightRadius: 4,
  },
  botBubble: {
    alignSelf: 'flex-start',
    backgroundColor: colors.botMessage,
    borderBottomLeftRadius: 4,
    borderWidth: 1,
    borderColor: colors.border,
  },
  messageText: {
    fontSize: 16,
    lineHeight: 22,
  },
  messageTime: {
    fontSize: 12,
    marginTop: 6,
    alignSelf: 'flex-end',
  },
  typingIndicator: {
    opacity: 0.8,
  },
  quickQuestionsContainer: {
    marginTop: 20,
    paddingHorizontal: 4,
  },
  quickQuestionsTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: colors.text,
    marginBottom: 12,
  },
  quickQuestionButton: {
    backgroundColor: colors.surface,
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: 20,
    paddingHorizontal: 16,
    paddingVertical: 12,
    marginBottom: 8,
  },
  quickQuestionText: {
    fontSize: 14,
    color: colors.text,
  },
  inputContainer: {
    paddingHorizontal: 16,
    paddingVertical: 12,
    backgroundColor: colors.surface,
    borderTopWidth: 1,
    borderTopColor: colors.border,
  },
  inputWrapper: {
    flexDirection: 'row',
    alignItems: 'flex-end',
    backgroundColor: colors.background,
    borderRadius: 25,
    borderWidth: 1,
    borderColor: colors.border,
    paddingHorizontal: 16,
    paddingVertical: 8,
  },
  textInput: {
    flex: 1,
    fontSize: 16,
    color: colors.text,
    maxHeight: 100,
    paddingVertical: 8,
  },
  sendButton: {
    width: 36,
    height: 36,
    borderRadius: 18,
    alignItems: 'center',
    justifyContent: 'center',
    marginLeft: 8,
  },
  sendButtonText: {
    fontSize: 18,
    color: '#FFFFFF',
    fontWeight: '600',
  },
  inputHint: {
    fontSize: 12,
    color: colors.textLight,
    textAlign: 'center',
    marginTop: 8,
  },
});