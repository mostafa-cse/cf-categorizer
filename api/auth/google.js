/**
 * Vercel Serverless Function: Google Authentication & User Sync
 * POST /api/auth/google
 */

const db = require('../db');

module.exports = async (req, res) => {
  // CORS Headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(200).json({
      status: 'ok',
      endpoint: '/api/auth/google',
      dbConfigured: db.isConfigured()
    });
  }

  try {
    const { google_id, email, name, avatar } = req.body || {};

    if (!email) {
      return res.status(400).json({ error: 'Email is required for authentication.' });
    }

    const userId = google_id || `usr_${Buffer.from(email).toString('hex').slice(0, 16)}`;

    // If Database is configured on Vercel
    if (db.isConfigured()) {
      const upsertSql = `
        INSERT INTO users (id, google_id, email, name, avatar, last_login)
        VALUES ($1, $2, $3, $4, $5, CURRENT_TIMESTAMP)
        ON CONFLICT (email) DO UPDATE 
        SET name = EXCLUDED.name, avatar = EXCLUDED.avatar, last_login = CURRENT_TIMESTAMP
        RETURNING id, google_id, email, name, avatar, created_at;
      `;
      const userRes = await db.query(upsertSql, [userId, google_id || null, email, name || 'Anonymous', avatar || '']);
      const dbUser = userRes.rows[0] || { id: userId, email, name, avatar };

      // Fetch user's existing progress
      const progressRes = await db.query(
        `SELECT problem_id, is_solved, is_bookmarked FROM user_progress WHERE user_id = $1`,
        [dbUser.id]
      );
      const solved = [];
      const bookmarked = [];
      progressRes.rows.forEach(row => {
        if (row.is_solved) solved.push(row.problem_id);
        if (row.is_bookmarked) bookmarked.push(row.problem_id);
      });

      // Fetch user's notes
      const notesRes = await db.query(
        `SELECT problem_id, notes FROM user_notes WHERE user_id = $1`,
        [dbUser.id]
      );
      const notes = {};
      notesRes.rows.forEach(row => {
        notes[row.problem_id] = row.notes;
      });

      return res.status(200).json({
        success: true,
        databaseSynced: true,
        user: dbUser,
        progress: { solved, bookmarked, notes }
      });
    }

    // Database not configured yet: Return user profile for local-first storage
    return res.status(200).json({
      success: true,
      databaseSynced: false,
      message: 'Running in local-first storage mode. Configure DATABASE_URL in Vercel for cloud sync.',
      user: {
        id: userId,
        google_id: google_id || null,
        email,
        name: name || 'Google User',
        avatar: avatar || ''
      },
      progress: { solved: [], bookmarked: [], notes: {} }
    });

  } catch (err) {
    console.error('[API Auth] Error:', err);
    return res.status(500).json({ error: 'Authentication failed', details: err.message });
  }
};
