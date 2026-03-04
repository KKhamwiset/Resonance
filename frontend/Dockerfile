FROM node:18-alpine

WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy project files
COPY . .

# Build arguments (needed at build time for Nuxt runtimeConfig.public)
ARG API_URL
ARG ENVIRONMENT
ARG API_IMG_KEY

# Make build args available as env vars during build
ENV API_URL=$API_URL
ENV ENVIRONMENT=$ENVIRONMENT
ENV API_IMG_KEY=$API_IMG_KEY

# Build the application
RUN npm run build

# Set environment variables
ENV HOST=0.0.0.0
ENV PORT=3000

# Expose port
EXPOSE 3000

# Run the built application
CMD ["node", ".output/server/index.mjs"]