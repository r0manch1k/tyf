FROM node:18-alpine as build-stage

WORKDIR /frontend
COPY ./frontend/package*.json .

RUN npm install
COPY ./frontend .
RUN npm run build


FROM nginx:latest as production-stage

RUN rm /etc/nginx/conf.d/default.conf
COPY ./.docker/prod/nginx/nginx.conf /etc/nginx/conf.d
COPY --from=build-stage /frontend/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]