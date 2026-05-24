import React, { useEffect, useState } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import client from '../../api/client'
import { BiArrowBack } from 'react-icons/bi'
import toast from 'react-hot-toast'

const ProductoForm = () => {
  const { id } = useParams()
  const isEdit = !!id
  const navigate = useNavigate()

  const [categorias, setCategorias] = useState([])
  const [loading, setLoading] = useState(isEdit)
  const [submitting, setSubmitting] = useState(false)

  // Campos del formulario
  const [nombre, setNombre] = useState('')
  const [descripcion, setDescripcion] = useState('')
  const [categoria, setCategoria] = useState('')
  const [marca, setMarca] = useState('')
  const [modelo, setModelo] = useState('')
  const [numeroSerie, setNumeroSerie] = useState('')
  const [precio, setPrecio] = useState('0')
  const [stock, setStock] = useState('0')
  const [estado, setEstado] = useState('nuevo')
  const [disponible, setDisponible] = useState(true)
  const [ubicacion, setUbicacion] = useState('')
  const [imagenFile, setImagenFile] = useState(null)

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

    if (isEdit) {
      const fetchProductData = async () => {
        try {
          const res = await client.get(`/api/productos/${id}/`)
          const p = res.data
          setNombre(p.nombre)
          setDescripcion(p.descripcion || '')
          setCategoria(p.categoria || '')
          setMarca(p.marca || '')
          setModelo(p.modelo || '')
          setNumeroSerie(p.numero_serie || '')
          setPrecio(p.precio.toString())
          setStock(p.stock.toString())
          setEstado(p.estado)
          setDisponible(p.disponible)
          setUbicacion(p.ubicacion || '')
        } catch (err) {
          toast.error('Error al cargar datos del producto.')
          navigate('/productos')
        } finally {
          setLoading(false)
        }
      }
      fetchProductData()
    }
  }, [id, isEdit])

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!nombre || !categoria) {
      toast.error('Nombre y Categoría son campos obligatorios.')
      return
    }

    setSubmitting(true)
    const formData = new FormData()
    formData.append('nombre', nombre)
    formData.append('descripcion', descripcion)
    formData.append('categoria', categoria)
    formData.append('marca', marca)
    formData.append('modelo', modelo)
    formData.append('numero_serie', numeroSerie)
    formData.append('precio', parseFloat(precio))
    formData.append('stock', parseInt(stock))
    formData.append('estado', estado)
    formData.append('disponible', disponible)
    formData.append('ubicacion', ubicacion)
    
    if (imagenFile) {
      formData.append('imagen', imagenFile)
    }

    try {
      if (isEdit) {
        await client.put(`/api/productos/${id}/`, formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        })
        toast.success('Producto actualizado exitosamente.')
      } else {
        await client.post('/api/productos/', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        })
        toast.success('Producto creado exitosamente.')
      }
      navigate('/productos')
    } catch (err) {
      console.error(err)
      const data = err.response?.data
      if (data && data.numero_serie) {
        toast.error(`Número de serie: ${data.numero_serie[0]}`)
      } else {
        toast.error('Ocurrió un error al guardar el producto.')
      }
    } finally {
      setSubmitting(false)
    }
  }

  if (loading) {
    return (
      <div style={{ display: 'flex', flex: 1, alignItems: 'center', justifyContent: 'center', height: '50vh' }}>
        <div className="spinner"></div>
      </div>
    )
  }

  return (
    <div>
      <div className="page-header">
        <Link to="/productos" className="btn btn-secondary">
          <BiArrowBack /> Volver
        </Link>
        <div className="page-title" style={{ flex: 1, marginLeft: '20px' }}>
          <h2>{isEdit ? 'Editar Producto' : 'Nuevo Producto'}</h2>
          <p>{isEdit ? 'Modifica los campos del equipo en la tienda' : 'Ingresa un nuevo equipo al inventario'}</p>
        </div>
      </div>

      <div className="glass-card">
        <form onSubmit={handleSubmit}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
            <div className="form-group">
              <label className="form-label">Nombre del Producto *</label>
              <input 
                type="text" 
                className="form-input" 
                placeholder="Ej: ThinkPad L14 Gen 4"
                value={nombre}
                onChange={(e) => setNombre(e.target.value)}
                required
              />
            </div>

            <div className="form-group">
              <label className="form-label">Categoría *</label>
              <select 
                className="form-input"
                value={categoria}
                onChange={(e) => setCategoria(e.target.value)}
                required
              >
                <option value="">Selecciona una categoría</option>
                {categorias.map(c => (
                  <option key={c.id} value={c.id}>{c.nombre}</option>
                ))}
              </select>
            </div>
          </div>

          <div className="form-group">
            <label className="form-label">Descripción</label>
            <textarea 
              className="form-input" 
              placeholder="Detalla las especificaciones del equipo..."
              value={descripcion}
              onChange={(e) => setDescripcion(e.target.value)}
              rows="3"
              style={{ fontFamily: 'inherit', resize: 'vertical' }}
            />
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '20px' }}>
            <div className="form-group">
              <label className="form-label">Marca</label>
              <input 
                type="text" 
                className="form-input" 
                placeholder="Ej: Lenovo"
                value={marca}
                onChange={(e) => setMarca(e.target.value)}
              />
            </div>

            <div className="form-group">
              <label className="form-label">Modelo</label>
              <input 
                type="text" 
                className="form-input" 
                placeholder="Ej: L14"
                value={modelo}
                onChange={(e) => setModelo(e.target.value)}
              />
            </div>

            <div className="form-group">
              <label className="form-label">Número de Serie</label>
              <input 
                type="text" 
                className="form-input" 
                placeholder="Ej: LNV-SER-99218"
                value={numeroSerie}
                onChange={(e) => setNumeroSerie(e.target.value)}
              />
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '20px' }}>
            <div className="form-group">
              <label className="form-label">Precio (USD) *</label>
              <input 
                type="number" 
                step="0.01"
                className="form-input" 
                value={precio}
                onChange={(e) => setPrecio(e.target.value)}
                required
              />
            </div>

            <div className="form-group">
              <label className="form-label">Stock inicial *</label>
              <input 
                type="number" 
                className="form-input" 
                value={stock}
                onChange={(e) => setStock(e.target.value)}
                required
              />
            </div>

            <div className="form-group">
              <label className="form-label">Estado Físico *</label>
              <select 
                className="form-input"
                value={estado}
                onChange={(e) => setEstado(e.target.value)}
                required
              >
                <option value="nuevo">Nuevo</option>
                <option value="bueno">Buen Estado</option>
                <option value="regular">Regular</option>
                <option value="malo">Mal Estado</option>
                <option value="baja">Dado de Baja</option>
              </select>
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
            <div className="form-group">
              <label className="form-label">Ubicación</label>
              <input 
                type="text" 
                className="form-input" 
                placeholder="Ej: Vitrina Principal"
                value={ubicacion}
                onChange={(e) => setUbicacion(e.target.value)}
              />
            </div>

            <div className="form-group">
              <label className="form-label">Imagen</label>
              <input 
                type="file" 
                className="form-input" 
                onChange={(e) => setImagenFile(e.target.files[0])}
                accept="image/*"
              />
            </div>
          </div>

          <div className="form-group" style={{ display: 'flex', alignItems: 'center', gap: '10px', marginTop: '10px', marginBottom: '30px' }}>
            <input 
              type="checkbox" 
              id="disponible"
              checked={disponible}
              onChange={(e) => setDisponible(e.target.checked)}
              style={{ width: '20px', height: '20px', cursor: 'pointer' }}
            />
            <label htmlFor="disponible" style={{ fontSize: '15px', fontWeight: 500, cursor: 'pointer' }}>
              Producto disponible para alquiler / entrega inmediata
            </label>
          </div>

          <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '12px' }}>
            <Link to="/productos" className="btn btn-secondary">
              Cancelar
            </Link>
            <button type="submit" className="btn btn-primary" disabled={submitting}>
              {submitting ? 'Guardando...' : (isEdit ? 'Guardar Cambios' : 'Crear Producto')}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default ProductoForm
