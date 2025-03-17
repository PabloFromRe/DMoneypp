import streamlit as st
import requests

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

# Function to get the currency conversion and exchange rate with commission
def convertir_moneda(desde, hacia, cantidad):
    url = f"https://api.exchangerate-api.com/v4/latest/{desde}"  # Replace with your API URL
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        tasa_conversion = data['rates'].get(hacia)
        
        if tasa_conversion:
            # Calcular la conversión sin la comisión
            conversion_sin_comision = cantidad * tasa_conversion
            
            # Calcular la comisión (3%)
            comision = conversion_sin_comision * 0.03
            
            # Calcular el total con la comisión incluida
            total_con_comision = conversion_sin_comision + comision
            
            return conversion_sin_comision, comision, total_con_comision
        else:
            return "Moneda no disponible", None, None
    else:
        return "Error al conectar con la API", None, None

# Streamlit app layout
st.title("Convertidor de Moneda")
st.write("Este convertidor de moneda utiliza una API para hacer las conversiones.")

# Input fields
moneda_desde = st.selectbox("Selecciona la moneda de origen", monedas)
cantidad = st.number_input("Ingresa la cantidad que deseas convertir", min_value=1, value=100)
moneda_hacia = st.selectbox("Selecciona la moneda de destino", monedas)

# Conversion result
if st.button("Convertir"):
    conversion_sin_comision, comision, total_con_comision = convertir_moneda(moneda_desde, moneda_hacia, cantidad)
    
    if isinstance(conversion_sin_comision, float):
        st.write(f"El valor de la conversión sin comisión es: {conversion_sin_comision:.2f} {moneda_hacia}")
        st.write(f"Comisión del 3%: {comision:.2f} {moneda_hacia}")
        st.write(f"El total con la comisión incluida es: {total_con_comision:.2f} {moneda_hacia}")
    else:
        st.write(conversion_sin_comision)
