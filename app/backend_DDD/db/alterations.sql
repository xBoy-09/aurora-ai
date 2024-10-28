-- Add fields to existing users table
ALTER TABLE users
ADD COLUMN IF NOT EXISTS user_email VARCHAR(100) NOT NULL,
ADD COLUMN IF NOT EXISTS affiliate_id VARCHAR(100) NOT NULL;

-- affiliate enum {none, student}
ALTER TABLE affiliate_details
ALTER COLUMN affiliate_type TYPE affiliate_type_enum USING affiliate_type::text::affiliate_type_enum;


-- Add the foreign key constraint for university_id
-- TODO: Add the foreign key constraint for university_id
ALTER TABLE affiliate_details
ADD CONSTRAINT fk_university_id
FOREIGN KEY (university_id) REFERENCES university(university_id);