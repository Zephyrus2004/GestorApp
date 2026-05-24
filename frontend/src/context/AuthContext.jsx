import React, { createContext, useState, useEffect, useContext } from 'react'
import client from '../api/client'
import toast from 'react-hot-toast'

const AuthContext = createContext(null)

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [token, setToken] = useState(localStorage.getItem('token') || null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const initAuth = async () => {
      if (token) {
        try {
          const res = await client.get('/api/auth/profile/')
          setUser(res.data)
        } catch (err) {
          console.error('Sesión expirada o token inválido', err)
          logoutUser()
        }
      }
      setLoading(false)
    }
    initAuth()
  }, [token])

  const loginUser = async (username, password) => {
    try {
      const res = await client.post('/api/auth/login/', { username, password })
      const { token: userToken, user: userData } = res.data
      localStorage.setItem('token', userToken)
      setToken(userToken)
      setUser(userData)
      toast.success(`¡Bienvenido, ${userData.full_name}!`)
      return true
    } catch (err) {
      const errors = err.response?.data?.non_field_errors || ['Credenciales incorrectas o error de conexión.']
      toast.error(errors[0])
      return false
    }
  }

  const logoutUser = async () => {
    if (token) {
      try {
        await client.post('/api/auth/logout/')
      } catch (err) {
        console.error('Error al cerrar sesión en el servidor', err)
      }
    }
    localStorage.removeItem('token')
    setToken(null)
    setUser(null)
    toast.success('Sesión cerrada.')
  }

  const updateProfile = (updatedUser) => {
    setUser(updatedUser)
  }

  return (
    <AuthContext.Provider value={{ user, token, loading, login: loginUser, logout: logoutUser, updateProfile }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => useContext(AuthContext)
