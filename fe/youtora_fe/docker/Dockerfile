# build stage
FROM node:lts-alpine as build-stage
WORKDIR /youtora_fe
COPY ../package*.json ./
RUN npm install --silent
COPY ./ .
RUN npm run build --quiet

# production stage
FROM nginx as production-stage
RUN mkdir /youtora_fe
COPY --from=build-stage /youtora_fe/dist /youtora_fe
COPY ../conf/nginx.conf /etc/nginx/nginx.conf

EXPOSE 3000
CMD ["nginx", "-g", "daemon off;"]