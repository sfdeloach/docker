# Multi-stage Dockerfile for Production
FROM node:lts-alpine3.22 AS build

# Set working directory
WORKDIR /usr/src/app

# Install app dependencies
COPY package*.json ./
RUN npm install

# Bundle app source
COPY . .

# Build the app
RUN npm run build

# Produce a lean production image
FROM nginx:1.29.2-alpine

# Copy built app from the build stage
COPY --from=build /usr/src/app/build /usr/share/nginx/html
