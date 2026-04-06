import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 60000,
})

// Token interceptor: auto attach Bearer token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Response interceptor: auto clear token on 401
api.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401) {
      // Only clear if it's an auth endpoint error (not optional auth)
      const url = err.config?.url || ''
      if (url.includes('/auth/')) {
        localStorage.removeItem('token')
        localStorage.removeItem('user')
      }
    }
    return Promise.reject(err)
  }
)

// ---- Transfer API ----

// Reserve a code for E2EE encryption
export async function reserveCode(): Promise<{ code: string }> {
  const res = await api.get('/transfer/reserve-code')
  return res.data
}

// Create transfer (text/files)
export async function createTransfer(
  formData: FormData
): Promise<{ code: string; type: string; expires_at: string }> {
  const res = await api.post('/transfer', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return res.data
}

// Verify code
export async function verifyCode(code: string): Promise<{ valid: boolean; message: string }> {
  const res = await api.post('/transfer/verify', { code })
  return res.data
}

// Retrieve transfer
export async function retrieveTransfer(code: string) {
  const res = await api.get(`/transfer/${code}`)
  return res.data
}

// Get file download URL
export function getDownloadUrl(code: string, filename: string): string {
  return `/api/transfer/${code}/download/${encodeURIComponent(filename)}`
}

// ---- Auth API ----

export interface UserInfo {
  id: number
  username: string
}

export interface AuthResponse {
  id: number
  username: string
  token: string
}

export async function register(username: string, password: string): Promise<AuthResponse> {
  const res = await api.post('/auth/register', { username, password })
  return res.data
}

export async function login(username: string, password: string): Promise<AuthResponse> {
  const res = await api.post('/auth/login', { username, password })
  return res.data
}

export async function getMe(): Promise<{ user: UserInfo | null }> {
  const res = await api.get('/auth/me')
  return res.data
}

// ---- Records API ----

export interface RecordItem {
  id: number
  action: 'send' | 'retrieve'
  transfer_code: string
  transfer_type: string | null
  text_preview: string | null
  file_count: number
  permanent: boolean
  created_at: string
}

export interface RecordsResponse {
  items: RecordItem[]
  total: number
  page: number
  page_size: number
}

export async function getRecords(
  action?: string,
  page: number = 1,
  pageSize: number = 20
): Promise<RecordsResponse> {
  const params: Record<string, string | number> = { page, page_size: pageSize }
  if (action) params.action = action
  const res = await api.get('/records', { params })
  return res.data
}

// ---- Setup API ----

export async function getSetupStatus(): Promise<{ initialized: boolean }> {
  const res = await api.get('/setup/status')
  return res.data
}

export async function testDbConnection(data: {
  db_type: string
  db_host?: string
  db_port?: number
  db_user?: string
  db_password?: string
  db_name?: string
}): Promise<{ success: boolean; message: string }> {
  const res = await api.post('/setup/test-db', data)
  return res.data
}

export async function testStorageConnection(data: Record<string, string>): Promise<{ success: boolean; message: string }> {
  const res = await api.post('/setup/test-storage', data)
  return res.data
}

export async function finishSetup(data: Record<string, unknown>): Promise<{ success: boolean; message: string }> {
  const res = await api.post('/setup/finish', data)
  return res.data
}

export default api
