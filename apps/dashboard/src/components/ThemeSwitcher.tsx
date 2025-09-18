import React from "react";
import { Button } from "antd";
import { BulbOutlined, BulbFilled } from "@ant-design/icons";
import { useTheme } from "../ThemeContext";

export const ThemeSwitcher: React.FC = () => {
  const { isDark, toggleTheme } = useTheme();

  return (
    <Button
      type="text"
      icon={
        isDark ? (
          <BulbOutlined style={{ color: "#fff" }} />
        ) : (
          <BulbFilled style={{ color: "#fadb14" }} />
        )
      }
      onClick={toggleTheme}
      size="large"
      title={`Switch to ${isDark ? "light" : "dark"} mode`}
    />
  );
};
