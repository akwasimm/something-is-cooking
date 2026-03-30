import React, { createContext, useContext, useState, useEffect } from "react";
import axios from "axios";

// Standardizing localized Axos configurations guarding Token Injection
const api = axios.create({
  baseURL: "http://localhost:8000/api/v1", // Adjust mapped bounds targeting deployed backends explicitly
  headers: {
    "Content-Type": "application/json",
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("accessToken");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(false);
  const [initializing, setInitializing] = useState(true);

  const restore = async () => {
    const token = localStorage.getItem("accessToken");
    if (!token) {
      setInitializing(false);
      return;
    }

    try {
      // Utilizing our F-002 Profile Endpoint directly mimicking standard `me()` validations guaranteeing Authentication headers evaluate cleanly
      const response = await api.get("/profile/");
      setUser(response.data);
    } catch (error) {
      console.error("Session mapping invalidated locally:", error);
      localStorage.removeItem("accessToken");
      localStorage.removeItem("refreshToken");
    } finally {
      setInitializing(false);
    }
  };

  useEffect(() => {
    restore();
  }, []);

  const login = async (email, password) => {
    setLoading(true);
    try {
      const response = await api.post("/auth/login", { email, password });
      const { accessToken, refreshToken } = response.data;
      
      localStorage.setItem("accessToken", accessToken);
      localStorage.setItem("refreshToken", refreshToken);

      // Trigger automatic hydration pulling User Models natively immediately after token execution
      const profile = await api.get("/profile/");
      setUser(profile.data);
      
      return { success: true };
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.error || "A secure server connection failed." 
      };
    } finally {
      setLoading(false);
    }
  };

  const register = async (formData) => {
    setLoading(true);
    try {
      const response = await api.post("/auth/register", formData);
      const { accessToken, refreshToken } = response.data;
      
      localStorage.setItem("accessToken", accessToken);
      localStorage.setItem("refreshToken", refreshToken);

      // Hydration immediately
      const profile = await api.get("/profile/");
      setUser(profile.data);

      return { success: true };
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.error || "Registration endpoints crashed unexpectedly." 
      };
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem("accessToken");
    localStorage.removeItem("refreshToken");
    setUser(null);
  };

  const value = {
    user,
    loading,
    initializing,
    login,
    register,
    logout,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth mandates structuring directly inside <AuthProvider> nodes natively!");
  }
  return context;
};
