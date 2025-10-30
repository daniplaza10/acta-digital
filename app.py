import streamlit as st
import hashlib, time, json, secrets

# --- Función de hash ---
def get_hash(text):
    return hashlib.sha256(text.encode()).hexdigest()

# --- Interfaz principal ---
st.title("Registro de Documentos Digitales")

owner = st.text_input("Propietario")
content = st.text_area("Contenido del documento")

# --- Registro del documento ---
if st.button("Registrar"):
    if not owner or not content:
        st.warning("Completa todos los campos antes de registrar.")
    else:
        record = {"owner": owner, "hash": get_hash(content), "time": time.time()}
        with open("blockchain.json", "a") as f:
            f.write(json.dumps(record) + "\n")
        st.success("Documento registrado con éxito ✅")

# --- Verificación de integridad ---
def verify(content):
    h = get_hash(content)
    try:
        with open("blockchain.json") as f:
            for line in f:
                r = json.loads(line)
                if r["hash"] == h:
                    return True
    except FileNotFoundError:
        return False
    return False

if st.button("Verificar"):
    if verify(content):
        st.success("✅ El documento ya estaba registrado.")
    else:
        st.error("❌ No se encontró este documento en el registro.")

# --- Generación de claves (firma digital) ---
st.header("Firma digital")
private_key = secrets.token_hex(16)
public_key = get_hash(private_key)

st.write("Tu clave pública:", public_key)
st.info("La clave pública identifica al usuario; la privada le da poder para firmar.")

# --- Sistema de votación ---
st.header("Votación de validez")
doc_hash = st.text_input("Hash del documento a votar")
vote = st.radio("¿Es válido?", ["Sí", "No"])

if st.button("Votar"):
    if not doc_hash:
        st.warning("Introduce el hash del documento antes de votar.")
    else:
        with open("votes.json", "a") as f:
            f.write(json.dumps({"hash": doc_hash, "vote": vote}) + "\n")
        st.success("Voto registrado 🗳️")

# --- Resultado de la votación ---
def count_votes():
    yes, no = 0, 0
    try:
        with open("votes.json") as f:
            for line in f:
                v = json.loads(line)
                if v["vote"] == "Sí":
                    yes += 1
                else:
                    no += 1
    except FileNotFoundError:
        pass
    return yes, no

if st.button("Ver resultado"):
    y, n = count_votes()
    st.write(f"Sí: {y} | No: {n}")
    st.caption("El código ejecuta la decisión, pero no analiza si es justa: la justicia digital requiere interpretación humana.")
