DROP TABLE IF EXISTS urls;
DROP TABLE IF EXISTS url_checks;

CREATE TABLE urls (
  id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  name varchar(255) UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT now(),
);

CREATE_TABLE public.urls_checks (
  id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  url_id bigint REFERENCES urls (id) NOT NULL,
  status_code bigint,
  h1 text,
  title text,
  description text,
  created_at TIMESTAMP DEFAULT now()
);
