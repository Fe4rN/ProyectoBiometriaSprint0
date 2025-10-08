# Proyecto Biometría - Sprint 0

Este proyecto se centra en la **captura de datos ambientales** desde un modulo BLE y su visualización en una **aplicación web**.

## Tecnologías y Herramientas Utilizadas

- **Arduino**: Para la adquisición de datos desde sensores BLE.  
- **Java**: Lógica de procesamiento y envio de datos.  
- **FastAPI**: API para comunicar los datos con la base de datos.  
- **SQLite**: Base de datos ligera para almacenamiento de datos.  
- **Amazon Web Services (AWS) - EC2**: Despliegue y alojamiento del proyecto en la nube.

## Funcionalidades

- Lectura en tiempo real de sensores BLE.  
- Visualización de datos medioambientales en la web.  
- Almacenamiento y recuperación de datos históricos.

## Recursos

- **Dirección Web**: http://13.37.194.239:5000
- Enlace **Figma** con los diseños y la ingeniería inversa (también incluidos en la carpeta Doc): [Sprint0 Fédor](https://www.figma.com/board/ZXr6GtmPDFBBFq0Fxf57Qd/Sprint0-F%C3%A9dor?node-id=0-1&t=vq2UG07EEHSMFoVu-1)

### 🚀 Despliegue

El proyecto cuenta con tres componentes principales: **Arduino**, **Android** y **Web**, cada uno con su propio proceso de despliegue.

#### **Arduino**
- Subir el archivo **`HolaMundoIBeacon.ino`** a la placa Arduino.  
- Una vez cargado el código, abrir el **Monitor Serial** para verificar la comunicación y la emisión del beacon.

#### **Android**
- Instalar la aplicación generada en un **dispositivo Android 14 o superior**.  
- Asegurarse de otorgar los permisos necesarios para el uso de **Bluetooth y localización**.

#### **Web**
- Subir la carpeta **`Web`** al servidor designado (por ejemplo, en una instancia **AWS EC2**).  
- Verificar que todos los archivos estáticos y dependencias estén correctamente configurados.

### 🧪 Tests

Antes de ejecutar los tests, asegúrate de cumplir con los **prerrequisitos** del entorno.

#### **Prerrequisitos**
- Instalar todas las dependencias necesarias indicadas en el archivo **`requirements.txt`**.

#### **Ejecución**
1. Abrir una terminal de comandos.  
2. Navegar hasta la carpeta **`Web`** del proyecto.  
3. Ejecutar el siguiente comando para correr las pruebas automatizadas: **`pytest -v`**