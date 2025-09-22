package com.example.blebridge;

//--------------------------------------
// Autor: Fédor Tikhomirov
//--------------------------------------

import android.util.Log;

import org.json.JSONObject;

import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.text.SimpleDateFormat;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.Arrays;
import java.util.Date;

//Esta clase procesa las tramas recibidas y envia los datos contenidos a la BBDD a traves de la API
public class TransporteDatos {
    //Dirección de la instancia EC2
    static final String DIRECCIONAPI = "http://13.37.194.239:5000/datosSensor";

    //Clase para los datos procesados porque Java no tiene structs
    public static class DatosProcesados{
        int contador;
        int C02;
        public int getContador() { return contador; }
        public int getC02() { return C02; }
        public DatosProcesados(int contador, int C02){
            this.contador = contador;
            this.C02 = C02;
        }

    }

    private static int ProcesarCO2(int CO2_original){
        // TODO: Implementar procesado de datos una vez que haya datos a procesar
        return CO2_original;
    }

    //Esta clase devuelve un objeto DatosProcesados (o un error) que obtiene a partir de una TramaIBeacon que se
    //le pasa
    public static DatosProcesados ProcesarTrama(TramaIBeacon trama) throws Exception {
        byte[] majorBytes = trama.getMajor();
        byte[] minorBytes = trama.getMinor();

        int major = ((majorBytes[0] & 0xFF) << 8) | (majorBytes[1] & 0xFF);
        int idMedicion = (major >> 8) & 0xFF;
        int contador = major & 0xFF;

        System.out.println("Raw major: " + Arrays.toString(majorBytes));
        System.out.println("Major int: " + major + " (ID=" + idMedicion + ", contador=" + contador + ")");
        System.out.println("Raw minor: " + Arrays.toString(minorBytes));

        if (idMedicion == 11) {
            int valorCO2 = ((minorBytes[0] & 0xFF) << 8) | (minorBytes[1] & 0xFF);
            valorCO2 = ProcesarCO2(valorCO2);
            System.out.println("CO2: " + valorCO2);

            return new DatosProcesados(contador, valorCO2);
        } else {
            throw new Exception("Medicion leída no es de C02 (ID=" + idMedicion + ")");
        }
    }

    public static void EnviarDatos(DatosProcesados datos){
        try {
            //Obtenemos fecha actual
            SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
            String timestamp = sdf.format(new Date());

            //Construimos el JSON con los datos a enviar
            JSONObject json = new JSONObject();
            json.put("Fecha", timestamp);
            json.put("Contador", datos.getContador());
            json.put("CO2", datos.getC02());

            //Establecemos la conexión y indicamos que es un POST
            URL url = new URL(DIRECCIONAPI);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("POST");
            conn.setRequestProperty("Content-Type", "application/json; utf-8");
            conn.setDoOutput(true);

            // Enviamos los datos
            try (OutputStream os = conn.getOutputStream()){
                byte[] input = json.toString().getBytes("utf-8");
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
