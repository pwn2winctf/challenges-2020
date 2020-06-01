FROM golang:1.14-alpine AS build-env

WORKDIR /app

COPY . .

RUN go mod download

RUN go build

FROM alpine:latest

WORKDIR /app

COPY --from=build-env /app .

RUN apk add --no-cache udev ttf-freefont chromium chromium-chromedriver bash

EXPOSE 80

ENTRYPOINT ["./ademir"]