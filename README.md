Langkah-langkah untuk menjalankan aplikasi ini:
1. Install software requirements:
> `pip install -r requirements.txt`
2. Ubah konfigurasi database dan buat database di mysql dengan nama yang sama:
```javascript
DATABASE_CONFIG = {
    'host': 'localhost',
    'dbname': 'backend_test',
    'user': 'root',
    'password': 'secret',
    'port': 3306
}
```
3. Kemudian buat table dengan perintah:
> `flask db upgrade`
4. Dan buat data dummy user:
> `flask seed`
