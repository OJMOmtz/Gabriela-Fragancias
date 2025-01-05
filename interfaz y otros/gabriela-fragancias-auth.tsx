import React, { useState, useEffect } from 'react';
import { Card } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { LogIn, UserCircle, LogOut } from 'lucide-react';

const LoginForm = ({ onLogin }) => {
  const [credentials, setCredentials] = useState({ username: '', password: '' });
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Aquí iría la lógica de autenticación real
      onLogin({ username: credentials.username, role: 'vendedor' });
    } catch (err) {
      setError('Credenciales inválidas');
    }
  };

  return (
    <Card className="w-full max-w-md p-6 bg-white">
      <h2 className="text-2xl font-serif mb-6">Gabriela Fragancias</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium mb-1">Usuario</label>
          <input
            type="text"
            className="w-full p-2 border rounded"
            value={credentials.username}
            onChange={(e) => setCredentials({...credentials, username: e.target.value})}
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Contraseña</label>
          <input
            type="password"
            className="w-full p-2 border rounded"
            value={credentials.password}
            onChange={(e) => setCredentials({...credentials, password: e.target.value})}
          />
        </div>
        {error && (
          <Alert variant="destructive">
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}
        <button
          type="submit"
          className="w-full bg-emerald-600 text-white p-2 rounded hover:bg-emerald-700"
        >
          <LogIn className="inline-block mr-2" size={16} />
          Iniciar Sesión
        </button>
      </form>
    </Card>
  );
};

const PaymentCard = () => {
  const [user, setUser] = useState(null);
  const [payments, setPayments] = useState([
    { control: '28 SEP', fecha: '28-09', entrega: '50.000', saldo: '230.000' },
    { control: '15 OCT', fecha: '05-10', entrega: '40.000', saldo: '190.000' },
    { control: '22 OCT', fecha: '12-10', entrega: '20.000', saldo: '170.000' },
    { control: '28 OCT', fecha: '20-10', entrega: '20.000', saldo: '150.000' },
    { control: '09 NOV', fecha: '02-11', entrega: '20.000', saldo: '130.000' },
  ]);

  const handleLogin = (userData) => {
    setUser(userData);
    // Aquí se podría cargar los datos específicos del vendedor
  };

  const handleLogout = () => {
    setUser(null);
  };

  if (!user) {
    return (
      <div className="min-h-screen bg-gray-100 p-8 flex justify-center items-center">
        <LoginForm onLogin={handleLogin} />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      {/* Header con información de usuario */}
      <div className="max-w-2xl mx-auto mb-4 flex justify-between items-center">
        <div className="flex items-center">
          <UserCircle className="mr-2" />
          <span className="font-mono">{user.username}</span>
        </div>
        <button
          onClick={handleLogout}
          className="text-gray-600 hover:text-gray-800 flex items-center"
        >
          <LogOut className="mr-1" size={16} />
          Cerrar Sesión
        </button>
      </div>

      {/* Contenido original de la tarjeta */}
      <Card className="max-w-2xl mx-auto bg-emerald-50 p-6 relative">
        {/* ... (resto del contenido de la tarjeta igual que antes) ... */}
        
        {/* Agregar registro de actividad */}
        <div className="mt-4 text-xs text-gray-500">
          Última actividad: {new Date().toLocaleString()}
        </div>
      </Card>
    </div>
  );
};

export default PaymentCard;
