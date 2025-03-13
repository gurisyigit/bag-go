# Stage 1: Build React frontend
FROM node:20 AS frontend

WORKDIR /app/frontend

COPY frontend/package.json ./
RUN yarn install

COPY frontend/ ./
RUN yarn build

# Stage 2: Build Django backend
FROM python:3.13 AS backend
#test 
WORKDIR /app 

COPY requirements.txt ./
RUN pip install -r requirements.txt
#test
COPY backend/ /app/backend/
#test
COPY manage.py /app/
RUN rm -f /app/backend/manage.py
# Copy built frontend to Django static files
COPY --from=frontend /app/frontend/dist /app/backend/static

# Expose port for Django
EXPOSE 8000

# Run Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
