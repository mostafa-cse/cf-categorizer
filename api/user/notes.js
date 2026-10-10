/**
 * Vercel Serverless Function: Save User Problem Notes
 * POST /api/user/notes
 */

const db = require('../db');

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { user_id, problem_id, notes } = req.body || {};

  if (!user_id || !problem_id) {
    return res.status(400).json({ error: 'user_id and problem_id are required' });
  }

  if (!db.isConfigured()) {
    return res.status(200).json({
      success: true,
      dbConfigured: false,
      message: 'Saved to local client storage.'
    });
  }

  try {
    const sql = `
      INSERT INTO user_notes (user_id, problem_id, notes, updated_at)
      VALUES ($1, $2, $3, CURRENT_TIMESTAMP)
      ON CONFLICT (user_id, problem_id) DO UPDATE 
      SET notes = EXCLUDED.notes, updated_at = CURRENT_TIMESTAMP
      RETURNING notes;
    `;
    const result = await db.query(sql, [user_id, problem_id, notes || '']);
    return res.status(200).json({
      success: true,
      notes: result.rows[0]?.notes || notes
    });
  } catch (err) {
    console.error('[API Notes POST] Error:', err);
    return res.status(500).json({ error: 'Failed to save notes', details: err.message });
  }
};
