import csv
import os

def menu_principal():
    while True:
        print("\nMenu Principal")
        print("1. Cargar datos en el archivo de pacientes")
        print("2. Cargar datos en el archivo de consultas")
        print("3. Búsqueda y visualización de datos")
        print("4. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            cargar_datos_pacientes()
        elif opcion == '2':
            cargar_datos_consultas()
        elif opcion == '3':
            busqueda_visualizacion()
        elif opcion == '4':
            break
        else:
            print("Opción no válida. Intente de nuevo.")

def cargar_datos_pacientes():
    archivo_pacientes = "pacientes.csv"
    
    with open(archivo_pacientes, mode='a', newline='') as file:
        writer = csv.writer(file)
        
        numero_historia = input("Ingrese el número de historia clínica: ").strip()
        nombre_apellido = input("Ingrese el nombre y apellido del paciente (en mayúsculas): ").strip().upper()
        prepaga = input("Ingrese la prepaga u obra social: ").strip()
        
        # Verificar unicidad del número de historia clínica
        if not verificar_unicidad_historia(numero_historia, archivo_pacientes):
            print("Error: El número de historia clínica ya existe.")
            return
        
        writer.writerow([numero_historia, nombre_apellido, prepaga])
        print("Datos del paciente cargados exitosamente.")

def verificar_unicidad_historia(numero_historia, archivo_pacientes):
    if not os.path.exists(archivo_pacientes):
        return True
    
    with open(archivo_pacientes, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == numero_historia:
                return False
    return True

def cargar_datos_consultas():
    archivo_consultas = "consultas.csv"
    archivo_pacientes = "pacientes.csv"
    
    with open(archivo_consultas, mode='a', newline='') as file:
        writer = csv.writer(file)
        
        numero_historia = input("Ingrese el número de historia clínica: ").strip()
        diagnostico = input("Ingrese el diagnóstico (en mayúsculas): ").strip().upper()
        fecha = input("Ingrese la fecha (AAAAMMDD): ").strip()
        
        # Verificar que el paciente exista
        if not verificar_existencia_paciente(numero_historia, archivo_pacientes):
            print("Error: El paciente no existe.")
            return
        
        writer.writerow([numero_historia, diagnostico, fecha])
        print("Datos de la consulta cargados exitosamente.")

def verificar_existencia_paciente(numero_historia, archivo_pacientes):
    if not os.path.exists(archivo_pacientes):
        return False
    
    with open(archivo_pacientes, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == numero_historia:
                return True
    return False

def busqueda_visualizacion():
    archivo_pacientes = "pacientes.csv"
    archivo_consultas = "consultas.csv"
    
    nombre_busqueda = input("Ingrese el nombre del paciente (todo o parte, en mayúsculas): ").strip().upper()
    
    pacientes_encontrados = []
    with open(archivo_pacientes, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if nombre_busqueda in row[1]:
                pacientes_encontrados.append(row)
    
    if not pacientes_encontrados:
        print("No se encontraron pacientes con ese nombre.")
        return
    
    print("\nPacientes encontrados:")
    for i, paciente in enumerate(pacientes_encontrados):
        print(f"{i+1}. {paciente[1]} (Historia Clínica: {paciente[0]})")
    
    seleccion = int(input("\nSeleccione un paciente por número: ")) - 1
    paciente_seleccionado = pacientes_encontrados[seleccion]
    
    print(f"\nConsultas para el paciente {paciente_seleccionado[1]} (Historia Clínica: {paciente_seleccionado[0]}):")
    with open(archivo_consultas, mode='r') as file:
        reader = csv.reader(file)
        consultas = [row for row in reader if row[0] == paciente_seleccionado[0]]
    
    consultas.sort(key=lambda x: x[2])  # Ordenar por fecha
    
    for consulta in consultas:
        print(f"Fecha: {consulta[2]}, Diagnóstico: {consulta[1]}")

if __name__ == "__main__":
    menu_principal()
