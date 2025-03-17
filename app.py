import streamlit as st
import requests
import math

# Lista de monedas disponibles
monedas = [
    'USD', 'AED', 'AFN', 'ALL', 'AMD', 'ANG', 'AOA', 'ARS', 'AUD', 'AWG', 'AZN', 
    'BAM', 'BBD', 'BDT', 'BGN', 'BHD', 'BIF', 'BMD', 'BND', 'BOB', 'BRL', 'BSD', 
    'BTN', 'BWP', 'BYN', 'BZD', 'CAD', 'CDF', 'CHF', 'CLP', 'CNY', 'COP', 'CRC', 
    'CUP', 'CVE', 'CZK', 'DJF', 'DKK', 'DOP', 'DZD', 'EGP', 'ERN', 'ETB', 'EUR', 
    'FJD', 'FKP', 'FOK', 'GBP', 'GEL', 'GGP', 'GHS', 'GIP', 'GMD', 'GNF', 'GTQ', 
    'GYD', 'HKD', 'HNL', 'HRK', 'HTG', 'HUF', 'IDR', 'ILS', 'IMP', 'INR', 'IQD', 
    'IRR', 'ISK', 'JEP', 'JMD', 'JOD', 'JPY', 'KES', 'KGS', 'KHR', 'KID', 'KMF', 
    'KRW', 'KWD', 'KYD', 'KZT', 'LAK', 'LBP', 'LKR', 'LRD', 'LSL', 'LYD', 'MAD', 
    'MDL', 'MGA', 'MKD', 'MMK', 'MNT', 'MOP', 'MRU', 'MUR', 'MVR', 'MWK', 'MXN', 
    'MYR', 'MZN', 'NAD', 'NGN', 'NIO', 'NOK', 'NPR', 'NZD', 'OMR', 'PAB', 'PEN', 
    'PGK', 'PHP', 'PKR', 'PLN', 'PYG', 'QAR', 'RON', 'RSD', 'RUB', 'RWF', 'SAR', 
    'SBD', 'SCR', 'SDG', 'SEK', 'SGD', 'SHP', 'SLE', 'SLL', 'SOS', 'SRD', 'SSP', 
    'STN', 'SYP', 'SZL', 'THB', 'TJS', 'TMT', 'TND', 'TOP', 'TRY', 'TTD', 'TVD', 
    'TWD', 'TZS', 'UAH', 'UGX', 'UYU', 'UZS', 'VES', 'VND', 'VUV', 'WST', 'XAF', 
    'XCD', 'XDR', 'XOF', 'XPF', 'YER', 'ZAR', 'ZMW', 'ZWL'
]

# Function to get the currency conversion and apply commission
def convertir_moneda(desde, hacia, cantidad):
    url = f"https://api.exchangerate-api.com/v4/latest/{desde}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        tasa_conversion = data['rates'].get(hacia)
        tasa_euro = data['rates'].get('EUR')  # Tasa de cambio para convertir 1 EUR a la moneda de origen
        
        # Si la moneda de origen es USD, la comisión es de 4 USD
        if desde == 'USD':
            comision = 4  # Comisión fija en USD
        else:
            if tasa_euro:
                # Invertir la tasa de EUR a la moneda de origen
                tasa_euro_a_origen = (1 / tasa_euro)  # Obtener cuántos de la moneda de origen equivale 1 EUR

                # Convertir la comisión fija de 4 EUR a la moneda de origen
                comision = 4.05 * tasa_euro_a_origen  # Comisión convertida a la moneda de origen
            else:
                return "Error con la tasa de cambio de EUR", None, None

        if tasa_conversion:
            # Calcular el total que se debe enviar incluyendo la comisión
            total_a_enviar = cantidad + comision
            
            # La persona recibe la cantidad enviada, no el total con comisión
            cantidad_recibida = cantidad * tasa_conversion 
            
            return cantidad_recibida, comision, total_a_enviar
        else:
            return "Moneda no disponible", None, None
    else:
        return "Error al conectar con la API", None, None

# Streamlit app layout
st.title("Convertidor de Moneda")
st.write("Selecciona la moneda de origen, ingresa la cantidad y elige la moneda de destino, luego presiona *Convertir*. \n"
"Verás el precio de envío (comisión), precio total a enviar y cuánto recibirás en la moneda elegida.")

# Input fields
st.write("Elige la moneda desde la que harás el cambio")
moneda_desde = st.selectbox("Selecciona la moneda de origen", monedas)
cantidad = st.number_input("Ingresa la cantidad que deseas convertir", min_value=1, value=100)
st.write("Elige la moneda que querrás obtener")
moneda_hacia = st.selectbox("Selecciona la moneda de destino", monedas)

# Conversion result
if st.button("Convertir"):
    cantidad_recibida, comision, total_a_enviar = convertir_moneda(moneda_desde, moneda_hacia, cantidad)
    
    if isinstance(cantidad_recibida, float):
        st.write(f"Precio de envío: {comision:.2f} {moneda_desde}")
        st.write(f"En total deberás enviar: {total_a_enviar:.2f} {moneda_desde}")
        st.write(f"Recibirás: {cantidad_recibida:.2f} {moneda_hacia}")
    else:
        st.write(cantidad_recibida)
