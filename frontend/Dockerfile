FROM node:20-alpine AS build
WORKDIR /app
COPY frontend/ . 
ARG REACT_APP_REQUEST_SERVICE_URL
ARG REACT_APP_FORMATTING_SERVICE_URL
ENV REACT_APP_REQUEST_SERVICE_URL=$REACT_APP_REQUEST_SERVICE_URL
ENV REACT_APP_FORMATTING_SERVICE_URL=$REACT_APP_FORMATTING_SERVICE_URL
RUN npm install
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY frontend/nginx.conf /etc/nginx/nginx.conf