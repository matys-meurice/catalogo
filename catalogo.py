import streamlit as st
from supabase import create_client

st.markdown("""
<style>
button {
    background-color: #ff6600 !important;
    color: white !important;
    border-radius: 10px !important;
}
.card {
    background-color: #f5f5f5;
    padding: 15px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.card:hover {
    transform: scale(1.05);
    box-shadow: 0 8px 20px rgba(0,0,0,0.2);
}
</style>
""", unsafe_allow_html=True)

# -------- CONFIG SUPABASE --------
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

# -------- ESTADO --------
if "producto" not in st.session_state:
    st.session_state.producto = None

# -------- PRODUCTOS --------
productos = [
    {"nombre": "Fidget spin piramide pequeña", "tipo": "piramide", "precio": 0.30, "img": "imagenes/1.png"},
    {"nombre": "Fidget spin piramide", "tipo": "piramide", "precio": 1, "img": "imagenes/2.png"},
    {"nombre": "Llavero personalizado", "tipo": "personalizado", "precio": "1-5", "img": "imagenes/3.png"},
    {"nombre": "Carteles personalizados", "tipo": "personalizado", "precio": "variable", "img": "imagenes/4.png"},
    {"nombre": "Figuras", "tipo": "personalizado", "precio": "variable", "img": "imagenes/5.png"},
    {"nombre": "Vaciabolsillos 1", "tipo": "normal", "precio": 9, "img": "imagenes/6.png"},
    {"nombre": "Vaciabolsillos 2", "tipo": "normal", "precio": 4, "img": "imagenes/7.png"},
    {"nombre": "Silbato turbo", "tipo": "normal", "precio": 0.5, "img": "imagenes/8.png"},
    {"nombre": "Silbato fuerte", "tipo": "normal", "precio": 0.4, "img": "imagenes/9.png"},
]

# -------- CATÁLOGO --------
def catalogo():
    st.markdown("<h1 style='text-align: center;'> Imprint - Catálogo</h1>", unsafe_allow_html=True)

    cols = st.columns(3)

    for i, p in enumerate(productos):
        with cols[i % 3]:

            st.markdown('<div class="card">', unsafe_allow_html=True)

            st.image(p["img"], use_container_width=True)

            st.markdown(f"### {p['nombre']}")
            st.markdown(f"**€ {p['precio']}**")

            if st.button("Comprar", key=p["nombre"]):
                st.session_state.producto = p

            st.markdown('</div>', unsafe_allow_html=True)

# -------- FORMULARIO --------
def formulario():
    p = st.session_state.producto

    st.title("Pedido")
    st.subheader(p["nombre"])

    datos = {
        "producto": p["nombre"]
    }

    #  PIRÁMIDES
    if p["tipo"] == "piramide":
        color_fuera = st.selectbox("Color exterior", ["Rojo", "Azul", "Verde", "Negro"])
        color_dentro = st.selectbox("Color interior", ["Rojo", "Azul", "Verde", "Negro"])

        datos["color_fuera"] = color_fuera
        datos["color_dentro"] = color_dentro

    #  PERSONALIZADOS
    elif p["tipo"] == "personalizado":
        descripcion = st.text_area("¿Cómo lo quieres?")
        datos["descripcion"] = descripcion

    #  NORMALES
    else:
        color = st.selectbox("Color", ["Rojo", "Azul", "Verde", "Negro"])
        datos["color"] = color

    #  EXTRA PARA TODOS
    extra = st.text_area("Especificaciones extra (opcional)")
    datos["extra"] = extra

    nombre = st.text_input("Tu nombre")
    datos["cliente"] = nombre

    if st.button("Enviar pedido"):
        supabase.table("pedidos").insert(datos).execute()
        st.success("Pedido enviado 🚀")
        st.session_state.producto = None

    if st.button("Volver"):
        st.session_state.producto = None

# -------- CONTROL --------
if st.session_state.producto is None:
    catalogo()
else:
    formulario()