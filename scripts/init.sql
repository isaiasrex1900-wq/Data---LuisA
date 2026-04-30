
CREATE TABLE team(
    tem_id CHAR(4),
    tem_name TEXT,

    constraint pk_team primary key (tem_id)

);

CREATE TABLE contestants (
    con_id VARCHAR(4),
    con_name TEXT,
    cell TEXT,
    tem_id CHAR(4),

    constraint pk_contestants primary key (con_id),

    constraint fk_team foreign key (tem_id)
        references team (tem_id)

);

CREATE TABLE proyects (
    pro_id VARCHAR(4),
    pro_name TEXT,
    tem_id CHAR(4),
    status estado_proyecto DEFAULT 'Idea',

    constraint pk_contestants primary key (pro_id),

    constraint fk_team foreign key (tem_id)
        references team (tem_id)

);

CREATE TABLE judges (
    jd_id VARCHAR(4),
    jd_name TEXT,
    tem_id CHAR(4),

    constraint pk_judges primary key (jd_id),

);

CREATE TABLE evaluations (
    ev_id VARCHAR(4),
    tem_id CHAR(4),
    jd_id VARCHAR(4),
    score VARCHAR(2),

    constraint pk_evaluations primary key (ev_id),
    
    constraint fk_team foreign key (tem_id)
        references team (tem_id),

    constraint fk_judges foreign key (jd_id)
        references judges (jd_id)
);


CREATE TABLE historial_estados_proyectos (
    id SERIAL PRIMARY KEY,
    proyecto_id VARCHAR(4) REFERENCES proyects(pro_id),
    estado_anterior estado_proyecto,
    estado_nuevo estado_proyecto,
    fecha_cambio TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Función para registrar el cambio
CREATE OR REPLACE FUNCTION registrar_cambio_estado()
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.status IS DISTINCT FROM NEW.status THEN
        INSERT INTO historial_estados_proyectos (proyecto_id, estado_anterior, estado_nuevo)
        VALUES (OLD.id, OLD.status, NEW.status);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_historial_status
AFTER UPDATE ON proyectos
FOR EACH ROW
EXECUTE FUNCTION registrar_cambio_estado();