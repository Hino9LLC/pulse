import React from "react";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Pie, Bar, Scatter, Line } from "react-chartjs-2";
import { Table, Alert, Card, Button } from "antd";
import { CloseOutlined } from "@ant-design/icons";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

interface VisualizationData {
  success: boolean;
  visualization_type: string;
  title: string;
  data: any[];
  chart_config: any;
  sql?: string;
  error?: string;
}

interface VisualizationChartProps {
  data: VisualizationData;
  onRemove?: () => void;
}

const VisualizationChart: React.FC<VisualizationChartProps> = ({ data, onRemove }) => {
  if (!data.success) {
    return (
      <Alert
        type="error"
        message="Visualization Error"
        description={data.error || "Failed to generate visualization"}
        showIcon
      />
    );
  }

  const generateColors = (count: number) => {
    // Use custom colors from chart_config if available
    if (data.chart_config?.colors && data.chart_config.colors.length > 0) {
      return Array.from({ length: count }, (_, i) =>
        data.chart_config.colors[i % data.chart_config.colors.length]
      );
    }

    // Map color names to hex values
    const colorMap: { [key: string]: string } = {
      'light_blue': '#87CEEB',
      'light blue': '#87CEEB',
      'blue': '#36A2EB',
      'red': '#FF6384',
      'green': '#4BC0C0',
      'yellow': '#FFCE56',
      'purple': '#9966FF',
      'orange': '#FF9F40',
      'pink': '#FFB6C1',
      'gray': '#C9CBCF',
      'grey': '#C9CBCF'
    };

    // Check if chart_style specifies a color theme
    if (data.chart_config?.chart_style) {
      const style = data.chart_config.chart_style.toLowerCase();
      if (colorMap[style]) {
        return Array.from({ length: count }, () => colorMap[style]);
      }
      // Handle color themes
      if (style === 'pastel') {
        const pastels = ['#FFB6C1', '#87CEEB', '#98FB98', '#F0E68C', '#DDA0DD'];
        return Array.from({ length: count }, (_, i) => pastels[i % pastels.length]);
      }
      if (style === 'vibrant') {
        const vibrant = ['#FF4500', '#32CD32', '#1E90FF', '#FF1493', '#FFD700'];
        return Array.from({ length: count }, (_, i) => vibrant[i % vibrant.length]);
      }
    }

    // Default colors
    const colors = [
      "#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF",
      "#FF9F40", "#FF6384", "#C9CBCF", "#4BC0C0", "#FF6384"
    ];
    return Array.from({ length: count }, (_, i) => colors[i % colors.length]);
  };

  const renderChart = () => {
    switch (data.visualization_type) {
      case "pie":
        const pieData = {
          labels: data.data.map(item => Object.values(item)[0] as string),
          datasets: [{
            data: data.data.map(item => Object.values(item)[1] as number),
            backgroundColor: generateColors(data.data.length),
            borderWidth: 1,
          }]
        };
        return <Pie data={pieData} options={{
          responsive: true,
          plugins: {
            legend: {
              position: (data.chart_config?.legend_position || 'bottom') as 'top' | 'bottom' | 'left' | 'right'
            }
          }
        }} />;

      case "bar":
        const barData = {
          labels: data.data.map(item => Object.values(item)[0] as string),
          datasets: [{
            label: data.chart_config.y_field || "Value",
            data: data.data.map(item => Object.values(item)[1] as number),
            backgroundColor: generateColors(data.data.length),
            borderWidth: 1,
          }]
        };
        return <Bar data={barData} options={{ responsive: true, plugins: { legend: { display: false } } }} />;

      case "scatter":
        const scatterColors = generateColors(1);
        const scatterData = {
          datasets: [{
            label: data.title,
            data: data.data.map(item => ({
              x: Object.values(item)[0] as number,
              y: Object.values(item)[1] as number,
            })),
            backgroundColor: data.chart_config?.background_color || scatterColors[0],
            borderColor: data.chart_config?.border_color || scatterColors[0],
          }]
        };
        return <Scatter data={scatterData} options={{ responsive: true, plugins: { legend: { display: false } } }} />;

      case "line":
        const lineColors = generateColors(1);
        const lineData = {
          labels: data.data.map(item => Object.values(item)[0] as string),
          datasets: [{
            label: data.chart_config.y_field || "Value",
            data: data.data.map(item => Object.values(item)[1] as number),
            borderColor: data.chart_config?.border_color || lineColors[0],
            backgroundColor: data.chart_config?.background_color || `${lineColors[0]}33`, // Add 33 for 20% opacity
            tension: 0.1,
          }]
        };
        return <Line data={lineData} options={{ responsive: true, plugins: { legend: { display: false } } }} />;

      case "table":
      default:
        const columns = Object.keys(data.data[0] || {}).map(key => ({
          title: key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
          dataIndex: key,
          key: key,
        }));

        return (
          <Table
            columns={columns}
            dataSource={data.data.map((item, index) => ({ ...item, key: index }))}
            pagination={{ pageSize: 10 }}
            scroll={{ x: 800 }}
          />
        );
    }
  };

  const getTitleStyle = () => {
    const style: React.CSSProperties = {};

    if (data.chart_config?.title_style) {
      const titleStyle = data.chart_config.title_style.toLowerCase();
      if (titleStyle.includes('bold')) {
        style.fontWeight = 'bold';
      }
      if (titleStyle.includes('italic')) {
        style.fontStyle = 'italic';
      }
      if (titleStyle.includes('large')) {
        style.fontSize = '18px';
      }
      if (titleStyle.includes('small')) {
        style.fontSize = '12px';
      }
    }

    if (data.chart_config?.font_weight) {
      style.fontWeight = data.chart_config.font_weight;
    }

    if (data.chart_config?.font_size) {
      style.fontSize = data.chart_config.font_size;
    }

    return style;
  };

  return (
    <Card
      title={
        <span style={getTitleStyle()}>
          {data.title}
        </span>
      }
      extra={onRemove && (
        <Button
          type="text"
          icon={<CloseOutlined />}
          size="small"
          onClick={onRemove}
          title="Remove visualization"
        />
      )}
      style={{ marginBottom: 24 }}
    >
      {renderChart()}
    </Card>
  );
};

export default VisualizationChart;