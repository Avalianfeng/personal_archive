import { z } from 'zod';
import { config as dotenvConfig } from 'dotenv';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));

// 优先加载仓库根目录 .env
dotenvConfig({ path: resolve(__dirname, '../../../../.env') });
// 也加载 api 本地 .env（作为覆盖）
dotenvConfig({ path: resolve(__dirname, '../.env') });

const envSchema = z.object({
  LLM_BASE_URL: z.string().default('https://api.deepseek.com/v1'),
  LLM_API_KEY: z.string().min(1, 'LLM_API_KEY is required when LLM_MOCK is false'),
  LLM_MODEL: z.string().default('deepseek-chat'),
  LLM_MOCK: z.enum(['true', 'false']).default('false'),
  DATABASE_PATH: z.string().default('./data/renge-shenqian.db'),
  PORT: z.coerce.number().default(3001),
  NODE_ENV: z.enum(['development', 'production', 'test']).default('development'),
});

export const env = envSchema.parse(process.env);
