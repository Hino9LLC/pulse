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
import { Table, Alert } from "antd";

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
}

const VisualizationChart: React.FC<VisualizationChartProps> = ({ data }) => {
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
        return <Pie data={pieData} options={{ responsive: true, plugins: { title: { display: true, text: data.title } } }} />;

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
        return <Bar data={barData} options={{ responsive: true, plugins: { title: { display: true, text: data.title } } }} />;

      case "scatter":
        const scatterData = {
          datasets: [{
            label: data.title,
            data: data.data.map(item => ({
              x: Object.values(item)[0] as number,
              y: Object.values(item)[1] as number,
            })),
            backgroundColor: "#36A2EB",
            borderColor: "#36A2EB",
          }]
        };
        return <Scatter data={scatterData} options={{ responsive: true, plugins: { title: { display: true, text: data.title } } }} />;

      case "line":
        const lineData = {
          labels: data.data.map(item => Object.values(item)[0] as string),
          datasets: [{
            label: data.chart_config.y_field || "Value",
            data: data.data.map(item => Object.values(item)[1] as number),
            borderColor: "#36A2EB",
            backgroundColor: "rgba(54, 162, 235, 0.2)",
            tension: 0.1,
          }]
        };
        return <Line data={lineData} options={{ responsive: true, plugins: { title: { display: true, text: data.title } } }} />;

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
            title={() => <h3>{data.title}</h3>}
          />
        );
    }
  };

  return (
    <div style={{ marginBottom: 24 }}>
      {renderChart()}
    </div>
  );
};

export default VisualizationChart;