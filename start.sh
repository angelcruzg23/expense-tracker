#!/bin/bash

# Script para iniciar el Expense Tracker

echo "🚀 Iniciando Expense Tracker..."
echo ""

# Verificar que las dependencias estén instaladas
if ! python -c "import fastapi" 2>/dev/null; then
    echo "📦 Instalando dependencias..."
    pip install -r requirements.txt
fi

echo "✅ Dependencias instaladas"
echo ""
echo "🌐 Iniciando servidor..."
echo "   Aplicación Web: http://localhost:8000"
echo "   API: http://localhost:8000/api"
echo "   Documentación: http://localhost:8000/docs"
echo ""
echo "Presiona Ctrl+C para detener el servidor"
echo ""

python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
