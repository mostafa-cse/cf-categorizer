/**
 * Vercel Serverless Function: Health Check & System Status
 * GET /api/health
 */

const db = require('./db');

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');

  const configured = db.isConfigured();
  let dbStatus = 'not_configured';
  let dbLatencyMs = null;

  if (configured) {
    try {
      const start = Date.now();
      const test = await db.query('SELECT 1 as test');
      dbLatencyMs = Date.now() - start;
      dbStatus = test.rows?.length > 0 ? 'connected' : 'error';
    } catch (err) {
      dbStatus = 'connection_failed: ' + err.message;
    }
  }

  return res.status(200).json({
    status: 'ok',
    platform: 'Vercel Serverless',
    timestamp: new Date().toISOString(),
    database: {
      type: 'PostgreSQL',
      configured,
      status: dbStatus,
      latencyMs: dbLatencyMs
    },
    version: '1.0.0'
  });
};
