import React from 'react'
import { NavLink, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { 
  BiSolidDashboard, 
  BiBox, 
  BiCategory, 
  BiGroup, 
  BiLogOut, 
  BiUser, 
  BiLaptop 
} from 'react-icons/bi'

const Sidebar = () => {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  if (!user) return null

  const userRole = user.profile?.rol || 'usuario'
  const isGestorOrAdmin = user.is_staff || ['admin', 'gestor'].includes(userRole)
  const isAdmin = user.is_staff || userRole === 'admin'

  const handleLogout = async () => {
    await logout()
    navigate('/login')
  }

  return (
    <aside className="sidebar">
      <NavLink to="/dashboard" className="sidebar-brand">
        <div className="brand-logo">
          <BiLaptop />
        </div>
        <div className="brand-text">
          <h1>InfoTech Shop</h1>
          <span>TIENDA IT</span>
        </div>
      </NavLink>

      <ul className="sidebar-nav">
        <li>
          <NavLink to="/dashboard" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
            <BiSolidDashboard size={20} />
            <span>Dashboard</span>
          </NavLink>
        </li>
        <li>
          <NavLink to="/productos" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
            <BiBox size={20} />
            <span>Productos</span>
          </NavLink>
        </li>
        {isGestorOrAdmin && (
          <li>
            <NavLink to="/categorias" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
              <BiCategory size={20} />
              <span>Categorías</span>
            </NavLink>
          </li>
        )}
        {isAdmin && (
          <li>
            <NavLink to="/usuarios" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
              <BiGroup size={20} />
              <span>Usuarios</span>
            </NavLink>
          </li>
        )}
      </ul>

      <div className="sidebar-user">
        <div className="user-avatar">
          {user.profile?.avatar ? (
            <img src={user.profile.avatar.startsWith('http') ? user.profile.avatar : `http://localhost:8000${user.profile.avatar}`} alt="Avatar" />
          ) : (
            <BiUser />
          )}
        </div>
        <div className="user-info">
          <h3>{user.full_name}</h3>
          <span className={`badge badge-${userRole}`}>
            {user.profile?.rol_display || 'Usuario'}
          </span>
        </div>
        <button onClick={handleLogout} className="logout-btn" title="Cerrar Sesión">
          <BiLogOut />
        </button>
      </div>
    </aside>
  )
}

export default Sidebar
