from sqlalchemy import create_engine

try:
    engine = create_engine('postgresql+psycopg2://alex:123@localhost:5432/granja')
    with engine.connect() as conn:
        print("✅ Conexión exitosa")
except Exception as e:
    print("❌ Error de conexión:", e)
