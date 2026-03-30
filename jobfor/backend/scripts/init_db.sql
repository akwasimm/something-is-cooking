-- PostgreSQL initialization script
-- Runs automatically on first container start via docker-entrypoint-initdb.d

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";     -- UUID generation
CREATE EXTENSION IF NOT EXISTS "pg_trgm";       -- trigram index for full-text search
CREATE EXTENSION IF NOT EXISTS "unaccent";      -- accent-insensitive search
CREATE EXTENSION IF NOT EXISTS vector;          -- vector embeddings

-- Set timezone
SET timezone = 'UTC';
