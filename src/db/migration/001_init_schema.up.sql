CREATE INDEX ON "products" ("code");

CREATE TABLE "products" (
  "id" bigserial PRIMARY KEY,
  "name" varchar NOT NULL,
  "code" varchar NOT NULL,
  "description" varchar NOT NULL,
  "category" varchar NOT NULL,
  "price" decimal NOT NULL,
  "created_at" timestamptz NOT NULL DEFAULT (now())
);

CREATE INDEX ON "products" ("code");
