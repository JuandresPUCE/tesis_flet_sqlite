from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

Base = declarative_base()

#modelos
class CondicionesIniciales(Base):
    __tablename__ = 'condiciones_iniciales'

    id = Column(Integer, primary_key=True)
    temperatura = Column(Float)
    tiempo = Column(Float)
    presion_total = Column(Float)
    presion_parcial = Column(Float)
    fraccion_molar = Column(Float)
    especie_quimica = Column(String)
    tipo_especie = Column(String)
    detalle = Column(String)
    nombre_data = Column(String)
    
    def __str__(self):
        return f"ID: {self.id}, Temperatura: {self.temperatura}, Tiempo: {self.tiempo}, Presión Total: {self.presion_total}, Presión Parcial: {self.presion_parcial}, Fracción Molar: {self.fraccion_molar}, Especie Química: {self.especie_quimica}, Tipo de Especie: {self.tipo_especie}, Detalle: {self.detalle}, Nombre de Data: {self.nombre_data}"
    
class DatosIngresadosCineticos(Base):
    __tablename__ = 'datos_ingresados_cineticos'

    id = Column(Integer, primary_key=True)
    tiempo = Column(Float, nullable=False)
    concentracion = Column(Float)
    otra_propiedad = Column(Float)
    conversion_reactivo_limitante = Column(Float)
    tipo_especie = Column(String)
    id_condiciones_iniciales = Column(Integer)
    nombre_data = Column(String)
    nombre_reaccion = Column(String)
    especie_quimica = Column(String)

class CondicionesManager:
    def __init__(self):
        db_path = r"D:\candidatos_proyectof\tesis_tec\dataReactor\tesis_flet_sqlite\tesis_flet_sqlite\data\data_reactor1.db"
        self.engine = create_engine(f'sqlite:///{db_path}')
        self.Session = sessionmaker(bind=self.engine)

    def add_condicion(self, condicion):
        session = self.Session()
        session.add(condicion)
        session.commit()

    def get_condiciones(self):
        session = self.Session()
        condiciones = session.query(CondicionesIniciales).all()
        return condiciones

    def delete_condicion(self, id):
        session = self.Session()
        condicion = session.query(CondicionesIniciales).filter(CondicionesIniciales.id == id).first()
        if condicion:
            session.delete(condicion)
            session.commit()
            print(f"Condition with ID {id} deleted successfully.")  # Debugging line
        else:
            print(f"No se encontró la condición con id {id}")


    def update_condicion(self, id, new_condicion):
        session = self.Session()
        condicion = session.query(CondicionesIniciales).filter(CondicionesIniciales.id == id).first()
        if condicion:
            for key, value in new_condicion.items():
                setattr(condicion, key, value)
            session.commit()
            print(f"Condition with ID {id} updated successfully.")  # Debugging line
        else:
            print(f"No se encontró la condición con id {id}")

class DatosCineticosMananger:
    def __init__(self):
        db_path = r"D:\candidatos_proyectof\tesis_tec\dataReactor\tesis_flet_sqlite\tesis_flet_sqlite\data\data_reactor1.db"
        self.engine = create_engine(f'sqlite:///{db_path}')
        self.Session = sessionmaker(bind=self.engine)

    def add_dato(self, dato):
        session = self.Session()
        session.add(dato)
        session.commit()

    def get_datos(self):
        session = self.Session()
        datos = session.query(DatosIngresadosCineticos).all()
        return datos
    
    def get_datos_1(self):
        session = self.Session()
        datos = session.query(DatosIngresadosCineticos)
        return datos
    
    def get_datos_por_nombre(self, nombre_data):
        session = self.Session()
        datos = session.query(DatosIngresadosCineticos).filter(DatosIngresadosCineticos.nombre_data == nombre_data)
        return datos

    def delete_dato(self, id):
        session = self.Session()
        dato = session.query(DatosIngresadosCineticos).filter(DatosIngresadosCineticos.id == id).first()
        if dato:
            session.delete(dato)
            session.commit()
            print(f"Data with ID {id} deleted successfully.")  # Debugging line
        else:
            print(f"No se encontró el dato con id {id}")

    def update_dato(self, id, new_dato):
        session = self.Session()
        dato = session.query(DatosIngresadosCineticos).filter(DatosIngresadosCineticos.id == id).first()
        if dato:
            for key, value in new_dato.items():
                setattr(dato, key, value)
            session.commit()
            print(f"Data with ID {id} updated successfully.")  # Debugging line
        else:
            print(f"No se encontró el dato con id {id}")
