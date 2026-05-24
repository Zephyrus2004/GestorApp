import React from 'react'
import { Navigate, Outlet } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

const ProtectedRoute = ({ allowedRoles = [] }) => {
  const { user, token, loading } = useAuth()

  if (loading) {
    return (
      <div className="loading-screen">
        <div className="spinner"></div>
        <p>Cargando sesión...</p>
      </div>
    )
  }

  if (!token || !user) {
    return <Navigate to="/login" replace />
  }

  const userRole = user.profile?.rol || 'usuario'
  
  // Superusers always have full access
  if (user.is_staff || userRole === 'admin') {
    return <Outlet />
  }

  if (allowedRoles.length > 0 && !allowedRoles.includes(userRole)) {
    return <Navigate to="/unauthorized" replace />
  }

  return <Outlet />
}

export default ProtectedRoute
