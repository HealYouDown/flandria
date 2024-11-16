# syntax=docker.io/docker/dockerfile:1.7-labs
# Stage 1: Builder
FROM node:22-alpine AS builder
WORKDIR /app

# Cache dependencies
COPY package*.json ./
RUN npm ci

# Copy the rest of the application code, excluding nginx config. See below
COPY --exclude=nginx/*  . .

# Build the application
ARG API_URL
ENV VITE_API_URL=$API_URL
RUN npm run codegen && npm run build

# Stage 2: Nginx
FROM nginx:1.25-alpine AS nginx

# Copy built files from builder stage
COPY --from=builder /app/dist /usr/share/nginx/flandria

# Copy custom Nginx configuration. Do it last, so that we don't have to rebuild all layers for config changes.
COPY ./nginx/nginx.conf /etc/nginx/nginx.conf

# Entrypoint for Nginx
CMD ["nginx", "-g", "daemon off;"]