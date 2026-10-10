/**
 * Database connection & query helper for Vercel Serverless Functions.
 * Supports Vercel Postgres, Supabase, Neon, or any PostgreSQL via DATABASE_URL.
 */

const { Pool } = require('pg');

let pool = null;
let initialized = false;

function getPool() {
  const connectionString = process.env.DATABASE_URL || process.env.POSTGRES_URL;
  if (!connectionString) {
    return null;
  }

  if (!pool) {
    const isLocalhost = connectionString.includes('localhost') || connectionString.includes('127.0.0.1');
    pool = new Pool({
      connectionString,
      ssl: isLocalhost ? false : { rejectUnauthorized: false },
      max: 10,
      idleTimeoutMillis: 30000,
      connectionTimeoutMillis: 5000,
    });
  }
  return pool;
}

/**
 * Auto-creates necessary tables if they don't already exist.
 */
async function ensureTables() {
  if (initialized) return true;
  const p = getPool();
  if (!p) return false;

  const schemaSql = `
    CREATE TABLE IF NOT EXISTS users (
      id VARCHAR(255) PRIMARY KEY,
      google_id VARCHAR(255) UNIQUE,
      email VARCHAR(255) UNIQUE NOT NULL,
      name VARCHAR(255),
      avatar VARCHAR(1024),
      created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
      last_login TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS user_progress (
      user_id VARCHAR(255) NOT NULL,
      problem_id VARCHAR(64) NOT NULL,
      is_solved BOOLEAN DEFAULT FALSE,
      is_bookmarked BOOLEAN DEFAULT FALSE,
      updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
      PRIMARY KEY (user_id, problem_id)
    );

    CREATE TABLE IF NOT EXISTS user_notes (
      user_id VARCHAR(255) NOT NULL,
      problem_id VARCHAR(64) NOT NULL,
      notes TEXT,
      updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
      PRIMARY KEY (user_id, problem_id)
    );

    CREATE INDEX IF NOT EXISTS idx_user_progress_user ON user_progress(user_id);
    CREATE INDEX IF NOT EXISTS idx_user_notes_user ON user_notes(user_id);
  `;

  try {
    const client = await p.connect();
    try {
      await client.query(schemaSql);
      initialized = true;
    } finally {
      client.release();
    }
    return true;
  } catch (err) {
    console.error('[DB] Schema init error:', err.message);
    return false;
  }
}

/**
 * Execute a query against the PostgreSQL database.
 */
async function query(text, params = []) {
  const p = getPool();
  if (!p) {
    return { isConfigured: false, rows: [] };
  }

  await ensureTables();
  const start = Date.now();
  const res = await p.query(text, params);
  const duration = Date.now() - start;
  return { isConfigured: true, rows: res.rows, rowCount: res.rowCount, duration };
}

module.exports = {
  getPool,
  ensureTables,
  query,
  isConfigured: () => Boolean(process.env.DATABASE_URL || process.env.POSTGRES_URL)
};
