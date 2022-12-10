import sqlite3


class CRUD:
    conn = lambda: None
    cursor = lambda: None

    def __init__(self) -> None:
        self.conn = sqlite3.connect('students.db')
        self.cursor = self.conn.cursor()
        q = "PRAGMA foreign_keys = ON"
        self.cursor.execute(q)
        self.conn.commit()

    def cerrar_conexion(self):
        self.conn.close()

    def crear_tablas(self):
        try:

            # cursor object
            cursor = self.conn.cursor()
            # drop query cursor.execute("DROP TABLE IF EXISTS STUDENT")
            q = "PRAGMA foreign_keys = ON"
            cursor.execute(q)
            # create query
            query = """CREATE TABLE IF NOT EXISTS DOCENTE(
                                ID_DOCENTE INTEGER PRIMARY KEY AUTOINCREMENT,
                                NOMBRE_DOCENTE CHAR(50) NOT NULL, 
                                CI_DOCENTE INTEGER(20), 
                                CODSIS_DOCENTE INTEGER(50))"""
            query2 = """CREATE TABLE IF NOT EXISTS MATERIA(
                                        ID_MATERIA INTEGER PRIMARY KEY AUTOINCREMENT,
                                        NOMBRE_MATERIA CHAR(50) NOT NULL, 
                                        ID_MATERIA_REQUERIDA INTEGER(20),
                                        FOREIGN KEY(ID_MATERIA_REQUERIDA)
                                            REFERENCES MATERIA(ID_MATERIA)
                                            ON DELETE CASCADE
                                            ON UPDATE CASCADE)
                                        """
            query3 = """CREATE TABLE IF NOT EXISTS GRUPO_MATERIA(
                                                ID_GRUPO INTEGER PRIMARY KEY AUTOINCREMENT,
                                                ID_MATERIA INTEGER(20) NOT NULL, 
                                                ID_DOCENTE INTEGER(20) NOT NULL,
                                                NUMERO_ESTUDIANTES INTEGER(20),
                                                NUMERO_GRUPO NOT NULL,
                                                FOREIGN KEY(ID_MATERIA)
                                                    REFERENCES MATERIA(ID_MATERIA)
                                                    ON DELETE CASCADE
                                                    ON UPDATE CASCADE,
                                                FOREIGN KEY(ID_DOCENTE)
                                                    REFERENCES DOCENTE(ID_DOCENTE)
                                                    ON DELETE CASCADE
                                                    ON UPDATE CASCADE)
                                                """
            cursor.execute(query)
            cursor.execute(query2)
            cursor.execute(query3)
            # commit and close
            self.conn.commit()

        except sqlite3.Error as err:
            print("A ocurrido un error durante la creacion de tablas")

    def create_table(self):
        try:

            # cursor object
            cursor = self.conn.cursor()
            # drop query cursor.execute("DROP TABLE IF EXISTS STUDENT")
            q = "PRAGMA foreign_keys = ON"
            cursor.execute(q)
            # create query
            query = """CREATE TABLE IF NOT EXISTS ESTUDIANTE(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            NOMBRE CHAR(50) NOT NULL, 
            CI INTEGER(20), 
            CODSIS INTEGER(50), 
            MATRICULA BOOLEAN )"""
            cursor.execute(query)
            # commit and close
            self.conn.commit()

        except sqlite3.Error as err:
            print("A ocurrido un error durante la creacion de tablas")
    def crear_grupos(self,id_materia,id_docente,nro_estudiantes,nro_grupo):
        try:

            query = (
                'INSERT INTO GRUPO_MATERIA (ID_MATERIA,ID_DOCENTE,NUMERO_ESTUDIANTES,NUMERO_GRUPO) ''VALUES (:ID_MATERIA, :ID_DOCENTE, :NUMERO_ESTUDIANTES, :NUMERO_GRUPO);')
            params = {
                'ID_MATERIA': id_materia,
                'ID_DOCENTE': id_docente,
                'NUMERO_ESTUDIANTES' :nro_estudiantes,
                'NUMERO_GRUPO' : nro_grupo
            }
            self.conn.execute(query, params)
            self.conn.commit()

        except sqlite3.Error as err:
            print("A ocurrido un error durante la escritura" + err)
    def add_materia(self, nombre_materia, id_materia_req, ):
        try:

            query = (
                'INSERT INTO MATERIA (NOMBRE_MATERIA,ID_MATERIA_REQUERIDA) ''VALUES (:NOMBRE_MATERIA, :ID_MATERIA_REQUERIDA);')
            params = {
                'NOMBRE_MATERIA': nombre_materia,
                'ID_MATERIA_REQUERIDA': id_materia_req
            }
            self.conn.execute(query, params)
            self.conn.commit()

        except sqlite3.Error as err:
            print("A ocurrido un error durante la escritura" + err)

    def add_docente(self, nombre, cedula, codigo_sis):
        try:

            query = (
                'INSERT INTO DOCENTE (NOMBRE_DOCENTE,CI_DOCENTE,CODSIS_DOCENTE) ''VALUES (:NOMBRE_DOCENTE, :CI_DOCENTE, :CODSIS_DOCENTE);')
            params = {
                'NOMBRE_DOCENTE': nombre,
                'CI_DOCENTE': cedula,
                'CODSIS_DOCENTE': codigo_sis
            }
            self.conn.execute(query, params)
            self.conn.commit()

        except sqlite3.Error as err:
            print("A ocurrido un error durante la escritura" + err)

    def guardar(self, nombre, cedula, codigo_sis, estado):
        try:

            query = (
                'INSERT INTO ESTUDIANTE (NOMBRE,CI,CODSIS,MATRICULA) ''VALUES (:NOMBRE, :CI, :CODSIS, :MATRICULA);')
            params = {
                'NOMBRE': nombre,
                'CI': cedula,
                'CODSIS': codigo_sis,
                'MATRICULA': estado
            }
            self.conn.execute(query, params)
            self.conn.commit()

        except sqlite3.Error as err:
            print("A ocurrido un error durante la escritura" + err)

    def leer(self):
        try:

            cursor = self.conn.execute("SELECT * from ESTUDIANTE")

            for c in cursor.fetchall():
                print(c)

        except sqlite3.Error as err:
            print("A ocurrido un error durante la lectura")

    def actualizar_estudiante(self, id, ci):
        try:

            query = ("UPDATE ESTUDIANTE set CI = :CI where ID = :ID")
            params = {
                'CI': ci,
                'ID': id
            }
            self.conn.execute(query, params)
            self.conn.commit()
            cursor = self.conn.execute("SELECT * from ESTUDIANTE")
            print(cursor.fetchall())

        except sqlite3.Error as err:
            print("A ocurrido un error durante la actualizacion")

    def eliminar_estudiante(self, id):
        try:

            query = ("DELETE from ESTUDIANTE where :ID;")
            params = {
                'ID': id
            }
            self.conn.execute(query, params)
            self.conn.commit()
            cursor = self.conn.execute("SELECT * from ESTUDIANTE")
            print(cursor.fetchall())
            self.conn.close()
        except sqlite3.Error as err:
            print("A ocurrido un error durante la eliminacion")


if __name__ == '__main__':
    base = CRUD()
    base.crear_tablas()
    base.create_table()
    base.leer()
    # base.actualizar_estudiante(2, 201726)
    base.cerrar_conexion()
