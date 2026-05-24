import React, { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import client from '../../api/client'
import { useAuth } from '../../context/AuthContext'
import { BiArrowBack as BackIcon, BiLaptop as LaptopIcon, BiEdit as EditIcon } from 'react-icons/bi'
import toast from 'react-hot-toast'

const ProductoDetail = () => {
  const { id } = useParams()
  const { user } = useAuth()
  const [producto, setProducto] = useState(null)
  const [asignaciones, setAsignaciones] = useState([])
  const [loading, setLoading] = useState(true)

  const userRole = user.profile?.rol || 'usuario'
  const isGestorOrAdmin = user.is_staff || ['admin', 'gestor'].includes(userRole)

  useEffect(() => {
    const fetchDetail = async () => {
      try {
        const [prodRes, asigRes] = await Promise.all([
          client.get(`/api/productos/${id}/`),
          client.get(`/api/asignaciones/?producto=${id}`)
        ])
        setProducto(prodRes.data)
        const filteredAsig = (asigRes.data.results || asigRes.data).filter(a => a.producto === parseInt(id))
        setAsignaciones(filteredAsig)
      } catch (err) {
        toast.error('Error al cargar detalles del producto.')
      } finally {
        setLoading(false)
      }
    }
    fetchDetail()
  }, [id])

  if (loading) {
    return (
      <div style={{ display: 'flex', flex: 1, alignItems: 'center', justifyContent: 'center', height: '50vh' }}>
        <div className="spinner"></div>
      </div>
    )
  }

  if (!producto) {
    return (
      <div className="glass-card" style={{ textAlign: 'center', padding: '40px' }}>
        <h3>Producto no encontrado</h3>
        <Link to="/productos" className="btn btn-secondary" style={{ marginTop: '20px' }}>
          Volver al catálogo
        </Link>
      </div>
    )
  }

  return (
    <div>
      <div className="page-header">
        <Link to="/productos" className="btn btn-secondary">
          <BackIcon /> Volver
        </Link>
        {isGestorOrAdmin && (
          <Link to={`/productos/${producto.id}/editar`} className="btn btn-primary">
            <EditIcon /> Editar Producto
          </Link>
        )}
      </div>

      <div className="glass-card" style={{ marginBottom: '30px' }}>
        <div className="detail-grid">
          <div className="product-image-large">
            {producto.imagen ? (
              <img src={producto.imagen.startsWith('http') ? producto.imagen : `http://localhost:8000${producto.imagen}`} alt={producto.nombre} />
            ) : (
              <LaptopIcon />
            )}
          </div>

          <div className="product-details">
            <div>
              <span className="badge badge-gestor" style={{ marginBottom: '10px' }}>
                {producto.categoria_detalle?.nombre || 'General'}
              </span>
              <h2 style={{ fontSize: '24px', fontWeight: 800 }}>{producto.nombre}</h2>
              <p style={{ color: 'var(--text-secondary)', marginTop: '10px', fontSize: '15px', lineHeight: 1.6 }}>
                {producto.descripcion || 'Sin descripción disponible.'}
              </p>
            </div>

            <div style={{ marginTop: '20px' }}>
              <div className="product-meta-row">
                <span className="meta-label">Marca / Modelo:</span>
                <span className="meta-value">{producto.marca || '-'} / {producto.modelo || '-'}</span>
              </div>
              <div className="product-meta-row">
                <span className="meta-label">Número de Serie:</span>
                <span className="meta-value" style={{ fontFamily: 'monospace' }}>{producto.numero_serie || 'N/A'}</span>
              </div>
              <div className="product-meta-row">
                <span className="meta-label">Precio (USD):</span>
                <span className="meta-value">${producto.precio}</span>
              </div>
              <div className="product-meta-row">
                <span className="meta-label">Stock en Tienda:</span>
                <span className="meta-value">{producto.stock} unidades</span>
              </div>
              <div className="product-meta-row">
                <span className="meta-label">Estado Físico:</span>
                <span className="meta-value" style={{ textTransform: 'capitalize' }}>{producto.estado}</span>
              </div>
              <div className="product-meta-row">
                <span className="meta-label">Ubicación física:</span>
                <span className="meta-value">{producto.ubicacion || 'Depósito central'}</span>
              </div>
              <div className="product-meta-row">
                <span className="meta-label">Registrado Por:</span>
                <span className="meta-value">{producto.registrado_por_name || 'Sistema'}</span>
              </div>
              <div className="product-meta-row">
                <span className="meta-label">Disponibilidad:</span>
                <span className={`badge ${producto.disponible ? 'badge-gestor' : 'badge-visitante'}`}>
                  {producto.disponible ? 'Disponible' : 'Alquilado / Ocupado'}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="glass-card">
        <h3 style={{ fontSize: '18px', fontWeight: 700, marginBottom: '20px' }}>Historial de Asignaciones</h3>
        <div className="table-container">
          <table className="custom-table">
            <thead>
              <tr>
                <th>Asignado A</th>
                <th>Departamento</th>
                <th>Fecha Asignación</th>
                <th>Fecha Devolución</th>
                <th>Estado</th>
                <th>Observaciones</th>
                <th>Asignado Por</th>
              </tr>
            </thead>
            <tbody>
              {asignaciones.length === 0 ? (
                <tr>
                  <td colSpan="7" style={{ textAlign: 'center', color: 'var(--text-secondary)', padding: '24px' }}>
                    Este producto no registra asignaciones o alquileres activos.
                  </td>
                </tr>
              ) : (
                asignaciones.map((a) => (
                  <tr key={a.id}>
                    <td style={{ fontWeight: 600 }}>{a.asignado_a_name}</td>
                    <td>{a.departamento || '-'}</td>
                    <td>{new Date(a.fecha_asignacion).toLocaleDateString()}</td>
                    <td>{a.fecha_devolucion ? new Date(a.fecha_devolucion).toLocaleDateString() : '-'}</td>
                    <td>
                      <span className={`badge ${a.estado === 'activa' ? 'badge-gestor' : 'badge-visitante'}`}>
                        {a.estado}
                      </span>
                    </td>
                    <td style={{ maxWidth: '250px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{a.observaciones || '-'}</td>
                    <td>{a.asignado_por_name || '-'}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}

export default ProductoDetail
