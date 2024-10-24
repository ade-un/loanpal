START TRANSACTION;

DROP TABLE IF EXISTS auth_group;
CREATE TABLE auth_group (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(150) NOT NULL UNIQUE,
    PRIMARY KEY (id)
);

DROP TABLE IF EXISTS auth_group_permissions;
CREATE TABLE auth_group_permissions (
    id INT NOT NULL AUTO_INCREMENT,
    group_id INT NOT NULL,
    permission_id INT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (group_id) REFERENCES auth_group(id) ON DELETE CASCADE,
    FOREIGN KEY (permission_id) REFERENCES auth_permission(id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS auth_permission;
CREATE TABLE auth_permission (
    id INT NOT NULL AUTO_INCREMENT,
    content_type_id INT NOT NULL,
    codename VARCHAR(100) NOT NULL,
    name VARCHAR(255) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS django_admin_log;
CREATE TABLE django_admin_log (
    id INT NOT NULL AUTO_INCREMENT,
    object_id TEXT,
    object_repr VARCHAR(200) NOT NULL,
    action_flag SMALLINT UNSIGNED NOT NULL CHECK (action_flag >= 0),
    change_message TEXT NOT NULL,
    content_type_id INT,
    user_id BIGINT NOT NULL,
    action_time DATETIME NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES loan_management_customuser(id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS django_content_type;
CREATE TABLE django_content_type (
    id INT NOT NULL AUTO_INCREMENT,
    app_label VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    PRIMARY KEY (id)
);

DROP TABLE IF EXISTS django_migrations;
CREATE TABLE django_migrations (
    id INT NOT NULL AUTO_INCREMENT,
    app VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    applied DATETIME NOT NULL,
    PRIMARY KEY (id)
);

DROP TABLE IF EXISTS django_session;
CREATE TABLE django_session (
    session_key VARCHAR(40) NOT NULL,
    session_data TEXT NOT NULL,
    expire_date DATETIME NOT NULL,
    PRIMARY KEY (session_key)
);

DROP TABLE IF EXISTS loan_management_application;
CREATE TABLE loan_management_application (
    id INT NOT NULL AUTO_INCREMENT,
    amount DECIMAL(10,2) NOT NULL,
    purpose VARCHAR(255) NOT NULL,
    duration INT,
    status VARCHAR(20) NOT NULL,
    submission_date DATETIME NOT NULL,
    review_date DATETIME,
    user_id BIGINT NOT NULL,
    employer_name VARCHAR(100) NOT NULL,
    job_title VARCHAR(100) NOT NULL,
    monthly_income INT,
    can_reapply BOOLEAN NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES loan_management_customuser(id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS loan_management_customuser;
CREATE TABLE loan_management_customuser (
    id INT NOT NULL AUTO_INCREMENT,
    password VARCHAR(128) NOT NULL,
    username VARCHAR(150) NOT NULL UNIQUE,
    first_name VARCHAR(150) NOT NULL,
    last_name VARCHAR(150) NOT NULL,
    is_staff BOOLEAN NOT NULL,
    is_active BOOLEAN NOT NULL,
    date_joined DATETIME NOT NULL,
    email VARCHAR(254) NOT NULL,
    role VARCHAR(20) NOT NULL,
    last_login DATETIME,
    is_superuser BOOLEAN NOT NULL,
    PRIMARY KEY (id)
);

DROP TABLE IF EXISTS loan_management_customuser_groups;
CREATE TABLE loan_management_customuser_groups (
    id INT NOT NULL AUTO_INCREMENT,
    customuser_id BIGINT NOT NULL,
    group_id INT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (customuser_id) REFERENCES loan_management_customuser(id) ON DELETE CASCADE,
    FOREIGN KEY (group_id) REFERENCES auth_group(id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS loan_management_customuser_user_permissions;
CREATE TABLE loan_management_customuser_user_permissions (
    id INT NOT NULL AUTO_INCREMENT,
    customuser_id BIGINT NOT NULL,
    permission_id INT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (customuser_id) REFERENCES loan_management_customuser(id) ON DELETE CASCADE,
    FOREIGN KEY (permission_id) REFERENCES auth_permission(id) ON DELETE CASCADE
);

INSERT INTO auth_permission (content_type_id, codename, name) VALUES
(1, 'add_logentry', 'Can add log entry'),
(1, 'change_logentry', 'Can change log entry'),
(1, 'delete_logentry', 'Can delete log entry'),
(1, 'view_logentry', 'Can view log entry'),
(2, 'add_permission', 'Can add permission'),
(2, 'change_permission', 'Can change permission'),
(2, 'delete_permission', 'Can delete permission'),
(2, 'view_permission', 'Can view permission'),
(3, 'add_group', 'Can add group'),
(3, 'change_group', 'Can change group'),
(3, 'delete_group', 'Can delete group'),
(3, 'view_group', 'Can view group'),
(4, 'add_contenttype', 'Can add content type'),
(4, 'change_contenttype', 'Can change content type'),
(4, 'delete_contenttype', 'Can delete content type'),
(4, 'view_contenttype', 'Can view content type'),
(5, 'add_session', 'Can add session'),
(5, 'change_session', 'Can change session'),
(5, 'delete_session', 'Can delete session'),
(5, 'view_session', 'Can view session'),
(6, 'add_customuser', 'Can add user'),
(6, 'change_customuser', 'Can change user'),
(6, 'delete_customuser', 'Can delete user'),
(6, 'view_customuser', 'Can view user'),
(7, 'add_application', 'Can add application'),
(7, 'change_application', 'Can change application'),
(7, 'delete_application', 'Can delete application'),
(7, 'view_application', 'Can view application'),
(8, 'add_user', 'Can add user'),
(8, 'change_user', 'Can change user'),
(8, 'delete_user', 'Can delete user'),
(8, 'view_user', 'Can view user');

COMMIT;
