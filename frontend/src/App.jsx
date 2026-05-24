// ==============================================================================
// SECCIÓN: RUTEO Y COMPONENTE PRINCIPAL (REACT APP)
// ==============================================================================
// Este es el punto de entrada de la interfaz de React. Configura el ruteo del lado del
// cliente mediante React Router, el proveedor de autenticación global (AuthProvider)
// y los niveles de protección para restringir páginas según el rol del usuario.

import React from 'react'
import { BrowserRouter, Routes, Route, Navigate, Link } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import { AuthProvider } from './context/AuthContext'
import ProtectedRoute from './components/ProtectedRoute'
import Layout from './components/Layout'

// Páginas de la aplicación (Pages)
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import ProductoList from './pages/productos/ProductoList'
import ProductoDetail from './pages/productos/ProductoDetail'
import ProductoForm from './pages/productos/ProductoForm'
import CategoriaList from './pages/categorias/CategoriaList'
import CategoriaForm from './pages/categorias/CategoriaForm'
import UsuarioList from './pages/usuarios/UsuarioList'
import UsuarioForm from './pages/usuarios/UsuarioForm'

/**
 * Componente renderizado en caso de que un usuario intente ingresar 
 * a una página para la cual no tiene el rol necesario.
 */
const Unauthorized = () => (
  <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '80vh', textAlign: 'center' }}>
    <h2 style={{ fontSize: '32px', color: 'var(--danger)', marginBottom: '16px' }}>Acceso Denegado</h2>
    <p style={{ color: 'var(--text-secondary)' }}>No tienes permisos para acceder a esta sección.</p>
    <Link to="/dashboard" className="btn btn-primary" style={{ marginTop: '20px' }}>
      Volver al Inicio
    </Link>
  </div>
)

function App() {
  return (
    <BrowserRouter>
      {/* AuthProvider suministra el estado del usuario logueado (user, token, login, logout) a toda la app */}
      <AuthProvider>
        {/* Componente global para renderizar notificaciones dinámicas (toasts) en pantalla */}
        <Toaster 
          position="top-right" 
          toastOptions={{
            style: {
              background: '#0d1423',
              color: '#f3f4f6',
              border: '1px solid rgba(255,255,255,0.08)',
              borderRadius: '10px',
              fontFamily: 'Inter, sans-serif',
            }
          }} 
        />
        <Routes>
          {/* Ruta pública: Inicio de sesión */}
          <Route path="/login" element={<Login />} />
          
          {/* ------------------------------------------------------------------
              RUTAS PROTEGIDAS (Requieren inicio de sesión básico)
             ------------------------------------------------------------------ */}
          <Route element={<ProtectedRoute />}>
            {/* El componente Layout define la barra lateral (Sidebar) y la estructura visual global */}
            <Route element={<Layout />}>
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/productos" element={<ProductoList />} />
              <Route path="/productos/:id" element={<ProductoDetail />} />
              <Route path="/unauthorized" element={<Unauthorized />} />
              
              {/* RUTAS EXCLUSIVAS: Gestor y Administrador solamente */}
              <Route element={<ProtectedRoute allowedRoles={['admin', 'gestor']} />}>
                <Route path="/productos/nuevo" element={<ProductoForm />} />
                <Route path="/productos/:id/editar" element={<ProductoForm />} />
                <Route path="/categorias" element={<CategoriaList />} />
                <Route path="/categorias/nueva" element={<CategoriaForm />} />
              </Route>

              {/* RUTAS EXCLUSIVAS: Únicamente Administrador */}
              <Route element={<ProtectedRoute allowedRoles={['admin']} />}>
                <Route path="/usuarios" element={<UsuarioList />} />
                <Route path="/usuarios/nuevo" element={<UsuarioForm />} />
                <Route path="/usuarios/:id/editar" element={<UsuarioForm />} />
              </Route>
            </Route>
          </Route>

          {/* Redirección por defecto: Cualquier URL no válida se redirige al Dashboard */}
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  )
}

export default App

