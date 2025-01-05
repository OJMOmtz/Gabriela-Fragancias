import React, { useState } from 'react';
import { Layout, Menu, Table, Form, Input, Select, Button, DatePicker, Card } from '@/components/ui/shadcn';
import { LineChart, XAxis, YAxis, Tooltip, Legend, Line, ResponsiveContainer } from 'recharts';
import { Users, DollarSign, FileText, Settings, Plus, Edit, Trash } from 'lucide-react';

const { Header, Sider, Content } = Layout;

const App = () => {
  const [collapsed, setCollapsed] = useState(false);

  const clientesData = [
    { key: '1', nombre: 'Juan Pérez', tipoPago: 'Contado', fechaRegistro: '2024-09-01' },
    { key: '2', nombre: 'María López', tipoPago: 'Crédito', fechaRegistro: '2024-09-05' },
    // Más datos...
  ];

  const ventasData = [
    { name: 'Ene', contado: 4000, credito: 2400 },
    { name: 'Feb', contado: 3000, credito: 1398 },
    // Más datos...
  ];

  const columns = [
    { title: 'Nombre', dataIndex: 'nombre', key: 'nombre' },
    { title: 'Tipo de Pago', dataIndex: 'tipoPago', key: 'tipoPago' },
    { title: 'Fecha de Registro', dataIndex: 'fechaRegistro', key: 'fechaRegistro' },
    {
      title: 'Acciones',
      key: 'acciones',
      render: () => (
        <>
          <Button icon={<Edit />} size="small" className="mr-2" />
          <Button icon={<Trash />} size="small" danger />
        </>
      ),
    },
  ];

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sider collapsible collapsed={collapsed} onCollapse={setCollapsed}>
        <div className="logo" />
        <Menu theme="dark" defaultSelectedKeys={['1']} mode="inline">
          <Menu.Item key="1" icon={<Users />}>
            Clientes
          </Menu.Item>
          <Menu.Item key="2" icon={<DollarSign />}>
            Ventas
          </Menu.Item>
          <Menu.Item key="3" icon={<FileText />}>
            Reportes
          </Menu.Item>
          <Menu.Item key="4" icon={<Settings />}>
            Configuración
          </Menu.Item>
        </Menu>
      </Sider>
      <Layout className="site-layout">
        <Header className="site-layout-background" style={{ padding: 0 }} />
        <Content style={{ margin: '0 16px' }}>
          <div className="site-layout-background" style={{ padding: 24, minHeight: 360 }}>
            <Card title="Clientes" extra={<Button type="primary" icon={<Plus />}>Agregar Cliente</Button>}>
              <Table dataSource={clientesData} columns={columns} />
            </Card>
            <Card title="Ventas" style={{ marginTop: 16 }}>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={ventasData}>
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="contado" stroke="#8884d8" />
                  <Line type="monotone" dataKey="credito" stroke="#82ca9d" />
                </LineChart>
              </ResponsiveContainer>
            </Card>
          </div>
        </Content>
      </Layout>
    </Layout>
  );
};

export default App;
