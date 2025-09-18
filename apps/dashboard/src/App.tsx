import React, { useState, useEffect } from "react";
import {
  Layout,
  Card,
  Table,
  Tag,
  Statistic,
  Row,
  Col,
  Alert,
  Typography,
  Spin,
} from "antd";
import {
  DatabaseOutlined,
  CheckCircleOutlined,
  ClockCircleOutlined,
  FileTextOutlined,
} from "@ant-design/icons";
import { ThemeSwitcher } from "./components/ThemeSwitcher";
import { companiesAPI } from "./utils/api";
import "./App.css";

const { Header, Content } = Layout;
const { Title } = Typography;

// Format large numbers with M, B, T suffixes
const formatCurrency = (value: number): string => {
  if (value === 0) return "$0";
  if (value >= 1e12) return `$${Math.round(value / 1e12)}T`;
  if (value >= 1e9) return `$${Math.round(value / 1e9)}B`;
  if (value >= 1e6) return `$${Math.round(value / 1e6)}M`;
  if (value >= 1e3) return `$${Math.round(value / 1e3)}K`;
  return `$${value.toLocaleString()}`;
};

const formatNumber = (value: number | null): string => {
  if (value === null || value === 0) return "0";
  if (value >= 1e6) return `${Math.round(value / 1e6)}M`;
  if (value >= 1e3) return `${Math.round(value / 1e3)}K`;
  return value.toLocaleString();
};

interface Company {
  id: number;
  uuid: string;
  company_name: string;
  founded_year: number;
  headquarters: string;
  industry: string;
  total_funding_usd: number;
  arr_usd: number;
  valuation_usd: number;
  employee_count: number | null;
  top_investors: string;
  product: string;
  g2_rating: number;
  created_at: string;
  updated_at: string;
}

function App() {
  const [companies, setCompanies] = useState<Company[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchCompanies();
  }, []);

  const fetchCompanies = async () => {
    try {
      setIsLoading(true);
      const data = await companiesAPI.getCompanies();
      setCompanies(data);
    } catch (error) {
      console.error("Failed to fetch companies:", error);
    } finally {
      setIsLoading(false);
    }
  };


  const columns = [
    {
      title: "Company",
      dataIndex: "company_name",
      key: "company_name",
      render: (text: string) => <strong>{text}</strong>,
      width: 200,
    },
    {
      title: "Industry",
      dataIndex: "industry",
      key: "industry",
      width: 150,
    },
    {
      title: "Founded",
      dataIndex: "founded_year",
      key: "founded_year",
      width: 100,
    },
    {
      title: "Headquarters",
      dataIndex: "headquarters",
      key: "headquarters",
      width: 200,
    },
    {
      title: "Total Funding",
      dataIndex: "total_funding_usd",
      key: "total_funding_usd",
      width: 120,
      render: (value: number) => formatCurrency(value),
    },
    {
      title: "Valuation",
      dataIndex: "valuation_usd",
      key: "valuation_usd",
      width: 120,
      render: (value: number) => formatCurrency(value),
    },
    {
      title: "ARR",
      dataIndex: "arr_usd",
      key: "arr_usd",
      width: 120,
      render: (value: number) => formatCurrency(value),
    },
    {
      title: "Employees",
      dataIndex: "employee_count",
      key: "employee_count",
      width: 120,
      render: (value: number | null) => formatNumber(value),
    },
    {
      title: "G2 Rating",
      dataIndex: "g2_rating",
      key: "g2_rating",
      width: 100,
      render: (rating: number) => <Tag color="blue">{rating}/5</Tag>,
    },
    {
      title: "Top Investors",
      dataIndex: "top_investors",
      key: "top_investors",
      ellipsis: true,
      width: 250,
    },
    {
      title: "Product",
      dataIndex: "product",
      key: "product",
      ellipsis: true,
      width: 200,
    },
  ];


  return (
    <Layout style={{ minHeight: "100vh" }}>
      <Header
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          padding: "0 24px",
          boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
        }}
      >
        <Title
          level={2}
          style={{
            margin: 0,
            color: "#1890ff",
            textShadow: "none",
          }}
        >
          <DatabaseOutlined /> SaaS Companies Explorer
        </Title>
        <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
          <ThemeSwitcher />
        </div>
      </Header>

      <Content>
        <div style={{ maxWidth: 1200, margin: "0 auto", padding: "24px" }}>

          {/* Statistics Cards */}
          <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
            <Col xs={24} sm={12} md={6}>
              <Card>
                <Statistic
                  title="Total Companies"
                  value={companies.length}
                  prefix={<DatabaseOutlined />}
                  valueStyle={{ color: "#1890ff" }}
                />
              </Card>
            </Col>
            <Col xs={24} sm={12} md={6}>
              <Card>
                <Statistic
                  title="Unique Industries"
                  value={new Set(companies.map(c => c.industry)).size}
                  prefix={<FileTextOutlined />}
                  valueStyle={{ color: "#52c41a" }}
                />
              </Card>
            </Col>
            <Col xs={24} sm={12} md={6}>
              <Card>
                <Statistic
                  title="Avg G2 Rating"
                  value={(companies.reduce((sum, c) => sum + c.g2_rating, 0) / companies.length || 0).toFixed(1)}
                  prefix={<CheckCircleOutlined />}
                  valueStyle={{ color: "#faad14" }}
                />
              </Card>
            </Col>
            <Col xs={24} sm={12} md={6}>
              <Card>
                <Statistic
                  title="Founded Since 2000"
                  value={companies.filter((c) => c.founded_year >= 2000).length}
                  prefix={<ClockCircleOutlined />}
                  valueStyle={{ color: "#722ed1" }}
                />
              </Card>
            </Col>
          </Row>

          {/* Main Content */}
          <Card title="Top 100 SaaS Companies 2025" style={{ marginBottom: 24 }}>
            {isLoading ? (
              <div style={{ textAlign: "center", padding: "50px" }}>
                <Spin size="large" />
                <p style={{ marginTop: 16 }}>Loading companies...</p>
              </div>
            ) : (
              <Table
                columns={columns}
                dataSource={companies}
                rowKey="id"
                pagination={{ pageSize: 10 }}
                scroll={{ x: 1800 }}
                locale={{
                  emptyText:
                    "No companies found.",
                }}
              />
            )}
          </Card>

          {/* Info Alert */}
          <Alert
            message="SaaS Companies Explorer"
            description={
              <div>
                This dashboard displays data from the Top 100 SaaS Companies 2025 dataset.
                The data is served by a FastAPI backend at{" "}
                <code>http://localhost:8200</code> and includes company metrics like
                funding, valuation, ARR, and G2 ratings.
                <br />
                <strong>Phase 1 & 2 Complete - Ready for natural language visualization features!</strong>
              </div>
            }
            type="success"
            showIcon
            style={{ marginTop: 16 }}
          />
        </div>
      </Content>
    </Layout>
  );
}

export default App;
