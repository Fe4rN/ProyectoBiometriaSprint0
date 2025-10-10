//----------------------------------------------
//  Autor: Fédor Tikhomirov
//  Fecha: 10 de octubre de 2025 
//----------------------------------------------

package com.example.blebridge;

import org.json.JSONObject;

import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;

//  Esta clase envia los datos recibidos en la trama a la API desde el teléfono
public class LogicaNegocio {
    static final String DIRECCIONAPI = "http://13.37.194.239:5000/datosSensor";
        
    //  Enviamos los datos pasados a la direccion de la API
    //         JSON: datos --> EnviarDatos()
    //  Exception | 200 OK <--
    public static void EnviarDatos(JSONObject datos){
        try {
            //Establecemos la conexión y indicamos que es un POST
            URL url = new URL(DIRECCIONAPI);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("POST");
            conn.setRequestProperty("Content-Type", "application/json; utf-8");
            conn.setDoOutput(true);

            // Enviamos los datos
            try (OutputStream os = conn.getOutputStream()){
                byte[] input = datos.toString().getBytes("utf-8");
                os.write(input, 0, input.length);
            }

            //Recibimos la respuesta y desconectamos
            int code = conn.getResponseCode();
            System.out.println("Respuesta del servidor: " + code);
            conn.disconnect();

        } catch (Exception e) {
            //Por que es Java con lo que trabajamos
            e.printStackTrace();
        }
    }
}
