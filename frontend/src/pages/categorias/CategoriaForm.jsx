import React, { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import client from '../../api/client'
import { BiArrowBack } from 'react-icons/bi'
import toast from 'react-hot-toast'

const CategoriaForm = () => {
  const navigate = useNavigate()
  const [nombre, setNombre] = useState('')
  const [descripcion, setDescripcion] = useState('')
  const [icono, setIcono] = useState('bi-box')
  const [submitting, setSubmitting] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!nombre) {
      toast.error('El nombre es obligatorio.')
      return
    }

    setSubmitting(true)
    try {
      await client.post('/api/categorias/', { nombre, descripcion, icono })
      toast.success('Categoría creada exitosamente.')
      navigate('/categorias')
    } catch (err) {
      toast.error('Error al crear la categoría. Asegúrese de que el nombre sea único.')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div>
      <div className="page-header">
        <Link to="/categorias" className="btn btn-secondary">
          <BiArrowBack /> Volver
        </Link>
        <div className="page-title" style={{ flex: 1, marginLeft: '20px' }}>
          <h2>Nueva Categoría</h2>
          <p>Ingresa una nueva categoría para organizar los productos</p>
        </div>
      </div>

      <div className="glass-card" style={{ maxWidth: '600px', margin: '0 auto' }}>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label">Nombre de la Categoría *</label>
            <input 
              type="text" 
              className="form-input" 
              placeholder="Ej: Servidores y Redes"
              value={nombre}
              onChange={(e) => setNombre(e.target.value)}
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label">Descripción</label>
            <textarea 
              className="form-input" 
              placeholder="Describa qué tipo de productos agrupa esta categoría..."
              value={descripcion}
              onChange={(e) => setDescripcion(e.target.value)}
              rows="3"
              style={{ fontFamily: 'inherit', resize: 'vertical' }}
            />
          </div>

          <div className="form-group">
            <label className="form-label">Ícono de Bootstrap Icons *</label>
            <select 
              className="form-input"
              value={icono}
              onChange={(e) => setIcono(e.target.value)}
              required
            >
              <option value="bi-laptop">bi-laptop (Laptops/Computadoras)</option>
              <option value="bi-printer">bi-printer (Impresoras/Escáneres)</option>
              <option value="bi-router">bi-router (Servidores/Redes)</option>
              <option value="bi-cpu">bi-cpu (Componentes/Accesorios)</option>
              <option value="bi-file-earmark-code">bi-file-earmark-code (Software/Licencias)</option>
              <option value="bi-box">bi-box (General)</option>
            </select>
          </div>

          <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '12px', marginTop: '30px' }}>
            <Link to="/categorias" className="btn btn-secondary">
              Cancelar
            </Link>
            <button type="submit" className="btn btn-primary" disabled={submitting}>
              {submitting ? 'Guardando...' : 'Crear Categoría'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default CategoriaForm
