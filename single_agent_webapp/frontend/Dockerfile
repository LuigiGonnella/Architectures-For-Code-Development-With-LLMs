# Frontend Dockerfile
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files
COPY single_agent_webapp/frontend/package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY single_agent_webapp/frontend/ ./

# Build the application
RUN npm run build

# Production image
FROM node:18-alpine AS runner

WORKDIR /app

ENV NODE_ENV production

# Copy necessary files
COPY --from=builder /app/next.config.js ./
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/package.json ./package.json

# Expose port
EXPOSE 3000

# Run the application  
CMD sh -c "echo ''; echo 'Frontend: http://localhost:3000'; echo 'Backend:  http://localhost:8000'; echo ''; node server.js"
