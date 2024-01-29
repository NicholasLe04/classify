FROM node:20.10.0-alpine as builder

WORKDIR /frontend

COPY ./package*.json ./

RUN npm install

COPY . .

RUN npm run build


FROM nginx:alpine

COPY ./nginx.conf /etc/nginx/conf.d/default.conf

COPY --from=builder /frontend/build /usr/share/nginx/html

EXPOSE 3000

CMD ["nginx", "-g", "daemon off;"]