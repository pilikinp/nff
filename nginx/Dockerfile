# build stage
FROM node:lts-alpine as build-stage
WORKDIR /app/
COPY needforfeed-vue/package.json /app/
RUN npm cache verify
RUN npm install
COPY needforfeed-vue/ /app/
RUN npm run build

# production stage
FROM nginx:stable-alpine as production-stage
COPY nginx/default.conf /etc/nginx/conf.d/default.conf
COPY site/static /app/static/
COPY site/media /app/media/
COPY --from=build-stage /app/dist/static /app/static/
COPY --from=build-stage /app/dist /app/dist/
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
