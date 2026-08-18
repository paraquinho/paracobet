FROM node:20-alpine
WORKDIR /app
COPY package.json ./
RUN corepack enable && pnpm install --no-frozen-lockfile
COPY . .
EXPOSE 3000
CMD ["pnpm", "dev", "--hostname", "0.0.0.0"]
