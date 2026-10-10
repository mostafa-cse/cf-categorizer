/**
 * Verification test for Vercel Serverless Endpoints & Database Layer
 */

const assert = require('assert');
const fs = require('fs');
const path = require('path');

// Mock request and response helpers
function createMockReqRes(method, body = {}, query = {}, headers = {}) {
  const req = {
    method,
    body,
    query,
    headers: { ...headers }
  };
  let statusCode = 200;
  let responseData = null;
  const resHeaders = {};

  const res = {
    setHeader(key, val) {
      resHeaders[key] = val;
    },
    status(code) {
      statusCode = code;
      return this;
    },
    json(data) {
      responseData = data;
      return this;
    },
    end() {
      return this;
    },
    getStatusCode: () => statusCode,
    getData: () => responseData,
    getHeaders: () => resHeaders
  };

  return { req, res };
}

async function runTests() {
  console.log('=================================================================');
  console.log('  [*] VERCEL SERVERLESS & DATABASE LAYER VERIFICATION');
  console.log('=================================================================\n');

  let passed = 0;
  let failed = 0;

  // Test 1: Health Endpoint
  try {
    const healthHandler = require('../api/health.js');
    const { req, res } = createMockReqRes('GET');
    await healthHandler(req, res);
    assert.strictEqual(res.getStatusCode(), 200);
    const data = res.getData();
    assert.strictEqual(data.status, 'ok');
    assert.strictEqual(data.platform, 'Vercel Serverless');
    console.log('[PASS] Test 1: api/health.js -> Status 200, platform verified');
    passed++;
  } catch (e) {
    console.error('[FAIL] Test 1: api/health.js ->', e.message);
    failed++;
  }

  // Test 2: Google Auth Handler (Mock / Fallback)
  try {
    const authHandler = require('../api/auth/google.js');
    const testUser = {
      google_id: 'gid_1234567890',
      email: 'tester@example.com',
      name: 'Mostafa Kamal',
      avatar: 'https://example.com/avatar.png'
    };
    const { req, res } = createMockReqRes('POST', testUser);
    await authHandler(req, res);
    assert.strictEqual(res.getStatusCode(), 200);
    const data = res.getData();
    assert.strictEqual(data.success, true);
    assert.strictEqual(data.user.email, 'tester@example.com');
    console.log('[PASS] Test 2: api/auth/google.js -> Status 200, user profile returned');
    passed++;
  } catch (e) {
    console.error('[FAIL] Test 2: api/auth/google.js ->', e.message);
    failed++;
  }

  // Test 3: User Progress GET & POST
  try {
    const progressHandler = require('../api/user/progress.js');
    
    // GET test
    const { req: getReq, res: getRes } = createMockReqRes('GET', {}, { user_id: 'test_user_1' });
    await progressHandler(getReq, getRes);
    assert.strictEqual(getRes.getStatusCode(), 200);
    const getData = getRes.getData();
    assert(Array.isArray(getData.solved));
    assert(Array.isArray(getData.bookmarked));

    // POST toggle_solved test
    const { req: postReq, res: postRes } = createMockReqRes('POST', {
      user_id: 'test_user_1',
      problem_id: '1497D',
      action: 'toggle_solved'
    });
    await progressHandler(postReq, postRes);
    assert.strictEqual(postRes.getStatusCode(), 200);
    assert.strictEqual(postRes.getData().success, true);
    console.log('[PASS] Test 3: api/user/progress.js -> GET & POST verified');
    passed++;
  } catch (e) {
    console.error('[FAIL] Test 3: api/user/progress.js ->', e.message);
    failed++;
  }

  // Test 4: User Notes POST
  try {
    const notesHandler = require('../api/user/notes.js');
    const { req, res } = createMockReqRes('POST', {
      user_id: 'test_user_1',
      problem_id: '1497D',
      notes: 'Solved using bitmask DP transition trick.'
    });
    await notesHandler(req, res);
    assert.strictEqual(res.getStatusCode(), 200);
    assert.strictEqual(res.getData().success, true);
    console.log('[PASS] Test 4: api/user/notes.js -> Note saved successfully');
    passed++;
  } catch (e) {
    console.error('[FAIL] Test 4: api/user/notes.js ->', e.message);
    failed++;
  }

  // Test 5: Verify Static Assets & Config files for Vercel
  try {
    assert(fs.existsSync(path.join(__dirname, '../vercel.json')), 'vercel.json missing');
    assert(fs.existsSync(path.join(__dirname, '../index.html')), 'index.html missing');
    assert(fs.existsSync(path.join(__dirname, '../static/auth.js')), 'static/auth.js missing');
    assert(fs.existsSync(path.join(__dirname, '../static/app.js')), 'static/app.js missing');
    assert(fs.existsSync(path.join(__dirname, '../data/problems_catalog.json')), 'data/problems_catalog.json missing');
    console.log('[PASS] Test 5: Static assets, catalog & vercel.json verified');
    passed++;
  } catch (e) {
    console.error('[FAIL] Test 5: Static verification ->', e.message);
    failed++;
  }

  console.log('\n=================================================================');
  console.log(`  [+] VERCEL TEST SUITE FINISHED: ${passed} PASSED | ${failed} FAILED`);
  console.log('=================================================================');

  if (failed > 0) process.exit(1);
}

runTests();
