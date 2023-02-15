FROM node:16-alpine

COPY . .
RUN yarn

EXPOSE 8080
ENTRYPOINT ["HOST=0.0.0.0" "yarn", "run", "serve"]
