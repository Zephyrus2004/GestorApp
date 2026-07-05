import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import client from '../../api/client'
import { useAuth } from '../../context/AuthContext'
import { BiPlus, BiTrash, BiFolder, BiDesktop, BiPrinter, BiTransferAlt, BiChip, BiFile } from 'react-icons/bi'
import toast from 'react-hot-toast'

// Map icon string to actual React Icon
const getIcon = (iconName) => {
  switch (iconName) {
    case 'bi-laptop': return <BiDesktop />
    case 'bi-printer': return <BiPrinter />
    case 'bi-router': return <BiTransferAlt />
    case 'bi-cpu': return <BiChip />
    case 'bi-file-earmark-code': return <BiFile />
    default: return <BiFolder />
  }
}

const CategoriaList = () => {
  const { user } = useAuth()
  const [categorias, setCategorias] = useState([])
  const [loading, setLoading] = useState(true)

  const userRole = user.profile?.rol || 'usuario'
  const isGestorOrAdmin = user.is_staff || ['admin', 'gestor'].includes(userRole)
  const isAdmin = user.is_staff || userRole === 'admin'

  const fetchCategorias = async () => {
    try {
      setLoading(true)
      const res = await client.get('/api/categorias/')
      setCategorias(res.data.results || res.data)
    } catch (err) {
      toast.error('Error al cargar categorías.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchCategorias()
  }, [])

  const handleDelete = async (id, nombre) => {
    if (!window.confirm(`¿Estás seguro de que deseas eliminar la categoría "${nombre}"? Los productos que pertenezcan a ella podrían bloquear la eliminación.`)) return
    try {
      await client.delete(`/api/categorias/${id}/`)
      toast.success('Categoría eliminada.')
      fetchCategorias()
    } catch (err) {
      toast.error('No se pudo eliminar. Verifique que no contenga productos asociados.')
    }
  }

  return (
    <div>
      <div className="page-header">
        <div className="page-title">
          <h2>Categorías de Productos</h2>
          <p>Organiza e identifica los insumos de tecnología en la tienda.</p>
        </div>
        {isGestorOrAdmin && (
          <Link to="/categorias/nueva" className="btn btn-primary">
            <BiPlus size={18} /> Nueva Categoría
          </Link>
        )}
      </div>

      {loading ? (
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '30vh' }}>
          <div className="spinner"></div>
        </div>
      ) : (
        <div className="stats-grid" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))' }}>
          {categorias.length === 0 ? (
            <div className="glass-card" style={{ gridColumn: '1 / -1', textAlign: 'center', padding: '40px' }}>
              No hay categorías creadas actualmente.
            </div>
          ) : (
            categorias.map((c) => (
              <div className="glass-card" key={c.id} style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
                <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', marginBottom: '20px' }}>
                  <div className="stat-icon" style={{ fontSize: '28px', width: '56px', height: '56px' }}>
                    {getIcon(c.icono)}
                  </div>
                  <span className="badge badge-gestor">
                    {c.total_productos} productos
                  </span>
                </div>
                
                <h3 style={{ fontSize: '18px', fontWeight: 700, marginBottom: '10px' }}>{c.nombre}</h3>
                <p style={{ color: 'var(--text-secondary)', fontSize: '13px', lineHeight: 1.5, flex: 1, marginBottom: '20px' }}>
                  {c.descripcion || 'Sin descripción detallada.'}
                </p>

                {isGestorOrAdmin && (
                  <div style={{ display: 'flex', gap: '8px', borderTop: '1px solid var(--glass-border)', paddingTop: '15px', justifyContent: 'flex-end' }}>
                    {isAdmin && (
                      <button 
                        onClick={() => handleDelete(c.id, c.nombre)} 
                        className="btn btn-danger" 
                        style={{ padding: '6px 12px', borderRadius: '6px', fontSize: '12px' }}
                      >
                        <BiTrash /> Eliminar
                      </button>
                    )}
                  </div>
                )}
              </div>
            ))
          )}
        </div>
      )}
    </div>
  )
}

export default CategoriaList
