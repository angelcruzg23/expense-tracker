// Detectar automáticamente la URL de la API
const API_URL = window.location.origin;

// Log de debug para verificar la URL en consola
console.log('🔧 API URL configurada:', API_URL);
console.log('📍 Location:', {
    origin: window.location.origin,
    hostname: window.location.hostname,
    protocol: window.location.protocol
});

function expenseTracker() {
    return {
        // Estado
        gastos: [],
        categorias: [],
        subcategorias: [],
        resumen: { categorias: [], totales: {} },
        bancos: [],
        mediosPago: [],
        cuentasBancarias: [],
        ingresos: [],

        // Formulario
        nuevoGasto: {
            fecha: new Date().toISOString().split('T')[0],
            monto: '',
            descripcion: '',
            categoria_id: '',
            subcategoria_id: null,
            banco_id: null,
            medio_pago_id: null
        },

        // UI
        mostrarTodos: false,
        modalPresupuesto: false,
        modalPresupuestos: false,
        modalGrafico: false,
        modalCategorias: false,
        modalNuevaCategoria: false,
        modalBancos: false,
        modalMediosPago: false,
        modalCuentasBancarias: false,
        modalNuevaCuenta: false,
        modalIngresos: false,
        tablaPresupuestoExpandida: true,
        mostrarTodosIngresos: false,
        categoriaEditar: null,
        nuevoPresupuesto: 0,
        presupuestosTemporales: {},
        nuevaCategoria: {
            nombre: '',
            icono: '💰',
            color: '#3B82F6',
            presupuesto_mensual: 0
        },
        nuevoBanco: {
            nombre: ''
        },
        nuevoMedioPago: {
            tipo: '',
            nombre: '',
            banco_id: ''
        },
        nuevaCuenta: {
            nombre: '',
            banco_id: '',
            saldo_transaccional: 0,
            saldo_ahorros: 0,
            tipo_cuenta: 'Ahorro'
        },
        nuevoIngreso: {
            fecha: new Date().toISOString().split('T')[0],
            monto: '',
            descripcion: '',
            categoria_ingreso: 'Salario',
            cuenta_bancaria_id: ''
        },

        // Filtros
        mesSeleccionado: new Date().getMonth() + 1,
        anioSeleccionado: new Date().getFullYear(),

        // Chart
        chart: null,

        // Inicialización
        async init() {
            await Promise.all([
                this.cargarCategorias(),
                this.cargarBancos(),
                this.cargarMediosPago(),
                this.cargarCuentasBancarias(),
                this.cargarIngresos()
            ]);
            await this.cargarDatos();

            // Observar cambios en modalGrafico para actualizar el gráfico
            this.$watch('modalGrafico', (value) => {
                if (value) {
                    // Esperar a que el DOM se actualice
                    setTimeout(() => this.actualizarGrafico(), 100);
                }
            });
        },

        // Cargar datos
        async cargarCategorias() {
            try {
                const response = await fetch(`${API_URL}/categorias`);
                this.categorias = await response.json();
            } catch (error) {
                console.error('Error cargando categorías:', error);
                alert('Error al cargar las categorías');
            }
        },

        async cargarSubcategorias() {
            if (!this.nuevoGasto.categoria_id) {
                this.subcategorias = [];
                return;
            }

            try {
                const response = await fetch(`${API_URL}/subcategorias?categoria_id=${this.nuevoGasto.categoria_id}`);
                this.subcategorias = await response.json();
            } catch (error) {
                console.error('Error cargando subcategorías:', error);
            }
        },

        async cargarDatos() {
            await Promise.all([
                this.cargarGastos(),
                this.cargarResumen()
            ]);
            // Solo actualizar gráfico si el modal está abierto
            if (this.modalGrafico) {
                this.$nextTick(() => this.actualizarGrafico());
            }
        },

        async cargarGastos() {
            try {
                const response = await fetch(
                    `${API_URL}/gastos?mes=${this.mesSeleccionado}&anio=${this.anioSeleccionado}&limit=100`
                );
                this.gastos = await response.json();
            } catch (error) {
                console.error('Error cargando gastos:', error);
            }
        },

        async cargarResumen() {
            try {
                const response = await fetch(
                    `${API_URL}/resumen?mes=${this.mesSeleccionado}&anio=${this.anioSeleccionado}`
                );
                this.resumen = await response.json();
            } catch (error) {
                console.error('Error cargando resumen:', error);
            }
        },

        // CRUD Gastos
        async crearGasto() {
            try {
                const payload = {
                    ...this.nuevoGasto,
                    monto: parseFloat(this.nuevoGasto.monto),
                    categoria_id: parseInt(this.nuevoGasto.categoria_id),
                    subcategoria_id: this.nuevoGasto.subcategoria_id ? parseInt(this.nuevoGasto.subcategoria_id) : null,
                    banco_id: this.nuevoGasto.banco_id ? parseInt(this.nuevoGasto.banco_id) : null,
                    medio_pago_id: this.nuevoGasto.medio_pago_id ? parseInt(this.nuevoGasto.medio_pago_id) : null
                };

                const response = await fetch(`${API_URL}/gastos`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });

                if (response.ok) {
                    // Resetear formulario
                    this.nuevoGasto = {
                        fecha: new Date().toISOString().split('T')[0],
                        monto: '',
                        descripcion: '',
                        categoria_id: '',
                        subcategoria_id: null,
                        banco_id: null,
                        medio_pago_id: null
                    };
                    this.subcategorias = [];

                    // Recargar datos
                    await this.cargarDatos();

                    alert('Gasto registrado exitosamente');
                } else {
                    const error = await response.json();
                    alert('Error al registrar gasto: ' + (error.detail || 'Error desconocido'));
                }
            } catch (error) {
                console.error('Error creando gasto:', error);
                alert('Error al registrar el gasto');
            }
        },

        async eliminarGasto(id) {
            if (!confirm('¿Estás seguro de eliminar este gasto?')) return;

            try {
                const response = await fetch(`${API_URL}/gastos/${id}`, {
                    method: 'DELETE'
                });

                if (response.ok) {
                    await this.cargarDatos();
                    alert('Gasto eliminado exitosamente');
                } else {
                    alert('Error al eliminar el gasto');
                }
            } catch (error) {
                console.error('Error eliminando gasto:', error);
                alert('Error al eliminar el gasto');
            }
        },

        // Editar presupuesto
        editarPresupuesto(categoria) {
            const cat = this.categorias.find(c => c.nombre === categoria.categoria);
            if (cat) {
                this.categoriaEditar = {
                    ...categoria,
                    id: cat.id
                };
                this.nuevoPresupuesto = categoria.presupuesto_mensual;
                this.modalPresupuesto = true;
            }
        },

        async actualizarPresupuesto() {
            try {
                const response = await fetch(`${API_URL}/categorias/${this.categoriaEditar.id}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        presupuesto_mensual: parseFloat(this.nuevoPresupuesto)
                    })
                });

                if (response.ok) {
                    this.modalPresupuesto = false;
                    await this.cargarCategorias();
                    await this.cargarResumen();
                    alert('Presupuesto actualizado exitosamente');
                } else {
                    alert('Error al actualizar el presupuesto');
                }
            } catch (error) {
                console.error('Error actualizando presupuesto:', error);
                alert('Error al actualizar el presupuesto');
            }
        },

        // Configurar presupuestos (múltiples)
        abrirModalPresupuestos() {
            // Cargar presupuestos actuales en el objeto temporal
            this.presupuestosTemporales = {};
            this.categorias.forEach(cat => {
                this.presupuestosTemporales[cat.id] = cat.presupuesto_mensual;
            });
            this.modalPresupuestos = true;
        },

        calcularPresupuestoTotal() {
            return Object.values(this.presupuestosTemporales)
                .reduce((sum, val) => sum + (parseFloat(val) || 0), 0);
        },

        async guardarTodosPresupuestos() {
            try {
                // Actualizar todas las categorías en paralelo
                const promises = this.categorias.map(cat => {
                    const presupuesto = parseFloat(this.presupuestosTemporales[cat.id]) || 0;
                    return fetch(`${API_URL}/categorias/${cat.id}`, {
                        method: 'PUT',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            presupuesto_mensual: presupuesto
                        })
                    });
                });

                const responses = await Promise.all(promises);
                const todosOk = responses.every(r => r.ok);

                if (todosOk) {
                    this.modalPresupuestos = false;
                    await this.cargarCategorias();
                    await this.cargarResumen();
                    alert('Presupuestos actualizados exitosamente');
                } else {
                    alert('Error al actualizar algunos presupuestos');
                }
            } catch (error) {
                console.error('Error guardando presupuestos:', error);
                alert('Error al guardar los presupuestos');
            }
        },

        // Configurar categorías
        abrirModalCategorias() {
            this.modalCategorias = true;
        },

        iniciarNuevaCategoria() {
            this.nuevaCategoria = {
                nombre: '',
                icono: '💰',
                color: '#3B82F6',
                presupuesto_mensual: 0
            };
            this.modalNuevaCategoria = true;
        },

        async crearNuevaCategoria() {
            try {
                const response = await fetch(`${API_URL}/categorias`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        nombre: this.nuevaCategoria.nombre,
                        icono: this.nuevaCategoria.icono || '💰',
                        color: this.nuevaCategoria.color,
                        presupuesto_mensual: parseFloat(this.nuevaCategoria.presupuesto_mensual) || 0
                    })
                });

                if (response.ok) {
                    this.modalNuevaCategoria = false;
                    await this.cargarCategorias();
                    await this.cargarResumen();
                    alert('Categoría creada exitosamente');
                } else {
                    const error = await response.json();
                    alert('Error al crear categoría: ' + (error.detail || 'Error desconocido'));
                }
            } catch (error) {
                console.error('Error creando categoría:', error);
                alert('Error al crear la categoría');
            }
        },

        async actualizarCategoriaDirecta(categoriaId, campo, valor) {
            try {
                const response = await fetch(`${API_URL}/categorias/${categoriaId}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        [campo]: valor
                    })
                });

                if (response.ok) {
                    await this.cargarCategorias();
                    await this.cargarResumen();
                } else {
                    alert('Error al actualizar la categoría');
                }
            } catch (error) {
                console.error('Error actualizando categoría:', error);
                alert('Error al actualizar la categoría');
            }
        },

        async eliminarCategoria(categoriaId, nombre) {
            if (!confirm(`¿Estás seguro de eliminar la categoría "${nombre}"?\n\nEsto también eliminará todos los gastos asociados.`)) {
                return;
            }

            try {
                const response = await fetch(`${API_URL}/categorias/${categoriaId}`, {
                    method: 'DELETE'
                });

                if (response.ok) {
                    await this.cargarCategorias();
                    await this.cargarResumen();
                    alert('Categoría eliminada exitosamente');
                } else {
                    alert('Error al eliminar la categoría');
                }
            } catch (error) {
                console.error('Error eliminando categoría:', error);
                alert('Error al eliminar la categoría');
            }
        },

        // Gráfico y Modal
        actualizarGrafico() {
            const ctx = document.getElementById('categoryChart');
            if (!ctx) return;

            const data = this.resumen.categorias || [];
            const labels = data.map(c => c.categoria);
            const gastados = data.map(c => c.total_gastado);
            const presupuestos = data.map(c => c.presupuesto_mensual);
            const colores = data.map(c => c.color);

            // Destruir gráfico existente si hay uno
            if (this.chart) {
                this.chart.destroy();
                this.chart = null;
            }

            // Crear nuevo gráfico
            this.chart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: 'Gastado',
                            data: gastados,
                            backgroundColor: colores.map(c => c + 'CC'),
                            borderColor: colores,
                            borderWidth: 1
                        },
                        {
                            label: 'Presupuesto',
                            data: presupuestos,
                            backgroundColor: 'rgba(209, 213, 219, 0.5)',
                            borderColor: 'rgba(156, 163, 175, 1)',
                            borderWidth: 1,
                            borderDash: [5, 5]
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                callback: function(value) {
                                    return '$' + value.toFixed(2);
                                }
                            }
                        }
                    },
                    plugins: {
                        legend: {
                            display: true,
                            position: 'top'
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    return context.dataset.label + ': $' + context.parsed.y.toFixed(2);
                                }
                            }
                        }
                    }
                }
            });
        },

        cerrarModalGrafico() {
            this.modalGrafico = false;
            // Destruir el gráfico al cerrar el modal para liberar memoria
            if (this.chart) {
                this.chart.destroy();
                this.chart = null;
            }
        },

        // Utilidades
        formatCurrency(value) {
            return new Intl.NumberFormat('es-MX', {
                style: 'currency',
                currency: 'MXN'
            }).format(value || 0);
        },

        formatDate(dateString) {
            const date = new Date(dateString + 'T00:00:00');
            return date.toLocaleDateString('es-MX', {
                year: 'numeric',
                month: 'short',
                day: 'numeric'
            });
        },

        // Bancos
        async cargarBancos() {
            try {
                const response = await fetch(`${API_URL}/bancos`);
                this.bancos = await response.json();
            } catch (error) {
                console.error('Error cargando bancos:', error);
            }
        },

        async crearBanco() {
            try {
                const response = await fetch(`${API_URL}/bancos`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ nombre: this.nuevoBanco.nombre })
                });

                if (response.ok) {
                    this.nuevoBanco.nombre = '';
                    await this.cargarBancos();
                    alert('Banco creado exitosamente');
                } else {
                    alert('Error al crear banco');
                }
            } catch (error) {
                console.error('Error creando banco:', error);
                alert('Error al crear banco');
            }
        },

        async eliminarBanco(bancoId, nombre) {
            if (!confirm(`¿Eliminar el banco "${nombre}"?`)) return;

            try {
                const response = await fetch(`${API_URL}/bancos/${bancoId}`, {
                    method: 'DELETE'
                });

                if (response.ok) {
                    await this.cargarBancos();
                    await this.cargarMediosPago();
                    alert('Banco eliminado');
                } else {
                    alert('Error al eliminar banco');
                }
            } catch (error) {
                console.error('Error eliminando banco:', error);
                alert('Error al eliminar banco');
            }
        },

        // Medios de Pago
        async cargarMediosPago() {
            try {
                const response = await fetch(`${API_URL}/medios-pago`);
                this.mediosPago = await response.json();
            } catch (error) {
                console.error('Error cargando medios de pago:', error);
            }
        },

        async crearMedioPago() {
            try {
                const response = await fetch(`${API_URL}/medios-pago`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        tipo: this.nuevoMedioPago.tipo,
                        nombre: this.nuevoMedioPago.nombre,
                        banco_id: parseInt(this.nuevoMedioPago.banco_id)
                    })
                });

                if (response.ok) {
                    this.nuevoMedioPago = { tipo: '', nombre: '', banco_id: '' };
                    await this.cargarMediosPago();
                    alert('Medio de pago creado exitosamente');
                } else {
                    alert('Error al crear medio de pago');
                }
            } catch (error) {
                console.error('Error creando medio de pago:', error);
                alert('Error al crear medio de pago');
            }
        },

        async eliminarMedioPago(medioPagoId) {
            if (!confirm('¿Eliminar este medio de pago?')) return;

            try {
                const response = await fetch(`${API_URL}/medios-pago/${medioPagoId}`, {
                    method: 'DELETE'
                });

                if (response.ok) {
                    await this.cargarMediosPago();
                    alert('Medio de pago eliminado');
                } else {
                    alert('Error al eliminar medio de pago');
                }
            } catch (error) {
                console.error('Error eliminando medio de pago:', error);
                alert('Error al eliminar medio de pago');
            }
        },

        getBancoNombre(bancoId) {
            const banco = this.bancos.find(b => b.id === bancoId);
            return banco ? banco.nombre : 'N/A';
        },

        // Cuentas Bancarias
        async cargarCuentasBancarias() {
            try {
                const response = await fetch(`${API_URL}/cuentas-bancarias`);
                this.cuentasBancarias = await response.json();
            } catch (error) {
                console.error('Error cargando cuentas bancarias:', error);
            }
        },

        iniciarNuevaCuenta() {
            this.nuevaCuenta = {
                nombre: '',
                banco_id: '',
                saldo_transaccional: 0,
                saldo_ahorros: 0,
                tipo_cuenta: 'Ahorro'
            };
            this.modalNuevaCuenta = true;
        },

        async crearCuentaBancaria() {
            try {
                const response = await fetch(`${API_URL}/cuentas-bancarias`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        nombre: this.nuevaCuenta.nombre,
                        banco_id: parseInt(this.nuevaCuenta.banco_id),
                        saldo_transaccional: parseFloat(this.nuevaCuenta.saldo_transaccional) || 0,
                        saldo_ahorros: parseFloat(this.nuevaCuenta.saldo_ahorros) || 0,
                        tipo_cuenta: this.nuevaCuenta.tipo_cuenta
                    })
                });

                if (response.ok) {
                    this.modalNuevaCuenta = false;
                    await this.cargarCuentasBancarias();
                    alert('Cuenta bancaria creada exitosamente');
                } else {
                    const error = await response.json();
                    alert('Error al crear cuenta: ' + (error.detail || 'Error desconocido'));
                }
            } catch (error) {
                console.error('Error creando cuenta bancaria:', error);
                alert('Error al crear la cuenta bancaria');
            }
        },

        async actualizarSaldoCuenta(cuentaId, campo, valor) {
            try {
                const response = await fetch(`${API_URL}/cuentas-bancarias/${cuentaId}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        [campo]: parseFloat(valor)
                    })
                });

                if (response.ok) {
                    await this.cargarCuentasBancarias();
                } else {
                    alert('Error al actualizar la cuenta');
                }
            } catch (error) {
                console.error('Error actualizando cuenta:', error);
                alert('Error al actualizar la cuenta');
            }
        },

        async eliminarCuentaBancaria(cuentaId, nombre) {
            if (!confirm(`¿Eliminar la cuenta "${nombre}"?\n\nEsto también eliminará todos los ingresos asociados.`)) {
                return;
            }

            try {
                const response = await fetch(`${API_URL}/cuentas-bancarias/${cuentaId}`, {
                    method: 'DELETE'
                });

                if (response.ok) {
                    await this.cargarCuentasBancarias();
                    alert('Cuenta eliminada exitosamente');
                } else {
                    alert('Error al eliminar la cuenta');
                }
            } catch (error) {
                console.error('Error eliminando cuenta:', error);
                alert('Error al eliminar la cuenta');
            }
        },

        calcularSaldoTotal(cuenta) {
            return (cuenta.saldo_transaccional || 0) + (cuenta.saldo_ahorros || 0);
        },

        calcularResumenCuentas() {
            const totalTransaccional = this.cuentasBancarias.reduce((sum, c) => sum + (c.saldo_transaccional || 0), 0);
            const totalAhorros = this.cuentasBancarias.reduce((sum, c) => sum + (c.saldo_ahorros || 0), 0);
            const totalGeneral = totalTransaccional + totalAhorros;
            return { totalTransaccional, totalAhorros, totalGeneral };
        },

        // Ingresos
        async cargarIngresos() {
            try {
                const response = await fetch(
                    `${API_URL}/ingresos?mes=${this.mesSeleccionado}&anio=${this.anioSeleccionado}&limit=100`
                );
                this.ingresos = await response.json();
            } catch (error) {
                console.error('Error cargando ingresos:', error);
            }
        },

        async crearIngreso() {
            try {
                const payload = {
                    fecha: this.nuevoIngreso.fecha,
                    monto: parseFloat(this.nuevoIngreso.monto),
                    descripcion: this.nuevoIngreso.descripcion,
                    categoria_ingreso: this.nuevoIngreso.categoria_ingreso,
                    cuenta_bancaria_id: parseInt(this.nuevoIngreso.cuenta_bancaria_id)
                };

                const response = await fetch(`${API_URL}/ingresos`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });

                if (response.ok) {
                    // Resetear formulario
                    this.nuevoIngreso = {
                        fecha: new Date().toISOString().split('T')[0],
                        monto: '',
                        descripcion: '',
                        categoria_ingreso: 'Salario',
                        cuenta_bancaria_id: ''
                    };

                    // Recargar datos
                    await this.cargarIngresos();
                    await this.cargarCuentasBancarias();

                    alert('Ingreso registrado exitosamente');
                } else {
                    const error = await response.json();
                    alert('Error al registrar ingreso: ' + (error.detail || 'Error desconocido'));
                }
            } catch (error) {
                console.error('Error creando ingreso:', error);
                alert('Error al registrar el ingreso');
            }
        },

        async eliminarIngreso(ingresoId) {
            if (!confirm('¿Estás seguro de eliminar este ingreso?')) return;

            try {
                const response = await fetch(`${API_URL}/ingresos/${ingresoId}`, {
                    method: 'DELETE'
                });

                if (response.ok) {
                    await this.cargarIngresos();
                    await this.cargarCuentasBancarias();
                    alert('Ingreso eliminado exitosamente');
                } else {
                    alert('Error al eliminar el ingreso');
                }
            } catch (error) {
                console.error('Error eliminando ingreso:', error);
                alert('Error al eliminar el ingreso');
            }
        },

        getCuentaNombre(cuentaId) {
            const cuenta = this.cuentasBancarias.find(c => c.id === cuentaId);
            return cuenta ? cuenta.nombre : 'N/A';
        },

        calcularTotalIngresos() {
            return this.ingresos.reduce((sum, ing) => sum + (ing.monto || 0), 0);
        },

        get gastosAMostrar() {
            return this.mostrarTodos ? this.gastos : this.gastos.slice(0, 10);
        },

        get ingresosAMostrar() {
            return this.mostrarTodosIngresos ? this.ingresos : this.ingresos.slice(0, 10);
        }
    };
}
