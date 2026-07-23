CREATE TYPE user_global_role AS ENUM (
    'APPLICANT',
    'ROOMMATE',
    'OWNER'
);

CREATE TYPE roommate_role AS ENUM (
    'BASIC',
    'LEAD'
);

CREATE TYPE application_status AS ENUM (
    'PENDING',
    'ACCEPTED',
    'REJECTED'
);

CREATE TYPE task_status AS ENUM (
    'TODO',
    'IN_PROGRESS',
    'DONE'
);

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(30),
    global_role user_global_role NOT NULL DEFAULT 'APPLICANT',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE colocations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    owner_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(150) NOT NULL,
    description TEXT,
    address VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    postal_code VARCHAR(20) NOT NULL,
    rent_amount NUMERIC(10, 2) NOT NULL,
    max_capacity INT NOT NULL,
    is_available BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE colocation_members (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    colocation_id UUID NOT NULL REFERENCES colocations(id) ON DELETE CASCADE,
    user_id UUID UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role roommate_role NOT NULL DEFAULT 'BASIC',
    joined_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE colocation_applications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    colocation_id UUID NOT NULL REFERENCES colocations(id) ON DELETE CASCADE,
    applicant_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    status application_status NOT NULL DEFAULT 'PENDING',
    message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(colocation_id, applicant_id)
);

CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    colocation_id UUID NOT NULL REFERENCES colocations(id) ON DELETE CASCADE,
    assigned_to_id UUID REFERENCES users(id) ON DELETE SET NULL,
    title VARCHAR(150) NOT NULL,
    description TEXT,
    status task_status NOT NULL DEFAULT 'TODO',
    due_date TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    colocation_id UUID NOT NULL REFERENCES colocations(id) ON DELETE CASCADE,
    sender_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_colocations_city ON colocations(city);
CREATE INDEX idx_colocations_owner ON colocations(owner_id);
CREATE INDEX idx_applications_applicant ON colocation_applications(applicant_id);
CREATE INDEX idx_applications_colocation ON colocation_applications(colocation_id);
CREATE INDEX idx_tasks_colocation ON tasks(colocation_id);
CREATE INDEX idx_messages_colocation ON messages(colocation_id, created_at);