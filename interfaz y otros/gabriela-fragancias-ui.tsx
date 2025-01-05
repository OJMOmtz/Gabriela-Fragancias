import React, { useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Camera, User, Search, Home, Users, ShoppingBag, BarChart2, Settings, Truck, Package, DollarSign } from 'lucide-react';

const data = [
  { name: 'Ene', ventas: 4000 },
  { name: 'Feb', ventas: 3000 },
  { name: 'Mar', ventas: 5000 },
  { name: 'Abr', ventas: 4500 },
  { name: 'May', ventas: 6000 },
  { name: 'Jun', ventas: 5500 },
];

const Dashboard = () => {
  const [activeTab, setActiveTab] = useState('inicio');

  return (
    <div className="flex h-screen bg-[#D1EFD7] text-[#3A684D] font-['FiraSans-Regular']">
      {/* Sidebar */}
      <div className="w-64 bg-[#5CA47A] p-5 flex flex-col">
        <div className="mb-10">
          <img src="/api/placeholder/200/100" alt="Gabriela Fragancias Logo" className="w-full" />
        </div>
        <nav className="flex-1">
          {[
            { icon: Home, label: 'Inicio', id: 'inicio' },
            { icon: Users, label: 'Clientes', id: 'clientes' },
            { icon: ShoppingBag, label: 'Ventas', id: 'ventas' },
            { icon: Package, label: 'Inventario', id: 'inventario' },
            { icon: Truck, label: 'Vehículos', id: 'vehiculos' },
            { icon: DollarSign, label: 'Liquidaciones', id: 'liquidaciones' },
            { icon: BarChart2, label: 'Reportes', id: 'reportes' },
            { icon: Settings, label: 'Configuración', id: 'configuracion' },
          ].map(({ icon: Icon, label, id }) => (
            <button
              key={id}
              onClick={() => setActiveTab(id)}
              className={`flex items-center space-x-3 p-2 w-full text-left mb-2 rounded ${
                activeTab === id ? 'bg-[#D678B6] text-white' : 'text-white hover:bg-[#3A684D]'
              }`}
            >
              <Icon size={20} />
              <span>{label}</span>
            </button>
          ))}
        </nav>
      </div>

      {/* Main content */}
      <div className="flex-1 p-10 overflow-auto">
        {/* Header */}
        <header className="flex justify-between items-center mb-10">
          <h1 className="text-3xl font-['FiraSans-Bold']">Dashboard</h1>
          <div className="flex items-center space-x-4">
            <div className="relative">
              <input
                type="text"
                placeholder="Buscar..."
                className="pl-10 pr-4 py-2 rounded-full bg-white text-[#3A684D]"
              />
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-[#5CA47A]" size={20} />
            </div>
            <button className="bg-[#5CA47A] text-white p-2 rounded-full">
              <User size={20} />
            </button>
          </div>
        </header>

        {/* Dashboard content */}
        <div className="grid grid-cols-3 gap-6 mb-10">
          {['Ventas Totales', 'Nuevos Clientes', 'Productos Vendidos', 'Liquidaciones Pendientes', 'Vehículos en Ruta', 'Kits Vendidos'].map((title) => (
            <div key={title} className="bg-white p-6 rounded-lg shadow">
              <h3 className="text-xl mb-2 font-['FiraSans-Bold']">{title}</h3>
              <p className="text-3xl text-[#D678B6]">
                {Math.floor(Math.random() * 1000)}
                {title === 'Ventas Totales' && ' Gs'}
              </p>
            </div>
          ))}
        </div>

        {/* Charts */}
        <div className="grid grid-cols-2 gap-6">
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-xl mb-4 font-['FiraSans-Bold']">Ventas por Mes</h3>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={data}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="ventas" stroke="#D678B6" />
              </LineChart>
            </ResponsiveContainer>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-xl mb-4 font-['FiraSans-Bold']">Productos Más Vendidos</h3>
            {/* Placeholder for products chart */}
            <div className="h-[300px] bg-[#D1EFD7] flex items-center justify-center">
              <p>Gráfico de Productos Más Vendidos</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
