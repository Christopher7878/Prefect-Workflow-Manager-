Este código implementa un flujo ETL (Extract, Transform, Load) utilizando la biblioteca Prefect para la orquestación de tareas.

![image](https://github.com/user-attachments/assets/65558542-86d7-40b8-a477-17118e714d51)


requests: Realiza solicitudes HTTP.

json: Maneja la conversión entre texto JSON y objetos Python.

namedtuple: Crea estructuras de datos tipo objeto inmutable.

closing: Maneja correctamente recursos como conexiones o cursores.

sqlite3: Interactúa con bases de datos SQLite.

prefect: Se usa para definir tareas y flujos de trabajo.

 Extracción (Extract)

 ![image](https://github.com/user-attachments/assets/506a12b0-b0eb-4ea5-8c5a-0c2ff0275cf4)

 Solicita los 10 registros más recientes de quejas de consumidores desde una API pública del gobierno estadounidense.

Devuelve una lista de objetos JSON con datos sin procesar.

Transformación (Transform)

![image](https://github.com/user-attachments/assets/f290980c-291b-4deb-88d6-75b5f6c1fc4b)

Transforma cada objeto JSON crudo en una estructura namedtuple llamada Complaint.

Extrae campos relevantes y devuelve una lista de quejas estructuradas.

Carga (Load)

![image](https://github.com/user-attachments/assets/3e1882f1-5577-42ed-9e50-bb042050b26c)

Crea (si no existe) una tabla SQLite llamada complaint.

Inserta todas las quejas procesadas en la base de datos local cfpbcomplaints.db.

Flujo ETL y Ejecución

![image](https://github.com/user-attachments/assets/4dc84212-d895-4456-9ba8-7b110b9b93c6)

Orquesta las tres tareas anteriores como un flujo continuo: primero extrae, luego transforma, y finalmente carga los datos y ejecuta el flujo completo si el archivo se corre directamente.

![image](https://github.com/user-attachments/assets/acc550d3-9d73-4663-8594-f0cb239d66ff)


Ventajas del enfoque:
Modularidad: Cada parte del proceso ETL está desacoplada.

Reusabilidad: Las tareas pueden ejecutarse por separado.

Escalabilidad y trazabilidad: Prefect permite rastrear y monitorear tareas, útil para producción.

Persistencia: Los datos se almacenan en una base SQLite local.




