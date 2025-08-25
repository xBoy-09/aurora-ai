-- user enum {user, admin}
DO $$ 
BEGIN 
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'user_type_enum') THEN 
        CREATE TYPE user_type_enum AS ENUM ('user', 'admin'); 
    END IF; 
END $$;

-- affiliate enum {none, student}
DO $$ 
BEGIN 
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'affiliate_type_enum') THEN 
        CREATE TYPE affiliate_type_enum AS ENUM ('none', 'student'); 
    END IF; 
END $$;

-- Priority levels for feedback and tasks
CREATE TYPE priority_enum AS ENUM ('Low', 'Medium', 'High', 'Critical');

-- Status for feedback and tasks
CREATE TYPE status_enum AS ENUM ('Open', 'In Progress', 'Resolved', 'Closed');

-- Feature names for feedback categorization
CREATE TYPE feature_name_enum AS ENUM ('Chat', 'PDC', 'General');

