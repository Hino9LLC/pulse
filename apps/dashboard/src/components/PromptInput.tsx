import React, { useState } from "react";
import { Input, Button, Card, Typography, Space, Spin } from "antd";
import { SendOutlined, BulbOutlined } from "@ant-design/icons";

const { TextArea } = Input;
const { Text } = Typography;

interface PromptInputProps {
  onSubmit: (prompt: string) => void;
  loading?: boolean;
}

const PromptInput: React.FC<PromptInputProps> = ({ onSubmit, loading = false }) => {
  const [prompt, setPrompt] = useState("");

  const handleSubmit = () => {
    if (prompt.trim()) {
      onSubmit(prompt.trim());
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) {
      handleSubmit();
    }
  };

  const examplePrompts = [
    "Create a pie chart representing industry breakdown",
    "Create a scatter plot of founded year and valuation",
    "Show me which investors appear most frequently",
    "What's the correlation between ARR and Valuation?",
    "Show companies with highest valuations",
    "Create a bar chart of average funding by industry"
  ];

  const selectExamplePrompt = (examplePrompt: string) => {
    setPrompt(examplePrompt);
  };

  return (
    <Card
      title={
        <Space>
          <BulbOutlined />
          <span>Natural Language Visualization</span>
        </Space>
      }
      style={{ marginBottom: 24 }}
    >
      <Space direction="vertical" style={{ width: "100%" }}>
        <Text type="secondary">
          Describe the visualization you want to create in plain English.
          Press Ctrl+Enter or click the button to generate.
        </Text>

        <div style={{ display: "flex", gap: 8 }}>
          <TextArea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="e.g., Create a pie chart showing the industry breakdown of companies"
            onKeyDown={handleKeyPress}
            disabled={loading}
            rows={2}
            style={{ flex: 1 }}
          />
          <Button
            type="primary"
            icon={loading ? <Spin size="small" /> : <SendOutlined />}
            onClick={handleSubmit}
            disabled={!prompt.trim() || loading}
            size="large"
          >
            Generate
          </Button>
        </div>

        <div>
          <Text strong style={{ fontSize: 12 }}>Example prompts:</Text>
          <div style={{ marginTop: 8, display: "flex", flexWrap: "wrap", gap: 8 }}>
            {examplePrompts.map((example, index) => (
              <Button
                key={index}
                size="small"
                type="dashed"
                onClick={() => selectExamplePrompt(example)}
                disabled={loading}
                style={{ fontSize: 11 }}
              >
                {example}
              </Button>
            ))}
          </div>
        </div>
      </Space>
    </Card>
  );
};

export default PromptInput;