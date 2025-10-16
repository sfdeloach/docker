# -- Multi-stage Dockerfile for a React application --
# This Dockerfile uses a multi-stage build to create a lightweight final image.
# The first stage builds the React app, and the second stage serves it using Nginx using the official Nginx image.
# The resulting image will not contain any files from the build stage except the built app.

# Named first stage as 'build'
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

# Final stage
FROM nginx:1.29.2-alpine
# Copy build from the 'build' stage to nginx html folder
COPY --from=build /usr/src/app/build /usr/share/nginx/html
