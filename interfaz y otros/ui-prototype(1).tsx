import React, { useState, useEffect } from 'react';
import { Layout, Menu, Table, Form, Input, Select, Button, DatePicker, Card, Modal, message } from '@/components/ui/shadcn';
import { LineChart, XAxis, YAxis, Tooltip, Legend, Line, ResponsiveContainer } from 'recharts';
import { Users, DollarSign, FileText, Settings, Plus, Edit, Trash, Search } from 'lucide-react';

const { Header, Sider, Content } = Layout;

const App = () => {
  const [collapsed, setCollapsed] = useState(false);
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [form] = Form.useForm();

  const clientesData = [
    { key: '1', cedula: '1234567890', nombre: 'Juan Pérez', tipoPago: 'Contado', fechaRegistro: '2024-09-01' },
    { key: '2', cedula: '0987654321', nombre: 'María López', tipoPago: 'Crédito', fechaRegistro: '2024-09-05' },
    // Más datos...
  ];

  const ventasData = [
    { name: 'Ene', contado: 4000, credito: 2400 },
    { name: 'Feb', contado: 3000, credito: 1398 },
    // Más datos...
  ];

  const columns = [
    { title: 'Cédula/RUC', dataIndex: 'cedula', key: 'cedula' },
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

  const onFinish = (values) => {
    console.log('Success:', values);
    setIsModalVisible(false);
    message.success('Cliente agregado exitosamente');
  };

  const buscarPorCedula = async () => {
    const cedula = form.getFieldValue('cedula');
    // Simulación de llamada a API externa
    const response = await fetch(`https://api-externa.com/buscar?cedula=${cedula}`);
    const data = await response.json();
    if (data) {
      form.setFieldsValue({
        nombre: data.nombre,
        apellido: data.apellido,
        direccion: data.direccion,
        // ... otros campos
      });
      message.success('Datos encontrados y completados automáticamente');
    } else {
      message.error('No se encontraron datos para esta cédula/RUC');
    }
  };

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
            <Card title="Clientes" extra={<Button type="primary" icon={<Plus />} onClick={() => setIsModalVisible(true)}>Agregar Cliente</Button>}>
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
      <Modal title="Agregar Cliente" visible={isModalVisible} onCancel={() => setIsModalVisible(false)} footer={null}>
        <Form form={form} onFinish={onFinish} layout="vertical">
          <Form.Item name="cedula" label="Cédula/RUC" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Button icon={<Search />} onClick={buscarPorCedula}>Buscar</Button>
          <Form.Item name="nombre" label="Nombre" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="apellido" label="Apellido" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="email" label="Correo Electrónico" rules={[{ type: 'email', required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="telefono" label="Teléfono" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="direccion" label="Dirección" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="tipoPago" label="Tipo de Pago" rules={[{ required: true }]}>
            <Select>
              <Select.Option value="contado">Contado</Select.Option>
              <Select.Option value="credito">Crédito</Select.Option>
            </Select>
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit">
              Guardar
            </Button>
          </Form.Item>
        </Form>
      </Modal>
    </Layout>
  );
};

export default App;
