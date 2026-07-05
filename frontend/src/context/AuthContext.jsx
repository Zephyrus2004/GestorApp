// ==============================================================================
// SECCIÓN: CONTEXTO GLOBAL DE AUTENTICACIÓN (REACT CONTEXT)
// ==============================================================================
// Este módulo crea y provee un contexto global de React para la autenticación.
# Guarda el estado de la sesión activa, el token de acceso, controla el proceso
# de inicio/cierre de sesión y gestiona las solicitudes persistidas en LocalStorage.

import React, { createContext, useState, useEffect, useContext } from 'react'
import client from '../api/client'
import toast from 'react-hot-toast'

// Crear el contexto de autenticación vacío
const AuthContext = createContext(null)

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null) // Contiene los datos del usuario logueado
  const [token, setToken] = useState(localStorage.getItem('token') || null) // Token de DRF persistido
  const [loading, setLoading] = useState(true) // Indicador de carga inicial mientras valida sesión

  // Efecto que inicializa la sesión. Si hay un token en LocalStorage,
  // intenta descargar los datos frescos del perfil del usuario para validar el token.
  useEffect(() => {
    const initAuth = async () => {
      if (token) {
        try {
          // Solicitar perfil del usuario usando el token almacenado
          const res = await client.get('/api/auth/profile/')
          setUser(res.data)
        } catch (err) {
          console.error('Sesión expirada o token inválido', err)
          logoutUser() // Limpia sesión local si el backend rechaza el token
        }
      }
      setLoading(false)
    }
    initAuth()
  }, [token])

  /**
   * Envía las credenciales al backend para iniciar sesión.
   * Si es exitoso, almacena el token en LocalStorage y actualiza el estado.
   */
  const loginUser = async (username, password) => {
    try {
      const res = await client.post('/api/auth/login/', { username, password })
      const { token: userToken, user: userData } = res.data
      
      // Guardar sesión en LocalStorage para persistencia
      localStorage.setItem('token', userToken)
      setToken(userToken)
      setUser(userData)
      
      toast.success(`¡Bienvenido, ${userData.full_name}!`)
      return true
    } catch (err) {
      // Captura y muestra el primer mensaje de error que retorne la API
      const errors = err.response?.data?.non_field_errors || ['Credenciales incorrectas o error de conexión.']
      toast.error(errors[0])
      return false
    }
  }

  /**
   * Cierra la sesión activa.
   * Envía petición de logout al backend para destruir el token e invalida el estado local.
   */
  const logoutUser = async () => {
    if (token) {
      try {
        await client.post('/api/auth/logout/')
      } catch (err) {
        console.error('Error al cerrar sesión en el servidor', err)
      }
    }
    // Limpieza de estados y LocalStorage
    localStorage.removeItem('token')
    setToken(null)
    setUser(null)
    toast.success('Sesión cerrada.')
  }

  // Permite actualizar el estado de usuario desde otros componentes (ej: editar perfil)
  const updateProfile = (updatedUser) => {
    setUser(updatedUser)
  }

  return (
    <AuthContext.Provider value={{ user, token, loading, login: loginUser, logout: logoutUser, updateProfile }}>
      {children}
    </AuthContext.Provider>
  )
}

// Hook personalizado (Custom Hook) para consumir fácilmente el contexto desde cualquier componente
export const useAuth = () => useContext(AuthContext)

