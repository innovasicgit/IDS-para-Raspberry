#!/bin/bash
# Script de verificación final - Comprueba que la instalación esté completa
# Ejecutar después de instalar todo

set -e

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "════════════════════════════════════════════════════════"
echo "  ✅ VERIFICACIÓN FINAL - IDS IoT Backend API"
echo "════════════════════════════════════════════════════════"
echo -e "${NC}"

# Contador de checks
total_checks=0
passed_checks=0

check() {
    total_checks=$((total_checks + 1))
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ $1${NC}"
        passed_checks=$((passed_checks + 1))
        return 0
    else
        echo -e "${RED}❌ $1${NC}"
        return 1
    fi
}

echo ""
echo -e "${BLUE}📁 Verificando archivos de código...${NC}"
echo ""

# Verificar archivos principales
[ -f "backend_api.py" ]
check "backend_api.py"

[ -f "app_cloud.py" ]
check "app_cloud.py"

[ -f "requirements_backend.txt" ]
check "requirements_backend.txt"

[ -f "requirements_frontend.txt" ]
check "requirements_frontend.txt"

echo ""
echo -e "${BLUE}📚 Verificando documentación...${NC}"
echo ""

[ -f "RESUMEN_EJECUTIVO.md" ]
check "RESUMEN_EJECUTIVO.md"

[ -f "INICIO_RAPIDO.md" ]
check "INICIO_RAPIDO.md"

[ -f "README_API.md" ]
check "README_API.md"

[ -f "ARQUITECTURA_API.md" ]
check "ARQUITECTURA_API.md"

[ -f "INDEX.md" ]
check "INDEX.md"

[ -f "FLUJO_COMPLETO.md" ]
check "FLUJO_COMPLETO.md"

echo ""
echo -e "${BLUE}🔧 Verificando scripts...${NC}"
echo ""

[ -x "start_backend.sh" ]
check "start_backend.sh (ejecutable)"

[ -x "stop_backend.sh" ]
check "stop_backend.sh (ejecutable)"

[ -x "check_prerequisites.py" ]
check "check_prerequisites.py (ejecutable)"

[ -x "test_backend.py" ]
check "test_backend.py (ejecutable)"

[ -x "generate_report.py" ]
check "generate_report.py (ejecutable)"

echo ""
echo -e "${BLUE}🤖 Verificando modelos ML...${NC}"
echo ""

[ -f "model/iforest__EJERCICIO10_n_components6_fit.pkl" ]
check "IForest model"

[ -f "model/ocsvm__EJERCICIO10_n_components6_fit.pkl" ]
check "OCSVM model"

[ -f "model/kmeans1__EJERCICIO10_n_components6_over.pkl" ]
check "KMEANS model"

[ -f "model/autoencoder.pkl" ]
check "Autoencoder model"

[ -f "model/list_kmeans_over.txt" ]
check "KMEANS dict"

echo ""
echo -e "${BLUE}📦 Verificando módulos backend...${NC}"
echo ""

[ -f "backend/capture_utils.py" ]
check "capture_utils.py"

[ -f "backend/predict.py" ]
check "predict.py"

[ -f "backend/model_utils.py" ]
check "model_utils.py"

[ -f "backend/constants.py" ]
check "constants.py"

echo ""
echo -e "${BLUE}══════════════════════════════════════════${NC}"
echo -e "${BLUE}  RESUMEN DE VERIFICACIÓN${NC}"
echo -e "${BLUE}══════════════════════════════════════════${NC}"
echo ""

percentage=$((passed_checks * 100 / total_checks))

if [ $passed_checks -eq $total_checks ]; then
    echo -e "${GREEN}🎉 ¡PERFECTO! Todos los checks pasaron${NC}"
    echo ""
    echo -e "Total: ${GREEN}$passed_checks/$total_checks${NC} (${GREEN}100%${NC})"
    echo ""
    echo -e "${GREEN}✅ El sistema está completamente instalado y listo${NC}"
    echo ""
    echo -e "${BLUE}Próximos pasos:${NC}"
    echo "  1. Inicia el backend: ${YELLOW}./start_backend.sh${NC}"
    echo "  2. Ejecuta tests: ${YELLOW}python test_backend.py${NC}"
    echo "  3. Lee la documentación: ${YELLOW}cat INDEX.md${NC}"
    echo ""
elif [ $percentage -ge 90 ]; then
    echo -e "${YELLOW}⚠️  Casi perfecto (algunos archivos opcionales faltan)${NC}"
    echo ""
    echo -e "Total: ${YELLOW}$passed_checks/$total_checks${NC} (${YELLOW}$percentage%${NC})"
    echo ""
    echo -e "${YELLOW}El sistema debería funcionar, pero revisa los items faltantes${NC}"
    echo ""
elif [ $percentage -ge 70 ]; then
    echo -e "${YELLOW}⚠️  Instalación incompleta${NC}"
    echo ""
    echo -e "Total: ${YELLOW}$passed_checks/$total_checks${NC} (${YELLOW}$percentage%${NC})"
    echo ""
    echo "Revisa los archivos faltantes arriba y consulta:"
    echo "  • ${YELLOW}INICIO_RAPIDO.md${NC}"
    echo "  • ${YELLOW}ARQUITECTURA_API.md${NC}"
    echo ""
else
    echo -e "${RED}❌ Instalación con problemas críticos${NC}"
    echo ""
    echo -e "Total: ${RED}$passed_checks/$total_checks${NC} (${RED}$percentage%${NC})"
    echo ""
    echo "Muchos archivos faltan. Asegúrate de:"
    echo "  1. Estar en el directorio correcto"
    echo "  2. Haber clonado/descargado todos los archivos"
    echo "  3. Tener permisos de lectura"
    echo ""
fi

echo -e "${BLUE}══════════════════════════════════════════${NC}"
echo ""

# Información adicional
echo -e "${BLUE}ℹ️  Información adicional:${NC}"
echo ""
echo "  Directorio actual: $(pwd)"
echo "  Usuario: $USER"
echo "  Fecha: $(date)"
echo ""

# Sugerencias
if [ $passed_checks -eq $total_checks ]; then
    echo -e "${GREEN}📖 Documentación recomendada:${NC}"
    echo "  • Para empezar: ${YELLOW}less INICIO_RAPIDO.md${NC}"
    echo "  • Para profundizar: ${YELLOW}less ARQUITECTURA_API.md${NC}"
    echo "  • Índice completo: ${YELLOW}less INDEX.md${NC}"
    echo ""
fi

exit 0
