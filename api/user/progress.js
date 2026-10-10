/**
 * Vercel Serverless Function: User Progress (Solved / Bookmarks)
 * GET & POST /api/user/progress
 */

const db = require('../db');

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  // GET: Fetch progress for user
  if (req.method === 'GET') {
    const userId = req.query.user_id || req.headers['x-user-id'];
    if (!userId) {
      return res.status(200).json({
        solved: [],
        bookmarked: [],
        notes: {},
        dbConfigured: db.isConfigured()
      });
    }

    if (!db.isConfigured()) {
      return res.status(200).json({
        solved: [],
        bookmarked: [],
        notes: {},
        dbConfigured: false
      });
    }

    try {
      const progressRes = await db.query(
        `SELECT problem_id, is_solved, is_bookmarked FROM user_progress WHERE user_id = $1`,
        [userId]
      );
      const solved = [];
      const bookmarked = [];
      progressRes.rows.forEach(r => {
        if (r.is_solved) solved.push(r.problem_id);
        if (r.is_bookmarked) bookmarked.push(r.problem_id);
      });

      const notesRes = await db.query(
        `SELECT problem_id, notes FROM user_notes WHERE user_id = $1`,
        [userId]
      );
      const notes = {};
      notesRes.rows.forEach(r => {
        notes[r.problem_id] = r.notes;
      });

      return res.status(200).json({
        solved,
        bookmarked,
        notes,
        dbConfigured: true
      });
    } catch (err) {
      console.error('[API Progress GET] Error:', err);
      return res.status(500).json({ error: 'Failed to fetch progress', details: err.message });
    }
  }

  // POST: Toggle solved or bookmark
  if (req.method === 'POST') {
    const { user_id, problem_id, action, is_solved, is_bookmarked } = req.body || {};

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
      if (action === 'toggle_solved') {
        const sql = `
          INSERT INTO user_progress (user_id, problem_id, is_solved, is_bookmarked, updated_at)
          VALUES ($1, $2, TRUE, FALSE, CURRENT_TIMESTAMP)
          ON CONFLICT (user_id, problem_id) DO UPDATE 
          SET is_solved = NOT user_progress.is_solved, updated_at = CURRENT_TIMESTAMP
          RETURNING is_solved, is_bookmarked;
        `;
        const result = await db.query(sql, [user_id, problem_id]);
        const row = result.rows[0];
        return res.status(200).json({
          success: true,
          is_solved: Boolean(row?.is_solved),
          is_bookmarked: Boolean(row?.is_bookmarked)
        });
      }

      if (action === 'toggle_bookmark') {
        const sql = `
          INSERT INTO user_progress (user_id, problem_id, is_solved, is_bookmarked, updated_at)
          VALUES ($1, $2, FALSE, TRUE, CURRENT_TIMESTAMP)
          ON CONFLICT (user_id, problem_id) DO UPDATE 
          SET is_bookmarked = NOT user_progress.is_bookmarked, updated_at = CURRENT_TIMESTAMP
          RETURNING is_solved, is_bookmarked;
        `;
        const result = await db.query(sql, [user_id, problem_id]);
        const row = result.rows[0];
        return res.status(200).json({
          success: true,
          is_solved: Boolean(row?.is_solved),
          is_bookmarked: Boolean(row?.is_bookmarked)
        });
      }

      // Explicit set
      const sql = `
        INSERT INTO user_progress (user_id, problem_id, is_solved, is_bookmarked, updated_at)
        VALUES ($1, $2, $3, $4, CURRENT_TIMESTAMP)
        ON CONFLICT (user_id, problem_id) DO UPDATE 
        SET is_solved = COALESCE($3, user_progress.is_solved),
            is_bookmarked = COALESCE($4, user_progress.is_bookmarked),
            updated_at = CURRENT_TIMESTAMP
        RETURNING is_solved, is_bookmarked;
      `;
      const result = await db.query(sql, [user_id, problem_id, is_solved, is_bookmarked]);
      const row = result.rows[0];
      return res.status(200).json({
        success: true,
        is_solved: Boolean(row?.is_solved),
        is_bookmarked: Boolean(row?.is_bookmarked)
      });

    } catch (err) {
      console.error('[API Progress POST] Error:', err);
      return res.status(500).json({ error: 'Failed to update progress', details: err.message });
    }
  }

  return res.status(405).json({ error: 'Method not allowed' });
};
