import pino from 'pino';
import { createWriteStream, existsSync, mkdirSync } from 'fs';
import { join } from 'path';

// Ensure 'logs' directory exists relative to CWD
const logsDir = join(process.cwd(), 'logs');
if (!existsSync(logsDir)) {
    mkdirSync(logsDir, { recursive: true });
}

// Create a writable stream to 'logs/main.log'
const logStream = createWriteStream(join(logsDir, 'main.log'), { flags: 'a' });

// Configure pino
const logger = pino({
    timestamp: pino.stdTimeFunctions.isoTime,
    formatters: {
        level(label) {
            return { level: label };
        }
    }
}, logStream);

export { logger };
