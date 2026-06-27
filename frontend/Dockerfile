# ==================== 阶段 1: 编译构建 ====================
FROM node:20-alpine AS build

WORKDIR /app

# 安装依赖（使用 npm ci 保证一致性）
COPY package*.json ./
RUN npm ci

# 复制源码并构建
COPY . .
RUN npm run build

# ==================== 阶段 2: Nginx 托管 ====================
FROM nginx:alpine

# 复制构建产物到 nginx 静态目录
COPY --from=build /app/dist /usr/share/nginx/html

# 自定义 nginx 配置（SPA 路由支持）
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
