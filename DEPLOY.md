# 🚀 Guía de Despliegue en Render

## 📋 Prerequisitos

- Cuenta en [Render.com](https://render.com)
- Repositorio en GitHub con el código del proyecto

---

## 🔧 Configuración del Proyecto

### 1. Preparar el Repositorio

El proyecto ya está configurado con los archivos necesarios:
- ✅ `requirements.txt` - Dependencias de Python
- ✅ `render.yaml` - Configuración de Render
- ✅ `frontend/static/js/app.js` - Configurado para usar `window.location.origin`

### 2. Variables de Entorno (Opcional)

Si necesitas configurar variables de entorno específicas, puedes agregarlas en Render:
- `PYTHON_VERSION`: 3.11.0 (ya configurado)
- `PORT`: Lo asigna automáticamente Render

---

## 📦 Despliegue en Render

### Opción A: Despliegue Automático con Blueprint (Recomendado)

1. **Conectar tu repositorio GitHub con Render**
   - Ve a [Render Dashboard](https://dashboard.render.com/)
   - Click en "New +" → "Blueprint"
   - Conecta tu cuenta de GitHub si aún no lo has hecho
   - Selecciona el repositorio `expense-tracker`
   - Render detectará automáticamente el archivo `render.yaml`
   - Click en "Apply" para crear el servicio

2. **Esperar el despliegue**
   - Render instalará las dependencias
   - Iniciará el servidor con uvicorn
   - Te proporcionará una URL como: `https://expense-tracker-xxxx.onrender.com`

### Opción B: Despliegue Manual

1. **Crear un nuevo Web Service**
   - Ve a [Render Dashboard](https://dashboard.render.com/)
   - Click en "New +" → "Web Service"
   - Conecta tu repositorio de GitHub

2. **Configurar el servicio**
   - **Name**: `expense-tracker` (o el nombre que prefieras)
   - **Environment**: `Python 3`
   - **Region**: Selecciona la más cercana a tu ubicación
   - **Branch**: `main` (o `master` según tu repo)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`

3. **Variables de Entorno**
   - Añade: `PYTHON_VERSION` = `3.11.0`

4. **Plan**
   - Selecciona "Free" si quieres el plan gratuito
   - ⚠️ **Nota**: El plan gratuito se duerme después de 15 minutos de inactividad

5. **Crear el Web Service**
   - Click en "Create Web Service"
   - Espera a que termine el despliegue (puede tomar 5-10 minutos)

---

## 🔄 Actualizar la Aplicación

### Desde Git (Automático)

Render se actualizará automáticamente cuando hagas push a tu rama principal:

```bash
git add .
git commit -m "Update: descripción de los cambios"
git push origin main
```

Render detectará el cambio y redesplegaráautomáticamente.

### Manual desde Render Dashboard

1. Ve a tu servicio en [Render Dashboard](https://dashboard.render.com/)
2. Click en "Manual Deploy" → "Deploy latest commit"
3. Espera a que termine el redespliegue

---

## 🧪 Verificar el Despliegue

Una vez desplegado, verifica que todo funcione:

1. **Abrir la URL de tu aplicación**
   - Ejemplo: `https://expense-tracker-r2r2.onrender.com/`

2. **Verificar la API**
   - Abre la consola del navegador (F12)
   - Deberías ver logs como:
     ```
     🔧 API URL configurada: https://expense-tracker-r2r2.onrender.com
     📍 Location: {...}
     ```

3. **Probar funcionalidades**
   - Crear categorías
   - Registrar gastos
   - Ver resumen
   - Probar desde móvil

---

## ⚠️ Solución de Problemas Comunes

### Error: "Error al cargar las categorías"

**Causa**: Problema de CORS o la base de datos no se inicializó

**Solución**:
1. Verifica los logs en Render Dashboard
2. Asegúrate de que el servidor inició correctamente
3. Revisa la consola del navegador para ver el error exacto

### La aplicación se tarda mucho en cargar

**Causa**: Plan gratuito de Render se duerme después de 15 minutos

**Solución**:
- Espera 30-60 segundos la primera vez que accedes
- Considera actualizar a un plan de pago si necesitas tiempo de respuesta constante

### Error 502 Bad Gateway

**Causa**: El servidor no respondió a tiempo

**Solución**:
1. Verifica que el comando de inicio sea correcto
2. Revisa los logs en Render para ver errores
3. Asegúrate de que uvicorn esté usando `--host 0.0.0.0 --port $PORT`

### No funciona en móvil pero sí en desktop

**Causa**: La URL de la API no se está detectando correctamente

**Solución**:
1. Abre la consola del navegador en móvil (usa Remote Debugging)
2. Verifica que `window.location.origin` sea correcto
3. Asegúrate de estar usando HTTPS (no HTTP)

---

## 📱 Probar desde Móvil

### iPhone/iPad
1. Abre Safari o Chrome
2. Ve a tu URL de Render
3. Abre las Developer Tools (si está disponible)
4. Verifica la consola para errores

### Android
1. Abre Chrome
2. Ve a tu URL de Render
3. Accede a las Developer Tools desde Chrome en desktop:
   - Conecta tu teléfono por USB
   - Abre `chrome://inspect` en Chrome desktop
   - Selecciona tu dispositivo

---

## 🔐 Seguridad

Para producción, considera:

1. **Configurar CORS específico** (en lugar de `"*"`):
   ```python
   allow_origins=[
       "https://tu-dominio.com",
       "https://expense-tracker-r2r2.onrender.com"
   ]
   ```

2. **Agregar autenticación** si la aplicación contiene datos sensibles

3. **Usar variables de entorno** para configuraciones sensibles

---

## 📊 Monitoreo

Render proporciona:
- **Logs en tiempo real**: Ver errores y requests
- **Métricas**: CPU, memoria, requests
- **Health checks**: Verificar que la app esté funcionando

Accede a todo esto desde tu [Render Dashboard](https://dashboard.render.com/).

---

## 🎉 ¡Listo!

Tu aplicación de Control de Gastos ya está desplegada y accesible desde cualquier dispositivo con conexión a internet.

**URL de ejemplo**: https://expense-tracker-r2r2.onrender.com/

---

## 📞 Soporte

Si encuentras problemas:
1. Revisa los logs en Render Dashboard
2. Verifica la consola del navegador
3. Asegúrate de que todos los archivos estén en GitHub
4. Verifica que el `render.yaml` esté en la raíz del proyecto
