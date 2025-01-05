.
├── public/
│   ├── index.html
│   └── favicon.ico
├── src/
│   ├── components/
│   │   ├── Layout/
│   │   │   ├── Sidebar.tsx
│   │   │   └── Header.tsx
│   │   ├── Auth/
│   │   │   ├── Login.tsx
│   │   │   └── Register.tsx
│   │   ├── Productos/
│   │   │   ├── ListaProductos.tsx
│   │   │   └── FormProducto.tsx
│   │   ├── Clientes/
│   │   │   ├── ListaClientes.tsx
│   │   │   └── FormCliente.tsx
│   │   └── Ventas/
│   │       ├── ListaVentas.tsx
│   │       └── FormVenta.tsx
│   ├── pages/
│   │   ├── Dashboard.tsx
│   │   ├── Productos.tsx
│   │   ├── Clientes.tsx
│   │   └── Ventas.tsx
│   ├── services/
│   │   ├── authService.ts
│   │   ├── productoService.ts
│   │   ├── clienteService.ts
│   │   └── ventaService.ts
│   ├── context/
│   │   └── AuthContext.tsx
│   ├── types/
│   │   ├── Usuario.ts
│   │   ├── Producto.ts
│   │   ├── Cliente.ts
│   │   └── Venta.ts
│   ├── utils/
│   │   ├── formatters.ts
│   │   └── validators.ts
│   ├── styles/
│   │   └── global.css
│   ├── App.tsx
│   └── index.tsx
├── package.json
├── tsconfig.json
└── tailwind.config.js

# package.json
{
  "name": "gabriela-fragancias-frontend",
  "version": "1.0.0",
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.22.0",
    "axios": "^1.6.7",
    "zustand": "^4.5.0",
    "tailwindcss": "^3.4.1",
    "shadcn-ui": "^0.8.0"
  },
  "devDependencies": {
    "typescript": "^5.3.3",
    "@types/react": "^18.2.48"
  }
}

# src/types/Usuario.ts
export interface Usuario {
  id: number;
  nombre: string;
  apellido: string;
  cedula: string;
  email: string;
  estado: 'activo' | 'inactivo' | 'eliminado';
  created_at: Date;
}

# src/services/authService.ts
import axios from 'axios';

const API_URL = '/api/usuarios';

export const authService = {
  login: async (email: string, password: string) => {
    const response = await axios.post(`${API_URL}/login`, { email, password });
    if (response.data.token) {
      localStorage.setItem('user', JSON.stringify(response.data));
    }
    return response.data;
  },
  
  logout: () => {
    localStorage.removeItem('user');
  },

  register: async (userData: {
    nombre: string, 
    apellido: string, 
    cedula: string, 
    email: string, 
    password: string
  }) => {
    return axios.post(`${API_URL}/registro`, userData);
  }
}

# src/components/Auth/Login.tsx
import React, { useState } from 'react';
import { authService } from '../../services/authService';

export const Login: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await authService.login(email, password);
      // Redirigir al dashboard
    } catch (error) {
      // Manejar error de login
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full space-y-8">
        <form onSubmit={handleLogin} className="mt-8 space-y-6">
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            placeholder="Correo electrónico"
            className="appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300"
          />
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            placeholder="Contraseña"
            className="appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300"
          />
          <button
            type="submit"
            className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
          >
            Iniciar Sesión
          </button>
        </form>
      </div>
    </div>
  );
};
