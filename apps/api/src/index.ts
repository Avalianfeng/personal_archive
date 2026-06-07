import Fastify from 'fastify';
import cors from '@fastify/cors';
import { env } from './config/env.js';
import { sessionRoutes } from './routes/sessions.js';

const app = Fastify({ logger: true });

// 确保题库可加载（启动时验证）
import './services/questionService.js';

async function main() {
  await app.register(cors, {
    origin: true,
    credentials: true,
  });

  await app.register(sessionRoutes, { prefix: '/api' });

  app.get('/health', async () => ({ status: 'ok', timestamp: new Date().toISOString() }));

  try {
    await app.listen({ port: env.PORT, host: '0.0.0.0' });
    console.log(`人格深潜 API running at http://localhost:${env.PORT}`);
  } catch (err) {
    app.log.error(err);
    process.exit(1);
  }
}

main();
