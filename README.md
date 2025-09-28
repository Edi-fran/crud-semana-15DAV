# CRUD Flask + MySQL (Productos)

Proyecto de ejemplo para la asignatura: **CRUD** de `productos` usando **Flask** y **MySQL**.

## 1) Requisitos
- Python 3.10+
- MySQL 8.x o MariaDB 10.x
- Visual Studio Code o PyCharm (opcional)
- `pip`

## 2) Instalación
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

pip install -r requirements.txt
```

Copia `.env.example` como `.env` y edita las credenciales de MySQL:
```
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=tu_password
MYSQL_DB=desarrollo_web
```

## 3) Base de datos
Ejecuta el script:
```sql
source create_db.sql;
```
O copia y pega su contenido en tu cliente MySQL.

## 4) Ejecutar
```bash
python app.py
```
Abrir: http://127.0.0.1:5000/

## 5) Rutas
- `GET /productos` → Listado
- `GET|POST /crear` → Crear producto
- `GET|POST /editar/<id>` → Editar
- `GET|POST /eliminar/<id>` → Confirmar y eliminar

## 6) Estructura
```
flask_mysql_crud_productos/
├── app.py
├── create_db.sql
├── requirements.txt
├── .env.example
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── form.html
│   └── confirm_delete.html
└── static/
    └── styles.css
```

## 7) Subir a GitHub
```bash
git init
git add .
git commit -m "CRUD Flask + MySQL (productos)"
git branch -M main
git remote add origin https://github.com/USUARIO/REPO.git
git push -u origin main
```

> Incluye `create_db.sql` en el repo como pide la rúbrica.