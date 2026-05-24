import React, { useEffect, useState } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import client from '../../api/client'
import { BiArrowBack } from 'react-icons/bi'
import toast from 'react-hot-toast'

const UsuarioForm = () => {
  const { id } = useParams()
  const isEdit = !!id
  const navigate = useNavigate()

  const [loading, setLoading] = useState(isEdit)
  const [submitting, setSubmitting] = useState(false)

  // Campos
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [firstName, setFirstName] = useState('')
  const [lastName, setLastName] = useState('')
  const [rol, setRol] = useState('usuario')
  const [telefono, setTelefono] = useState('')
  const [departamento, setDepartamento] = useState('')
  const [isActive, setIsActive] = useState(true)

  useEffect(() => {
    if (isEdit) {
      const fetchUserData = async () => {
        try {
          const res = await client.get(`/api/users/${id}/`)
          const u = res.data
          setUsername(u.username)
          setEmail(u.email)
          setFirstName(u.first_name)
          setLastName(u.last_name)
          setIsActive(u.is_active)
          if (u.profile) {
            setRol(u.profile.rol)
            setTelefono(u.profile.telefono || '')
            setDepartamento(u.profile.departamento || '')
          }
        } catch (err) {
          toast.error('Error al cargar datos del usuario.')
          navigate('/usuarios')
        } finally {
          setLoading(false)
        }
      }
      fetchUserData()
    }
  }, [id, isEdit])

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!username || !email || (!isEdit && !password)) {
      toast.error('Nombre de usuario, Email y Contraseña (en creación) son obligatorios.')
      return
    }

    setSubmitting(true)
    
    const payload = {
      username,
      email,
      first_name: firstName,
      last_name: lastName,
      is_active: isActive,
      profile: {
        rol,
        telefono,
        departamento
      }
    }

    if (!isEdit) {
      payload.password = password
      payload.rol = rol
      payload.telefono = telefono
      payload.departamento = departamento
    }

    try {
      if (isEdit) {
        await client.put(`/api/users/${id}/`, payload)
        toast.success('Usuario actualizado exitosamente.')
      } else {
        await client.post('/api/users/', payload)
        toast.success('Usuario creado exitosamente.')
      }
      navigate('/usuarios')
    } catch (err) {
      console.error(err)
      const data = err.response?.data
      if (data && data.username) {
        toast.error(`Nombre de usuario: ${data.username[0]}`)
      } else if (data && data.email) {
        toast.error(`Correo electrónico: ${data.email[0]}`)
      } else {
        toast.error('Ocurrió un error al guardar el usuario.')
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
        <Link to="/usuarios" className="btn btn-secondary">
          <BiArrowBack /> Volver
        </Link>
        <div className="page-title" style={{ flex: 1, marginLeft: '20px' }}>
          <h2>{isEdit ? 'Editar Usuario' : 'Nuevo Usuario'}</h2>
          <p>{isEdit ? 'Modifica los privilegios y perfiles de acceso' : 'Registra un nuevo usuario con credenciales específicas'}</p>
        </div>
      </div>

      <div className="glass-card" style={{ maxWidth: '800px', margin: '0 auto' }}>
        <form onSubmit={handleSubmit}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
            <div className="form-group">
              <label className="form-label">Nombre de Usuario *</label>
              <input 
                type="text" 
                className="form-input" 
                placeholder="Ej: cesar_ceferino"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                disabled={isEdit}
              />
            </div>

            <div className="form-group">
              <label className="form-label">Correo Electrónico *</label>
              <input 
                type="email" 
                className="form-input" 
                placeholder="correo@infotech.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
          </div>

          {!isEdit && (
            <div className="form-group">
              <label className="form-label">Contraseña *</label>
              <input 
                type="password" 
                className="form-input" 
                placeholder="Contraseña inicial..."
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
          )}

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
            <div className="form-group">
              <label className="form-label">Nombre</label>
              <input 
                type="text" 
                className="form-input" 
                placeholder="Ej: Cesar"
                value={firstName}
                onChange={(e) => setFirstName(e.target.value)}
              />
            </div>

            <div className="form-group">
              <label className="form-label">Apellido</label>
              <input 
                type="text" 
                className="form-input" 
                placeholder="Ej: Ceferino"
                value={lastName}
                onChange={(e) => setLastName(e.target.value)}
              />
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '20px' }}>
            <div className="form-group">
              <label className="form-label">Rol en el Sistema *</label>
              <select 
                className="form-input"
                value={rol}
                onChange={(e) => setRol(e.target.value)}
                required
              >
                <option value="admin">Administrador</option>
                <option value="gestor">Gestor</option>
                <option value="usuario">Usuario</option>

              </select>
            </div>

            <div className="form-group">
              <label className="form-label">Teléfono</label>
              <input 
                type="text" 
                className="form-input" 
                placeholder="+58 412 1234567"
                value={telefono}
                onChange={(e) => setTelefono(e.target.value)}
              />
            </div>

            <div className="form-group">
              <label className="form-label">Departamento</label>
              <input 
                type="text" 
                className="form-input" 
                placeholder="Ej: Gerencia y Control"
                value={departamento}
                onChange={(e) => setDepartamento(e.target.value)}
              />
            </div>
          </div>

          <div className="form-group" style={{ display: 'flex', alignItems: 'center', gap: '10px', marginTop: '10px', marginBottom: '30px' }}>
            <input 
              type="checkbox" 
              id="isActive"
              checked={isActive}
              onChange={(e) => setIsActive(e.target.checked)}
              style={{ width: '20px', height: '20px', cursor: 'pointer' }}
            />
            <label htmlFor="isActive" style={{ fontSize: '15px', fontWeight: 500, cursor: 'pointer' }}>
              Usuario activo (permite iniciar sesión)
            </label>
          </div>

          <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '12px' }}>
            <Link to="/usuarios" className="btn btn-secondary">
              Cancelar
            </Link>
            <button type="submit" className="btn btn-primary" disabled={submitting}>
              {submitting ? 'Guardando...' : (isEdit ? 'Guardar Cambios' : 'Crear Usuario')}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default UsuarioForm
