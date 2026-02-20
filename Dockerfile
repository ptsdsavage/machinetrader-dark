FROM nginx:alpine

# Custom nginx config (clean URLs, redirects, CORS)
COPY nginx/default.conf /etc/nginx/conf.d/default.conf

# Site files (filtered by .dockerignore)
COPY . /usr/share/nginx/html

# Fix permissions so nginx worker can read all files
RUN chmod -R 755 /usr/share/nginx/html && \
    find /usr/share/nginx/html -type f -exec chmod 644 {} +

EXPOSE 80
