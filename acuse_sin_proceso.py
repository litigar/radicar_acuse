import csv
import os
import requests
import re
from dotenv import load_dotenv

# from base64 import b64decode
from datetime import date
from concurrent.futures import ProcessPoolExecutor
from liti_log import UtilLog
from admin_user import admin_user
from file_system import getCsvToBase64, getPdfToBase64, crear_directorio


# C:\DocJairo\desarrollo\consumirApiPy\ve_cons\Scripts\activate
# ojo, actualizar la tarea --> "tarea":"radicarAcuseSinProceso"

class acusar_sin_proceso(object):
    """Obtiene los pdfs de una solicitud de radicaciones"""

    def __init__(self):
        # super(acusar_sin_proceso, self).__init__()
        crear_directorio("logs")
        self.path_logs = "logs/"
        crear_directorio("pdfs")
        self.path_pdfs = "pdfs/"
        # Para que funcionen los hilos NLS_LANG
        os.environ["NLS_LANG"] = "SPANISH_SPAIN.UTF8"
        load_dotenv()
        file_log = "acusar_sin_proceso-" + str(date.today()) + ".log"
        UtilLog.get_instance().set_file_name(self.path_logs + file_log)

        self.file_csv = "cargue_masivo.csv"
        # print(f"local_path {self.local_path}")
        # print(f"init username {self.username}")
        # print(f"init usr_dicc {self.usr_dicc}")
        try:
            self.procesar_desde_fila = int(os.environ.get("procesar_desde_fila"))
        except:
            self.procesar_desde_fila = 0
            UtilLog.get_instance().write("No existe procesar_desde_fila")
        try:
            self.masivo_file_id = os.environ.get("numero_ejecucion")
        except:
            self.masivo_file_id = 0
            UtilLog.get_instance().write("No existe masivo_file_id")

        UtilLog.get_instance().write(f"init procesar_desde_fila {self.procesar_desde_fila}")
        UtilLog.get_instance().write(f"init masivo_file_id {self.masivo_file_id}")

    __instance = None
    Lista = []

    def __str__(self):
        return "acusar_sin_proceso Singleton "

    def __new__(cls):
        if not acusar_sin_proceso.__instance:
            acusar_sin_proceso.__instance = object.__new__(cls)
        return acusar_sin_proceso.__instance

    @staticmethod
    def get_instance():
        if not acusar_sin_proceso.__instance:
            acusar_sin_proceso.__instance = acusar_sin_proceso()
        return acusar_sin_proceso.__instance

    def generar_resumen(self):
        # UtilLog.get_instance().write(f"generar_resumen INICIO ")
        endpoint = admin_user.get_instance().url + "resumen_cargue/"
        token = "Token " + admin_user.get_instance().get_token()
        # print(f"generar_resumen " + "b" * 10)
        # token='Token c3a16a55b7ebdc559c65a0e17c58197dc719061f'
        headers = {"Content-Type": "application/json;", "Authorization": token}
        # reponse=requests.get(endpoint, params={'pk':2})
        # print(f"generar_resumen radicacion_id {radicacion_id}")
        reponse = requests.post(
            endpoint,
            headers=headers,
            json={"masivo_file_id": self.masivo_file_id, "len_registros_csv": len(self.lista_registros_csv) - 1},
        )
        UtilLog.get_instance().write(
            f"generar_resumen reponse.status_code {str(reponse.status_code)} masivo_file_id {str(self.masivo_file_id)}"
        )
        # print(reponse)
        # print(reponse.url)
        json_item = reponse.json()
        # print(f"generar_resumen json_item {json_item}")

        if reponse.status_code == 201:
            # print(f"generar_resumen nombre_archivo {json_item['nombre_archivo']}")
            # UtilLog.get_instance().write(f"generar_resumen solicitud_id {str(json_item['radicado_id'])}")
            if json_item["estado"] == "ok":
                mensaje = f"generar_resumen masivo_file_id {str(self.masivo_file_id)} "
                mensaje += f" resumen {str(json_item['resumen'])} - ok"
                UtilLog.get_instance().write(mensaje)
                return True
            else:
                mensaje = f"generar_resumen masivo_file_id {str(self.masivo_file_id)} "
                mensaje += f" resumen {str(json_item['resumen'])} - error"
                UtilLog.get_instance().write(mensaje)
                return False
        else:
            UtilLog.get_instance().write(
                f"generar_resumen Else {str(reponse.status_code)} - masivo_file_id {str(self.masivo_file_id)}"
            )
            return False

    def enviar_registro_y_adjunto(self, payload):
        # UtilLog.get_instance().write(f"enviar_registro_y_adjunto payload ")
        endpoint = admin_user.get_instance().url + "acusar_sin_proceso/"
        token = "Token " + admin_user.get_instance().get_token()
        # print(f"enviar_registro_y_adjunto " + "b" * 10)
        # token='Token c3a16a55b7ebdc559c65a0e17c58197dc719061f'
        headers = {"Content-Type": "application/json;", "Authorization": token}
        # reponse=requests.get(endpoint, params={'pk':2})
        # print(f"enviar_registro_y_adjunto radicacion_id {radicacion_id}")
        reponse = requests.post(endpoint, headers=headers, json=payload)
        UtilLog.get_instance().write(
            f"enviar_registro_y_adjunto status_code {reponse.status_code} numero_fila {str(payload['numero_registro'])}"
        )
        # print(reponse)
        # print(reponse.url)
        json_item = reponse.json()
        # print(f"enviar_registro_y_adjunto json_item {json_item}")

        if reponse.status_code == 201:
            # print(f"enviar_registro_y_adjunto nombre_archivo {json_item['nombre_archivo']}")
            # UtilLog.get_instance().write(f"enviar_registro_y_adjunto solicitud_id {str(json_item['identificador'])}")
            mensaje = f"enviar_registro_y_adjunto numero_fila {str(payload['numero_registro'])}"
            mensaje += f" solicitud_id {str(json_item['identificador'])}"
            mensaje += f" resultado {str(json_item['resultado'])}"
            if json_item["estado"] == "ok":
                UtilLog.get_instance().write(mensaje + " - ok")
                return True
            else:
                UtilLog.get_instance().write(mensaje + " - error")
                return False
        else:
            mensaje = f"enviar_registro_y_adjunto Else {str(reponse.status_code)} "
            mensaje += f"- numero_fila {str(payload['numero_registro'])}"
            UtilLog.get_instance().write(mensaje)
            return False

    def get_json_datos_registro(self, registro, numero_fila, file_name, file_64):
        columnas = []
        columnas.append(registro.split(";"))
        # print(f"registro {registro}")
        # print(f"columnas[0] {columnas[0]}")
        # print(f"columnas[0][1] {columnas[0][1]}")

        radicado_id = ""  # 0
        fecha_radicacion = ""  # # 31/03/2022
        folios_dependiente = ""  # 1
        costo_impresion = ""  # 0
        

        try:
            radicado_id = columnas[0][0]  # 0
        except Exception as e:
            UtilLog.get_instance().write(f"get_json_datos_registro radicado_id(solicitud_id) {e}")
        try:
            proceso_id = columnas[0][1]  # 
        except Exception as e:
            UtilLog.get_instance().write(f"get_json_datos_registro proceso_id(identificador) {e}")
        try:
            despacho_id = columnas[0][2]  # 
        except Exception as e:
            UtilLog.get_instance().write(f"get_json_datos_registro despacho_id {e}")
        try:
            fecha_radicacion = columnas[0][3]  # 
        except Exception as e:
            UtilLog.get_instance().write(f"get_json_datos_registro fecha_radicacion {e}")
        try:
            folios_dependiente = columnas[0][4]  # 
        except Exception as e:
            UtilLog.get_instance().write(f"get_json_datos_registro folios_dependiente {e}")
        try:
            costo_impresion = columnas[0][5]  # 
        except Exception as e:
            UtilLog.get_instance().write(f"get_json_datos_registro costo_impresion {e}")

        datos = {
            "masivo_file_id": self.masivo_file_id,
            "numero_registro": numero_fila,
            "radicado_id": radicado_id,  # 0,
            "proceso_id": proceso_id,  # 0,
            "despacho_id": despacho_id,  # 0,
            "fecha_radicacion": fecha_radicacion,  # "31/03/2022",
            "folios_dependiente": folios_dependiente,  # "1",
            "costo_impresion": costo_impresion,  # "0",
            "creado_desde": "api-acusar_sin_proceso",
            "username": admin_user.get_instance().username,  # "JVEGA",
            "archivo_name": file_name,  # "algun_nombre.pdf or .zip",
            "archivo_64": file_64,
        }

        # print(datos)
        return datos

    def get_file_row(self, numero_fila):
        """
        Obtiene el archivo pdf/zip del numero de la fila a procesar
        """
        # print(f"get_file_row numero_fila {numero_fila} inicio")
        for archivo in self.lista_archivos_pdf_zip:
            if numero_fila == int(archivo.split("_")[0]):
                mensaje = f"Buscando archivo - row_num {str(numero_fila)} | "
                mensaje += f"num_file {str(archivo.split('_')[0])} | archivo {archivo} --> encontrado"
                UtilLog.get_instance().write(mensaje)
                return archivo
        # print(f"get_file_row numero_fila {numero_fila} no encontrado")
        return ""

    def fila_fue_creada(self, numero_fila):
        UtilLog.get_instance().write("cliente fila_fue_creada - inicio")
        endpoint = admin_user.get_instance().url + "fila_fue_creada/"
        token = "Token " + admin_user.get_instance().get_token()
        # token='Token c3a16a55b7ebdc559c65a0e17c58197dc719061f'

        """
        print(f'* fila_fue_creada - masivo_file_id {self.masivo_file_id}')
        print(f'* fila_fue_creada - numero_fila {numero_fila}')
        print(f'* fila_fue_creada - token {token}')
        print(f'* fila_fue_creada - endpoint {endpoint}')
        """

        headers = {"Content-Type": "application/json;", "Authorization": token}
        reponse = requests.get(
            endpoint, headers=headers, params={"masivo_file_id": self.masivo_file_id, "numero_fila": numero_fila}
        )
        UtilLog.get_instance().write(
            f"fila_fue_creada reponse.status_code {reponse.status_code} numero_fila {str(numero_fila)}"
        )
        # print(reponse)
        # print(reponse.url)
        json_item = reponse.json()
        print(f"fila_fue_creada json_item {json_item}")

        if reponse.status_code == 200:
            # print(f"fila_fue_creada nombre_archivo {json_item['nombre_archivo']}")
            # UtilLog.get_instance().write(f"fila_fue_creada solicitud_id {str(json_item['radicado_id'])}")
            if json_item["estado"] == "ok":
                mensaje = f"fila_fue_creada numero_fila {str(numero_fila)}"
                mensaje += f" solicitud_id {str(json_item['identificador'])} - fila ya habia sido creada"
                UtilLog.get_instance().write(mensaje)
                return True
            else:
                UtilLog.get_instance().write(
                    f"fila_fue_creada numero_fila {str(numero_fila)} - fila no ha sido creada, se procede a crear"
                )
                return False
        else:
            mensaje = f"fila_fue_creada numero_fila {str(numero_fila)}"
            mensaje += f" - error {str(reponse.status_code)} - se intentara crear fila"
            UtilLog.get_instance().write(mensaje)
            return False

    def add_registros_y_adjuntos(self, dato):
        registro = dato["registro"]
        numero_fila = dato["fila"]
        if not self.fila_fue_creada(numero_fila):
            file_pdf_zip = self.get_file_row(numero_fila)
            if len(file_pdf_zip) > 0:
                file_64 = getPdfToBase64(self.path_pdfs + file_pdf_zip)
                datos = self.get_json_datos_registro(registro, numero_fila, file_pdf_zip, file_64)

                # print(f"add_registros_y_adjuntos {datos}")
                # print(f"add_registros_y_adjuntos intento 1 fila ({numero_fila})")
                # Realiza dos intentos de descarga
                if not self.enviar_registro_y_adjunto(datos):
                    # print(f"add_registros_y_adjuntos intento 2 fila ({numero_fila})")
                    if not self.enviar_registro_y_adjunto(datos):
                        UtilLog.get_instance().write(f"No se proceso la fila {numero_fila}")
                        return False
                return True
            else:
                UtilLog.get_instance().write(f"No se encontró registro para la fila {numero_fila}")
                return False
        return False

    def procesar_registros_csv(self):
        i = 0
        for dato in self.lista_registros_csv:
            i = dato["fila"]
            if i > 1 and i >= self.procesar_desde_fila:  # La primera fila son los títulos
                UtilLog.get_instance().write(f"procesar_registros_csv --> add_registros_y_adjuntos fila ({i})")
                self.add_registros_y_adjuntos(dato)

    def get_lista_registros_csv(self):
        print(f"get_lista_registros_csv: {self.file_csv}")
        lista = []
        i = 0
        with open(self.file_csv, encoding="UTF-8") as fname:
            for registro in fname:
                i += 1
                # print(registro)
                dato = {"registro": registro, "fila": i}
                lista.append(dato)
        return lista

    def get_lista_archivos_pdf_zip(self):
        lista = []
        for file in os.listdir(self.path_pdfs):
            if ".pdf" in file.lower() or ".zip" in file.lower():
                # print(file)
                lista.append(str(file))
        return lista

    def procesar_registros_csv_hilos(self):
        # print("procesar_registros_csv __name__ ({__name__})")
        if __name__ == "__main__":
            cores = int(os.cpu_count() / 2 + 1)
            # UtilLog.get_instance().write("Nucleos a utilizar " + str(cores) + "/" + str(os.cpu_count()))
            UtilLog.get_instance().write(f"lista_registros_csv cantidad {str(len(self.lista_registros_csv))}")
            with ProcessPoolExecutor(max_workers=cores) as executor:
                [executor.map(self.add_registros_y_adjuntos, self.lista_registros_csv)]

    def subir_csv(self):
        if int(self.masivo_file_id) > 0:
            UtilLog.get_instance().write(f"subir_csv - numero_ejecucion: {str(self.masivo_file_id)}")
            return True

        UtilLog.get_instance().write("subir_csv - procesando archivo csv")

        secuencia = admin_user.get_instance().get_secuencia("SQ_FILE_API_ID")
        if secuencia == 0:
            UtilLog.get_instance().write("subir_csv - error secuencia - Fin programa")
            return False

        UtilLog.get_instance().write(f"subir_csv - secuencia_file_api {secuencia}")
        UtilLog.get_instance().write(f"subir_csv - file_csv - {self.file_csv}")
        csv_base_64 = getCsvToBase64(self.file_csv)
        # UtilLog.get_instance().write("subir_csv - base 64")

        payload = {
            "username": admin_user.get_instance().username,
            "archivo_name": "cargue_masivo_" + str(secuencia) + ".csv",
            "archivo_csv_64": csv_base_64,
            "tarea":"radicarAcuseSinProceso"
            # "archivo_csv_64": "YXJjaGl2b19jc3ZfNjQ="
        }

        endpoint = admin_user.get_instance().url + "cargar_csv/"
        token = "Token " + admin_user.get_instance().get_token()
        # UtilLog.get_instance().write(f"subir_csv - token {token}")
        # print(f"subir_csv " + "b" * 10)
        # token='Token c3a16a55b7ebdc559c65a0e17c58197dc719061f'
        headers = {"Content-Type": "application/json;", "Authorization": token}
        # reponse=requests.get(endpoint, params={'pk':2})
        # print(f"subir_csv radicacion_id {radicacion_id}")
        reponse = requests.post(endpoint, headers=headers, json=payload)
        print(f"subir_csv reponse.status_code {reponse.status_code}")
        # print(reponse)
        # print(reponse.url)
        json_item = reponse.json()
        UtilLog.get_instance().write(f"subir_csv list_json {json_item}")

        if reponse.status_code == 200:
            # print(f"generar_pdfs nombre_archivo {json_item['nombre_archivo']}")
            UtilLog.get_instance().write(
                f"subir_csv masivo_file {json_item['masivo_file_id']} archivo {json_item['archivo_name']}"
            )
            # UtilLog.get_instance().write(f"subir_csv solicitud_id {radicacion_id} {json_item}")
            if json_item["estado"] == "ok":
                self.masivo_file_id = json_item["masivo_file_id"]
                UtilLog.get_instance().write("-------------------------------------------------------------")
                UtilLog.get_instance().write(
                    f"******** numero ejecucion ({json_item['masivo_file_id']}) *********"
                )
                UtilLog.get_instance().write("-------------------------------------------------------------")
                return True
            else:
                UtilLog.get_instance().write(f"subir_csv solicitud_id json_item {json_item}")
                return False
        else:
            UtilLog.get_instance().write(f"subir_csv list_json json_item {json_item}")
            return False

    def validar_long_registros_archivos(self):
        self.lista_registros_csv = self.get_lista_registros_csv()
        self.lista_archivos_pdf_zip = self.get_lista_archivos_pdf_zip()
        l_registros = len(self.lista_registros_csv) - 1
        l_archivos = len(self.lista_archivos_pdf_zip)

        if l_registros > l_archivos:
            UtilLog.get_instance().write(f"registros csv: {str(l_registros)}")
            UtilLog.get_instance().write(f"cantidad archivos: {str(l_archivos)}")
            UtilLog.get_instance().write("cantidad registros es diferente a la cantidad archivos")
            return False
        return True

    def run(self):
        if self.validar_long_registros_archivos():
            # print("Inicio")
            admin_user.get_instance().autentication()
            admin_user.get_instance().get_token()
            # self.procesar_registros_csv()
            # self.fila_fue_creada(2)

            # Procesa los archivos uno a uno
            if self.subir_csv():
                self.procesar_registros_csv()
                self.generar_resumen()

            """
            if self.subir_csv():
                self.procesar_registros_csv_hilos()
            """

            if self.procesar_desde_fila > 0 or self.masivo_file_id:
                UtilLog.get_instance().write("-------------------------------------------------------------")
                UtilLog.get_instance().write("NO OLVIDE DEJAR EN CERO 0 LOS PARAMETROS: ")
                UtilLog.get_instance().write(" --> numero_ejecucion=0")
                UtilLog.get_instance().write(" --> procesar_desde_fila=0")
            UtilLog.get_instance().write("-------------------------------------------------------------")
            UtilLog.get_instance().write("Para ver resumen desde litiradicaciones")
            UtilLog.get_instance().write("masivos->Cargar archivos masivos->Consultar ultimos cargues")
            UtilLog.get_instance().write(f"*** numero ejecucion: ({self.masivo_file_id}) ***")
            UtilLog.get_instance().write("-------------------------------------------------------------")


acusar_sin_proceso().run()
