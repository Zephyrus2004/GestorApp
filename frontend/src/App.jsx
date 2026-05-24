import React from 'react'
import { BrowserRouter, Routes, Route, Navigate, Link } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import { AuthProvider } from './context/AuthContext'
import ProtectedRoute from './components/ProtectedRoute'
import Layout from './components/Layout'

// Pages
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import ProductoList from './pages/productos/ProductoList'
import ProductoDetail from './pages/productos/ProductoDetail'
import ProductoForm from './pages/productos/ProductoForm'
import CategoriaList from './pages/categorias/CategoriaList'
import CategoriaForm from './pages/categorias/CategoriaForm'
import UsuarioList from './pages/usuarios/UsuarioList'
import UsuarioForm from './pages/usuarios/UsuarioForm'

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
      <AuthProvider>
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
          <Route path="/login" element={<Login />} />
          
          {/* Protected Routes */}
          <Route element={<ProtectedRoute />}>
            <Route element={<Layout />}>
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/productos" element={<ProductoList />} />
              <Route path="/productos/:id" element={<ProductoDetail />} />
              <Route path="/unauthorized" element={<Unauthorized />} />
              
              {/* Gestor and Admin only */}
              <Route element={<ProtectedRoute allowedRoles={['admin', 'gestor']} />}>
                <Route path="/productos/nuevo" element={<ProductoForm />} />
                <Route path="/productos/:id/editar" element={<ProductoForm />} />
                <Route path="/categorias" element={<CategoriaList />} />
                <Route path="/categorias/nueva" element={<CategoriaForm />} />
              </Route>

              {/* Admin only */}
              <Route element={<ProtectedRoute allowedRoles={['admin']} />}>
                <Route path="/usuarios" element={<UsuarioList />} />
                <Route path="/usuarios/nuevo" element={<UsuarioForm />} />
                <Route path="/usuarios/:id/editar" element={<UsuarioForm />} />
              </Route>
            </Route>
          </Route>

          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  )
}

export default App
