import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import client from '../../api/client'
import { useAuth } from '../../context/AuthContext'
import { BiSearch, BiPlus, BiShow, BiEdit, BiTrash } from 'react-icons/bi'
import toast from 'react-hot-toast'

const ProductoList = () => {
  const { user } = useAuth()
  const [productos, setProductos] = useState([])
  const [categorias, setCategorias] = useState([])
  const [loading, setLoading] = useState(true)
  
  // Filtros
  const [search, setSearch] = useState('')
  const [selectedCat, setSelectedCat] = useState('')
  const [selectedEstado, setSelectedEstado] = useState('')
  const [selectedDispo, setSelectedDispo] = useState('')

  const userRole = user.profile?.rol || 'usuario'
  const isGestorOrAdmin = user.is_staff || ['admin', 'gestor'].includes(userRole)
  const isAdmin = user.is_staff || userRole === 'admin'

  const fetchProductos = async () => {
    try {
      setLoading(true)
      let url = '/api/productos/?'
      if (search) url += `&q=${search}`
      if (selectedCat) url += `&categoria=${selectedCat}`
      if (selectedEstado) url += `&estado=${selectedEstado}`
      if (selectedDispo) url += `&disponible=${selectedDispo}`

      const res = await client.get(url)
      setProductos(res.data.results || res.data)
    } catch (err) {
      toast.error('Error al cargar productos.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    const fetchCategorias = async () => {
      try {
        const res = await client.get('/api/categorias/')
        setCategorias(res.data.results || res.data)
      } catch (err) {
        console.error('Error al cargar categorías', err)
      }
    }
    fetchCategorias()
  }, [])

  useEffect(() => {
    const delayDebounce = setTimeout(() => {
      fetchProductos()
    }, 300)

    return () => clearTimeout(delayDebounce)
  }, [search, selectedCat, selectedEstado, selectedDispo])

  const handleDelete = async (id, nombre) => {
    if (!window.confirm(`¿Estás seguro de que deseas eliminar el producto "${nombre}"?`)) return
    try {
      await client.delete(`/api/productos/${id}/`)
      toast.success('Producto eliminado.')
      fetchProductos()
    } catch (err) {
      toast.error('No se pudo eliminar el producto.')
    }
  }

  return (
    <div>
      <div className="page-header">
        <div className="page-title">
          <h2>Catálogo de Productos</h2>
          <p>Consulta, busca y filtra el stock de informática.</p>
        </div>
        {isGestorOrAdmin && (
          <Link to="/productos/nuevo" className="btn btn-primary">
            <BiPlus size={18} /> Nuevo Producto
          </Link>
        )}
      </div>

      <div className="glass-card" style={{ marginBottom: '24px', padding: '20px' }}>
        <div className="filters-bar">
          <div className="form-group" style={{ flex: 2, marginBottom: 0 }}>
            <input 
              type="text" 
              className="form-input" 
              placeholder="Buscar por nombre, marca, modelo o serie..." 
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>
          
          <div className="form-group" style={{ marginBottom: 0 }}>
            <select 
              className="form-input"
              value={selectedCat}
              onChange={(e) => setSelectedCat(e.target.value)}
            >
              <option value="">Todas las Categorías</option>
              {categorias.map(c => (
                <option key={c.id} value={c.id}>{c.nombre}</option>
              ))}
            </select>
          </div>

          <div className="form-group" style={{ marginBottom: 0 }}>
            <select 
              className="form-input"
              value={selectedEstado}
              onChange={(e) => setSelectedEstado(e.target.value)}
            >
              <option value="">Cualquier Estado</option>
              <option value="nuevo">Nuevo</option>
              <option value="bueno">Buen Estado</option>
              <option value="regular">Regular</option>
              <option value="malo">Mal Estado</option>
              <option value="baja">Baja</option>
            </select>
          </div>

          <div className="form-group" style={{ marginBottom: 0 }}>
            <select 
              className="form-input"
              value={selectedDispo}
              onChange={(e) => setSelectedDispo(e.target.value)}
            >
              <option value="">Disponibilidad</option>
              <option value="true">Disponible</option>
              <option value="false">Alquilado/No Disponible</option>
            </select>
          </div>
        </div>
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
                  <th>Nombre</th>
                  <th>Categoría</th>
                  <th>Marca / Modelo</th>
                  <th>Precio (USD)</th>
                  <th>Stock</th>
                  <th>Estado</th>
                  <th>Disponibilidad</th>
                  <th style={{ textAlign: 'right' }}>Acciones</th>
                </tr>
              </thead>
              <tbody>
                {productos.length === 0 ? (
                  <tr>
                    <td colSpan="8" style={{ textAlign: 'center', color: 'var(--text-secondary)', padding: '40px' }}>
                      No se encontraron productos con los criterios ingresados.
                    </td>
                  </tr>
                ) : (
                  productos.map((p) => (
                    <tr key={p.id}>
                      <td style={{ fontWeight: 600 }}>{p.nombre}</td>
                      <td>{p.categoria_detalle?.nombre}</td>
                      <td>{p.marca} {p.modelo}</td>
                      <td>${p.precio}</td>
                      <td>
                        <span className={`badge ${p.stock <= 5 ? 'badge-visitante' : 'badge-gestor'}`}>
                          {p.stock} unid.
                        </span>
                      </td>
                      <td>
                        <span className="badge badge-admin" style={{ textTransform: 'capitalize' }}>{p.estado}</span>
                      </td>
                      <td>
                        <span className={`badge ${p.disponible ? 'badge-gestor' : 'badge-visitante'}`}>
                          {p.disponible ? 'Disponible' : 'Alquilado'}
                        </span>
                      </td>
                      <td className="actions-cell">
                        <Link to={`/productos/${p.id}`} className="action-btn" title="Ver Detalle">
                          <BiShow size={18} />
                        </Link>
                        {isGestorOrAdmin && (
                          <Link to={`/productos/${p.id}/editar`} className="action-btn" title="Editar">
                            <BiEdit size={18} />
                          </Link>
                        )}
                        {isAdmin && (
                          <button 
                            onClick={() => handleDelete(p.id, p.nombre)} 
                            className="action-btn danger-hover" 
                            title="Eliminar"
                          >
                            <BiTrash size={18} />
                          </button>
                        )}
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  )
}

export default ProductoList
