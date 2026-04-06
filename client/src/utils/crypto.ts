/**
 * End-to-end encryption utilities using Web Crypto API.
 *
 * Encryption flow:
 *   1. Generate random salt (16 bytes) + IV (12 bytes)
 *   2. Derive 256-bit AES key from password via PBKDF2 (100k iterations)
 *   3. Encrypt plaintext with AES-256-GCM → ciphertext + auth tag
 *   4. Store { ciphertext (Base64), salt (Base64), iv (Base64) } on server
 *
 * Decryption flow:
 *   1. Derive key from password + salt (same PBKDF2)
 *   2. Decrypt ciphertext with AES-256-GCM + iv
 *   3. If password is wrong, GCM auth tag check fails → DOMException
 */

const PBKDF2_ITERATIONS = 100_000;
const AES_KEY_LENGTH = 256;
const SALT_LENGTH = 16;
const IV_LENGTH = 12;

// ---------- Helpers ----------

function toArrayBuffer(base64: string): ArrayBuffer {
  const binary = atob(base64);
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i++) {
    bytes[i] = binary.charCodeAt(i);
  }
  return bytes.buffer;
}

function toBase64(buffer: ArrayBuffer): string {
  const bytes = new Uint8Array(buffer);
  let binary = "";
  for (let i = 0; i < bytes.byteLength; i++) {
    binary += String.fromCharCode(bytes[i]);
  }
  return btoa(binary);
}

// ---------- Key Derivation ----------

async function deriveKey(
  password: string,
  salt: Uint8Array
): Promise<CryptoKey> {
  const encoder = new TextEncoder();
  const keyMaterial = await crypto.subtle.importKey(
    "raw",
    encoder.encode(password),
    "PBKDF2",
    false,
    ["deriveKey"]
  );

  return crypto.subtle.deriveKey(
    {
      name: "PBKDF2",
      salt,
      iterations: PBKDF2_ITERATIONS,
      hash: "SHA-256",
    },
    keyMaterial,
    { name: "AES-GCM", length: AES_KEY_LENGTH },
    false,
    ["encrypt", "decrypt"]
  );
}

// ---------- Text Encrypt / Decrypt ----------

export interface EncryptedResult {
  ciphertext: string; // Base64
  salt: string; // Base64
  iv: string; // Base64
}

/**
 * Encrypt a plaintext string using AES-256-GCM.
 * Returns { ciphertext, salt, iv } all as Base64 strings.
 */
export async function encryptText(
  plaintext: string,
  password: string,
  salt?: Uint8Array,
  iv?: Uint8Array,
): Promise<EncryptedResult> {
  const useSalt = salt || crypto.getRandomValues(new Uint8Array(SALT_LENGTH));
  const useIV = iv || crypto.getRandomValues(new Uint8Array(IV_LENGTH));
  const key = await deriveKey(password, useSalt);

  const encoder = new TextEncoder();
  const ciphertext = await crypto.subtle.encrypt(
    { name: "AES-GCM", iv: useIV },
    key,
    encoder.encode(plaintext)
  );

  return {
    ciphertext: toBase64(ciphertext),
    salt: toBase64(useSalt.buffer),
    iv: toBase64(useIV.buffer),
  };
}

/**
 * Decrypt a ciphertext string using AES-256-GCM.
 * Throws DOMException if password is wrong (GCM auth tag mismatch).
 */
export async function decryptText(
  ciphertext: string,
  password: string,
  salt: string,
  iv: string
): Promise<string> {
  const key = await deriveKey(
    password,
    new Uint8Array(toArrayBuffer(salt))
  );
  const decrypted = await crypto.subtle.decrypt(
    { name: "AES-GCM", iv: new Uint8Array(toArrayBuffer(iv)) },
    key,
    toArrayBuffer(ciphertext)
  );
  return new TextDecoder().decode(decrypted);
}

// ---------- File Encrypt / Decrypt ----------

/**
 * Encrypt file data (ArrayBuffer) using AES-256-GCM.
 * Caller must provide pre-generated salt and iv (so they can be stored before encryption).
 */
export async function encryptFileData(
  fileData: ArrayBuffer,
  password: string,
  salt: Uint8Array,
  iv: Uint8Array
): Promise<ArrayBuffer> {
  const key = await deriveKey(password, salt);
  return crypto.subtle.encrypt({ name: "AES-GCM", iv }, key, fileData);
}

/**
 * Decrypt encrypted file data back to original ArrayBuffer.
 */
export async function decryptFileData(
  encryptedData: ArrayBuffer,
  password: string,
  salt: string,
  iv: string
): Promise<ArrayBuffer> {
  const key = await deriveKey(
    password,
    new Uint8Array(toArrayBuffer(salt))
  );
  return crypto.subtle.decrypt(
    { name: "AES-GCM", iv: new Uint8Array(toArrayBuffer(iv)) },
    key,
    encryptedData
  );
}

// ---------- Salt / IV generation ----------

/**
 * Generate a random salt (16 bytes) as Base64.
 */
export function generateSalt(): string {
  const salt = crypto.getRandomValues(new Uint8Array(SALT_LENGTH));
  return toBase64(salt.buffer);
}

/**
 * Generate a random IV (12 bytes) as Base64.
 */
export function generateIV(): string {
  const iv = crypto.getRandomValues(new Uint8Array(IV_LENGTH));
  return toBase64(iv.buffer);
}

/**
 * Decode a Base64 string back to Uint8Array.
 */
export function decodeBase64(base64: string): Uint8Array {
  return new Uint8Array(toArrayBuffer(base64));
}
