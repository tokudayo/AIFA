FROM node:16-alpine

# set our node environment, either development or production
# defaults to production, compose overrides this to development on build and run
ARG NODE_ENV=development
ENV NODE_ENV $NODE_ENV

# you'll likely want the latest npm, regardless of node version, for speed and fixes
# but pin this version for the best stability
RUN npm i npm@latest -g

# Create workdir directory
RUN mkdir -p /app
WORKDIR /app

# Copying source files
COPY . /app

RUN yarn

CMD ["yarn", "start"]
