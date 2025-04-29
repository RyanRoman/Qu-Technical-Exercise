CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create brands table
CREATE TABLE brands (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Create organizations table
CREATE TABLE organizations (
    id UUID PRIMARY KEY,
    brand_id UUID REFERENCES brands(id),
    name VARCHAR(255) NOT NULL
);

-- Create locations table
CREATE TABLE locations (
    id UUID PRIMARY KEY,
    organization_id UUID REFERENCES organizations(id),
    name VARCHAR(255) NOT NULL
);

-- Create electric_sensors table
CREATE TABLE electric_sensors (
    id UUID PRIMARY KEY,
    duid VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    location_id UUID REFERENCES locations(id)
);

-- Create circuits table
CREATE TABLE circuits (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    sensor_id UUID REFERENCES electric_sensors(id),
    name VARCHAR(255) NOT NULL,
    circuit_number INTEGER NOT NULL
);
