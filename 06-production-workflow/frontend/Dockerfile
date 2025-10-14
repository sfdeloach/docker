# 1st stage - build environment
# 'as builder' names the stage so we can reference it later
FROM node:16-alpine as builder

# Set working directory
WORKDIR '/app'

# Copy package.json and install dependencies
COPY package.json . 

# Install dependencies
RUN npm install

# Copy all files
COPY . . 

# Build the app
RUN npm run build

# 2nd stage - production environment
# Use nginx to serve the app
FROM nginx

# Copy built files from builder stage to nginx html folder
COPY --from=builder /app/build /usr/share/nginx/html

# nginx does not need a custom command, it will start by default
