import React, { useState, useRef, useEffect } from "react";
import { Send, User, Bot, Image, AlertCircle } from "lucide-react";

export default function App() {
  const [prompt, setPrompt] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const handleFollowUpClick = (question) => {
    if (loading) return;
    
    const event = { preventDefault: () => {} };
    setPrompt(question);

    handleSubmit(event);
    
 
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  async function handleSubmit(e) {
    e.preventDefault();
    if (!prompt.trim() || loading) return;

    const userMessage = {
      id: Date.now(),
      type: "user",
      content: prompt.trim(),
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setPrompt("");
    setLoading(true);

    try {
      const res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/generate`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ prompt: userMessage.content }),
      });

      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }

      const data = await res.json();
      console.log("API response data:", data);
      
      const botMessage = {
        id: Date.now() + 1,
        type: "assistant",
        content: data.response,
        image: data.image,
        followUp: data.followup || [],
        timestamp: new Date()
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (err) {
      const errorMessage = {
        id: Date.now() + 1,
        type: "error",
        content: `Failed to generate response: ${err.message}`,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
      inputRef.current?.focus();
    }
  }

  const formatTime = (date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const formatText = (text) => {
    if (!text) return text;
    
    // Handle triple asterisks for bold+italic (***text***)
    let formatted = text.replace(/\*\*\*(.*?)\*\*\*/g, '<strong><em>$1</em></strong>');
    
    // Handle double asterisks for bold (**text**)
    formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // Handle single asterisks for italic (*text*)
    formatted = formatted.replace(/\*(.*?)\*/g, '<em>$1</em>');
    
    return formatted;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800">
      <div className="max-w-4xl mx-auto flex flex-col h-screen">
        {/* Header */}
        <div className="bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm border-b border-slate-200 dark:border-slate-700 p-4 shadow-sm">
          <h1 className="text-2xl font-bold text-slate-800 dark:text-slate-100 flex items-center gap-2">
            <Bot className="w-7 h-7 text-blue-600 dark:text-blue-400" />
            clown.ai
          </h1>
          <p className="text-slate-600 dark:text-slate-400 text-sm mt-1">
            I'm funny apparently and I can generate images too!
          </p>
        </div>

        {/* Messages Container */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.length === 0 && (
            <div className="text-center py-12">
              <Bot className="w-16 h-16 mx-auto text-slate-400 dark:text-slate-600 mb-4" />
              <h3 className="text-xl font-semibold text-slate-600 dark:text-slate-400 mb-2">
                Start a conversation
              </h3>
              <p className="text-slate-500 dark:text-slate-500">
                Type a message below to begin chatting with the AI assistant
              </p>
            </div>
          )}

          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex gap-3 ${
                message.type === "user" ? "justify-end" : "justify-start"
              }`}
            >
              {message.type !== "user" && (
                <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
                  message.type === "error" 
                    ? "bg-red-100 dark:bg-red-900/30" 
                    : "bg-blue-100 dark:bg-blue-900/30"
                }`}>
                  {message.type === "error" ? (
                    <AlertCircle className="w-4 h-4 text-red-600 dark:text-red-400" />
                  ) : (
                    <Bot className="w-4 h-4 text-blue-600 dark:text-blue-400" />
                  )}
                </div>
              )}

              <div className={`max-w-2xl rounded-2xl px-4 py-3 ${
                message.type === "user"
                  ? "bg-blue-600 text-white ml-12"
                  : message.type === "error"
                  ? "bg-red-50 dark:bg-red-900/20 text-red-800 dark:text-red-200 border border-red-200 dark:border-red-800"
                  : "bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-200 shadow-sm border border-slate-200 dark:border-slate-700"
              }`}>
                <div 
                  className="whitespace-pre-wrap break-words"
                  dangerouslySetInnerHTML={{ __html: formatText(message.content) }}
                />

                {message.image && (
                  <div className="mt-3 rounded-lg overflow-hidden border border-slate-200 dark:border-slate-600">
                    <div className="flex items-center gap-2 bg-slate-50 dark:bg-slate-700 px-3 py-2 text-sm text-slate-600 dark:text-slate-400">
                      <Image className="w-4 h-4" />
                      Generated Image
                    </div>
                    <img
                      src={`data:image/png;base64,${message.image}`}
                      alt="Generated"
                      className="w-full h-auto"
                      loading="lazy"
                    />
                  </div>
                )}
                {message.followUp && message.followUp.length > 0 && (
                  <div className="mt-4 pt-3 border-t border-slate-200 dark:border-slate-600">
                    <div className="text-sm text-slate-600 dark:text-slate-400 mb-2 font-medium">
                      Continue the conversation:
                    </div>
                    <div className="flex flex-wrap gap-2">
                      {message.followUp.map((question, idx) => (
                        <button
                          key={idx}
                          onClick={() => handleFollowUpClick(question)}
                          disabled={loading}
                          className="text-sm px-3 py-1.5 bg-slate-100 dark:bg-slate-700 hover:bg-slate-200 dark:hover:bg-slate-600 text-slate-700 dark:text-slate-300 rounded-full transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed border border-slate-200 dark:border-slate-600"
                        >
                          {question}
                        </button>
                      ))}
                    </div>
                  </div>
                )}

                
                
                <div className={`text-xs mt-2 ${
                  message.type === "user" 
                    ? "text-blue-100" 
                    : "text-slate-500 dark:text-slate-500"
                }`}>
                  {formatTime(message.timestamp)}
                </div>
              </div>

              

              {message.type === "user" && (
                <div className="flex-shrink-0 w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
                  <User className="w-4 h-4 text-white" />
                </div>
              )}
            </div>
          ))}
    
          {loading && (
            <div className="flex gap-3 justify-start">
              <div className="flex-shrink-0 w-8 h-8 bg-blue-100 dark:bg-blue-900/30 rounded-full flex items-center justify-center">
                <Bot className="w-4 h-4 text-blue-600 dark:text-blue-400" />
              </div>
              <div className="bg-white dark:bg-slate-800 rounded-2xl px-4 py-3 shadow-sm border border-slate-200 dark:border-slate-700">
                <div className="flex items-center gap-2">
                  <div className="flex gap-1">
                    <div className="w-2 h-2 bg-blue-600 dark:bg-blue-400 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-blue-600 dark:bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                    <div className="w-2 h-2 bg-blue-600 dark:bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  </div>
                  <span className="text-slate-600 dark:text-slate-400 text-sm">Generating response...</span>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input Form */}
        <div className="bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm border-t border-slate-200 rounded-xl mb-3 dark:border-slate-700 p-4 shadow-sm">
          <form onSubmit={handleSubmit} className="flex gap-3">
            <div className="flex-1 relative">
              <input
                ref={inputRef}
                type="text"
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="Type your message here..."
                className="w-full px-4 py-3 pr-12 rounded-xl border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-200 placeholder-slate-500 dark:placeholder-slate-400 focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all duration-200"
                disabled={loading}
                autoFocus
              />
            </div>
            <button
              type="submit"
              disabled={!prompt.trim() || loading}
              className="px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-300 dark:disabled:bg-slate-600 text-white rounded-xl font-medium transition-all duration-200 flex items-center gap-2 shadow-sm hover:shadow-md disabled:cursor-not-allowed"
            >
              <Send className="w-4 h-4" />
              Send
            </button>
          </form>
          
          {messages.length > 0 && (
            <div className="flex justify-between items-center mt-3 text-xs text-slate-500 dark:text-slate-500">
              <span>{messages.length} messages</span>
              <button
                onClick={() => setMessages([])}
                className="hover:text-slate-700 dark:hover:text-slate-300 transition-colors"
              >
                Clear chat
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}