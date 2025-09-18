import React, {
  createContext,
  useContext,
  useState,
  useEffect,
  ReactNode,
} from "react";
import { ConfigProvider, theme } from "antd";

interface ThemeContextType {
  isDark: boolean;
  toggleTheme: () => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error("useTheme must be used within a ThemeProvider");
  }
  return context;
};

interface ThemeProviderProps {
  children: ReactNode;
}

export const ThemeProvider: React.FC<ThemeProviderProps> = ({ children }) => {
  const [isDark, setIsDark] = useState(() => {
    const saved = localStorage.getItem("pulse-theme");
    return saved === "dark";
  });

  useEffect(() => {
    localStorage.setItem("pulse-theme", isDark ? "dark" : "light");
    document.body.style.backgroundColor = isDark ? "#141414" : "#F5F5F5";
  }, [isDark]);

  const toggleTheme = () => {
    setIsDark(!isDark);
  };

  const antdTheme = {
    algorithm: isDark ? theme.darkAlgorithm : theme.defaultAlgorithm,
    token: {
      colorPrimary: "#1890ff",
      // Improve light theme contrast
      colorBgBase: isDark ? "#141414" : "#ffffff",
      colorBgContainer: isDark ? "#1f1f1f" : "#ffffff",
      colorBgElevated: isDark ? "#262626" : "#ffffff",
      colorBgLayout: isDark ? "#141414" : "#F5F5F5",
      colorBorder: isDark ? "#434343" : "#c0c0c0",
      colorBorderSecondary: isDark ? "#303030" : "#d0d0d0",
      colorTextHeading: isDark ? "#ffffff" : "#1890ff",
    },
  };

  return (
    <ThemeContext.Provider value={{ isDark, toggleTheme }}>
      <ConfigProvider theme={antdTheme}>{children}</ConfigProvider>
    </ThemeContext.Provider>
  );
};
