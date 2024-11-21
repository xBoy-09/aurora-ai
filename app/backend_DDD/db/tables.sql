

-- Create user table
CREATE TABLE IF NOT EXISTS users (
    user_id VARCHAR(100) PRIMARY KEY,
    user_name VARCHAR(100) NOT NULL,
    user_email VARCHAR(100) NOT NULL,
    affiliate_id VARCHAR(100) NOT NULL,
    user_type user_type_enum NOT NULL
    FOREIGN KEY (affiliate_id) REFERENCES affiliate_details(affiliate_id)
);

-- Create user_profile_setup table
CREATE TABLE IF NOT EXISTS user_profile_setup (
    user_id VARCHAR(100) PRIMARY KEY REFERENCES users(user_id),
    university_set_up BOOLEAN NOT NULL,
    courses_set_up BOOLEAN NOT NULL,
    email_verified BOOLEAN NOT NULL
);

-- Create affiliate_details table
CREATE TABLE IF NOT EXISTS affiliate_details (
    affiliate_id VARCHAR(100) SERIAL PRIMARY KEY,
    affiliate_type VARCHAR(50) NOT NULL,
    university_id VARCHAR(100) NOT NULL,
    affiliate_email_regex VARCHAR(100)
    FOREIGN KEY (university_id) REFERENCES university(university_id)
);

-- Create student_details table
CREATE TABLE IF NOT EXISTS student_details (
    student_id SERIAL PRIMARY KEY,
    user_id VARCHAR(100) NOT NULL,
    university_id INT NOT NULL,
    university_linked_email VARCHAR(100) NOT NULL,
    university_school_id INT NOT NULL,
    major VARCHAR(100) NOT NULL,
    expected_graduation_year INT NOT NULL,
    email_otp INT NOT NULL,
    FOREIGN KEY (university_id) REFERENCES university(university_id),
    FOREIGN KEY (university_school_id) REFERENCES university_school(university_school_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);


-- Create university table
CREATE TABLE IF NOT EXISTS university (
    university_id SERIAL PRIMARY KEY,
    university_name VARCHAR(100) NOT NULL,
    email_regex VARCHAR(100),
    university_assistant_id VARCHAR(100)
);

-- Create university_school table
CREATE TABLE IF NOT EXISTS university_school (
    university_school_id SERIAL PRIMARY KEY,
    university_id INT NOT NULL,
    majors_list VARCHAR(100)[],
    school_name VARCHAR(100) NOT NULL,
    school_name_abv VARCHAR(100) NOT NULL,
    university_school_regex VARCHAR(100),
    FOREIGN KEY (university_id) REFERENCES university(university_id)
);


-- Create assistant_details table
CREATE TABLE IF NOT EXISTS assistant_details (
    assistant_id VARCHAR(100) PRIMARY KEY,
    assistant_name VARCHAR(100) NOT NULL,
);

-- Create user_threads table
CREATE TABLE IF NOT EXISTS user_threads (
    thread_id VARCHAR(100) PRIMARY KEY,
    user_id VARCHAR(100) NOT NULL,
    thread_name VARCHAR(100) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Create Eateries Table
CREATE TABLE pdc_eateries (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    link TEXT NOT NULL
);

-- Create MenuItems Table
CREATE TABLE pdc_menu_items (
    id SERIAL PRIMARY KEY,
    eatery_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    image_link TEXT,
    FOREIGN KEY (eatery_id) REFERENCES pdc_eateries (id)
);

-- Create Prices Table
CREATE TABLE pdc_menu_prices (
    id SERIAL PRIMARY KEY,
    menu_item_id INT NOT NULL,
    type VARCHAR(50) NOT NULL, -- 'Full', 'Half', 'Quarter'
    price DECIMAL(10, 2),
    FOREIGN KEY (menu_item_id) REFERENCES pdc_menu_items (id)
);


