import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 60000,
})

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
