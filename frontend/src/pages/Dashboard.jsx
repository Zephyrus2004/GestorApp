import React, { useEffect, useState } from 'react'
import { useAuth } from '../context/AuthContext'
import client from '../api/client'
import { BiBox, BiCategory, BiGroup, BiError, BiTrendingUp } from 'react-icons/bi'

const Dashboard = () => {
  const { user } = useAuth()
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const res = await client.get('/api/dashboard/stats/')
        setStats(res.data)
      } catch (err) {
        console.error('Error al cargar estadísticas', err)
      } finally {
        setLoading(false)
      }
    }
    fetchStats()
  }, [])

  if (loading) {
    return (
      <div style={{ display: 'flex', flex: 1, alignItems: 'center', justifyContent: 'center', height: '60vh' }}>
        <div className="spinner"></div>
      </div>
    )
  }

  const userRole = user.profile?.rol || 'usuario'
  const isSuper = user.is_staff || userRole === 'admin'

  return (
    <div>
      <div className="page-header">
        <div className="page-title">
          <h2>Panel de Control</h2>
          <p>Bienvenido de nuevo, {user.full_name}.</p>
        </div>
      </div>

      {userRole === 'admin' || isSuper ? (
        <>
          <div className="stats-grid">
            <div className="glass-card stat-card">
              <div className="stat-info">
                <h3>Total Usuarios</h3>
                <p>{stats?.total_usuarios || 0}</p>
              </div>
              <div className="stat-icon accent">
                <BiGroup />
              </div>
            </div>
            <div className="glass-card stat-card">
              <div className="stat-info">
                <h3>Total Productos</h3>
                <p>{stats?.total_productos || 0}</p>
              </div>
              <div className="stat-icon">
                <BiBox />
              </div>
            </div>
            <div className="glass-card stat-card">
              <div className="stat-info">
                <h3>Total Categorías</h3>
                <p>{stats?.total_categorias || 0}</p>
              </div>
              <div className="stat-icon secondary">
                <BiCategory />
              </div>
            </div>
          </div>

          <div className="dashboard-sections">
            <div className="glass-card list-panel">
              <h3>Productos Recientes</h3>
              <div className="table-container">
                <table className="custom-table">
                  <thead>
                    <tr>
                      <th>Nombre</th>
                      <th>Marca / Modelo</th>
                      <th>Precio</th>
                      <th>Stock</th>
                    </tr>
                  </thead>
                  <tbody>
                    {stats?.productos_recientes?.map((p) => (
                      <tr key={p.id}>
                        <td style={{ fontWeight: 600 }}>{p.nombre}</td>
                        <td>{p.marca} {p.modelo}</td>
                        <td>${p.precio}</td>
                        <td>
                          <span className={`badge ${p.stock <= 5 ? 'badge-visitante' : 'badge-gestor'}`}>
                            {p.stock} unid.
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            <div className="glass-card list-panel">
              <h3>Usuarios Recientes</h3>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                {stats?.usuarios_recientes?.map((u) => (
                  <div key={u.id} style={{ display: 'flex', alignItems: 'center', gap: '12px', borderBottom: '1px solid rgba(255,255,255,0.03)', paddingBottom: '12px' }}>
                    <div className="user-avatar" style={{ width: '36px', height: '36px', fontSize: '14px' }}>
                      <BiGroup />
                    </div>
                    <div style={{ flex: 1, minWidth: 0 }}>
                      <h4 style={{ fontSize: '13px', fontWeight: 600, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{u.full_name}</h4>
                      <p style={{ fontSize: '11px', color: 'var(--text-secondary)' }}>@{u.username}</p>
                    </div>
                    <span className={`badge badge-${u.profile?.rol || 'usuario'}`} style={{ fontSize: '9px', padding: '2px 8px' }}>
                      {u.profile?.rol_display || 'Usuario'}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </>
      ) : userRole === 'gestor' ? (
        <>
          <div className="stats-grid">
            <div className="glass-card stat-card">
              <div className="stat-info">
                <h3>Total Productos</h3>
                <p>{stats?.total_productos || 0}</p>
              </div>
              <div className="stat-icon">
                <BiBox />
              </div>
            </div>
            <div className="glass-card stat-card">
              <div className="stat-info">
                <h3>Total Categorías</h3>
                <p>{stats?.total_categorias || 0}</p>
              </div>
              <div className="stat-icon secondary">
                <BiCategory />
              </div>
            </div>
            <div className="glass-card stat-card">
              <div className="stat-info">
                <h3>Bajo Stock</h3>
                <p>{stats?.productos_bajo_stock?.length || 0}</p>
              </div>
              <div className="stat-icon accent">
                <BiError />
              </div>
            </div>
          </div>

          <div className="dashboard-sections" style={{ gridTemplateColumns: '1fr 1fr' }}>
            <div className="glass-card list-panel">
              <h3>Productos Recientes</h3>
              <div className="table-container">
                <table className="custom-table">
                  <thead>
                    <tr>
                      <th>Nombre</th>
                      <th>Marca / Modelo</th>
                      <th>Precio</th>
                    </tr>
                  </thead>
                  <tbody>
                    {stats?.productos_recientes?.map((p) => (
                      <tr key={p.id}>
                        <td style={{ fontWeight: 600 }}>{p.nombre}</td>
                        <td>{p.marca} {p.modelo}</td>
                        <td>${p.precio}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            <div className="glass-card list-panel">
              <h3>Alertas de Bajo Stock</h3>
              <div className="table-container">
                <table className="custom-table">
                  <thead>
                    <tr>
                      <th>Producto</th>
                      <th>Stock</th>
                      <th>Estado</th>
                    </tr>
                  </thead>
                  <tbody>
                    {stats?.productos_bajo_stock?.map((p) => (
                      <tr key={p.id}>
                        <td style={{ fontWeight: 600, color: 'var(--accent)' }}>{p.nombre}</td>
                        <td>
                          <span className="badge badge-visitante">{p.stock} unid.</span>
                        </td>
                        <td>
                          <span className="badge badge-admin">{p.estado}</span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </>
      ) : (
        <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', padding: '40px', textAlign: 'center' }}>
          <BiTrendingUp size={48} style={{ color: 'var(--primary)', marginBottom: '16px' }} />
          <h3>Sección General</h3>
          <p style={{ color: 'var(--text-secondary)', marginTop: '8px', maxWidth: '500px' }}>
            {stats?.mensaje || 'Has iniciado sesión en el sistema. Puedes consultar el catálogo completo de productos en la sección "Productos" del menú lateral.'}
          </p>
          {userRole === 'usuario' && (
            <div className="stats-grid" style={{ marginTop: '30px', width: '100%', maxWidth: '600px' }}>
              <div className="glass-card stat-card" style={{ background: 'rgba(255,255,255,0.01)' }}>
                <div className="stat-info">
                  <h3>Equipos Disponibles</h3>
                  <p>{stats?.productos_disponibles || 0}</p>
                </div>
                <div className="stat-icon">
                  <BiBox />
                </div>
              </div>
              <div className="glass-card stat-card" style={{ background: 'rgba(255,255,255,0.01)' }}>
                <div className="stat-info">
                  <h3>Mis Asignaciones Activas</h3>
                  <p>{stats?.tus_asignaciones_activas || 0}</p>
                </div>
                <div className="stat-icon secondary">
                  <BiTrendingUp />
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default Dashboard
