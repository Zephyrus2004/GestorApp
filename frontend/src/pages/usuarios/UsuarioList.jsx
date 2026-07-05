import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import client from '../../api/client'
import { BiPlus, BiEdit, BiTrash } from 'react-icons/bi'
import toast from 'react-hot-toast'

const UsuarioList = () => {
  const [usuarios, setUsuarios] = useState([])
  const [loading, setLoading] = useState(true)

  const fetchUsuarios = async () => {
    try {
      setLoading(true)
      const res = await client.get('/api/users/')
      setUsuarios(res.data.results || res.data)
    } catch (err) {
      toast.error('Error al cargar usuarios.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchUsuarios()
  }, [])

  const handleDelete = async (id, name) => {
    if (window.confirm(`¿Estás seguro de que deseas eliminar el usuario "${name}"?`)) {
      try {
        await client.delete(`/api/users/${id}/`)
        toast.success('Usuario eliminado.')
        fetchUsuarios()
      } catch (err) {
        toast.error('No se pudo eliminar el usuario.')
      }
    }
  }

  return (
    <div>
      <div className="page-header">
        <div className="page-title">
          <h2>Gestión de Usuarios</h2>
          <p>Administra los roles, cuentas y perfiles de acceso.</p>
        </div>
        <Link to="/usuarios/nuevo" className="btn btn-primary">
          <BiPlus size={18} /> Nuevo Usuario
        </Link>
      </div>

      {loading ? (
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '30vh' }}>
          <div className="spinner"></div>
        </div>
      ) : (
        <div className="glass-card" style={{ padding: 0 }}>
          <div className="table-container">
            <table className="custom-table">
              <thead>
                <tr>
                  <th>Nombre Completo</th>
                  <th>Usuario</th>
                  <th>Correo Electrónico</th>
                  <th>Departamento</th>
                  <th>Teléfono</th>
                  <th>Rol</th>
                  <th>Estado</th>
                  <th style={{ textAlign: 'right' }}>Acciones</th>
                </tr>
              </thead>
              <tbody>
                {usuarios.map((u) => {
                  const rol = u.profile?.rol || 'usuario'
                  return (
                    <tr key={u.id}>
                      <td style={{ fontWeight: 600 }}>{u.full_name}</td>
                      <td>@{u.username}</td>
                      <td>{u.email}</td>
                      <td>{u.profile?.departamento || '-'}</td>
                      <td>{u.profile?.telefono || '-'}</td>
                      <td>
                        <span className={`badge badge-${rol}`}>
                          {u.profile?.rol_display || 'Usuario'}
                        </span>
                      </td>
                      <td>
                        <span className={`badge ${u.is_active ? 'badge-gestor' : 'badge-visitante'}`}>
                          {u.is_active ? 'Activo' : 'Inactivo'}
                        </span>
                      </td>
                      <td className="actions-cell">
                        <Link to={`/usuarios/${u.id}/editar`} className="action-btn" title="Editar">
                          <BiEdit size={18} />
                        </Link>
                        <button 
                          onClick={() => handleDelete(u.id, u.full_name)} 
                          className="action-btn danger-hover" 
                          title="Eliminar"
                        >
                          <BiTrash size={18} />
                        </button>
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  )
}

export default UsuarioList
