import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class MockDataService {

  private storageKey = 'mock_db';

  private defaultData = {
    usuarios: [
      { id: 1, nombre: 'Director', apellido: 'Admin',   email: 'director@gmail.com', role: 'director', activo: true },
      { id: 2, nombre: 'Carlos',   apellido: 'Mendoza', email: 'profecarlos@gmail.com', role: 'profesor', activo: true },
      { id: 3, nombre: 'Ayllon',   apellido: 'Rivera',  email: 'ayllon814@gmail.com',   role: 'profesor', activo: true },
      { id: 4, nombre: 'Jose',     apellido: 'Padre',   email: 'jose@gmail.com',         role: 'padre',    activo: true },
      { id: 5, nombre: 'Fabricio', apellido: 'Padre',   email: 'fabricio@gmail.com',     role: 'padre',    activo: true },
      { id: 6, nombre: 'Amilcar',  apellido: 'Padre',   email: 'amilcar@gmail.com',      role: 'padre',    activo: true },
      { id: 7, nombre: 'Carla',    apellido: 'Madre',   email: 'carla@gmail.com',        role: 'padre',    activo: true },
    ],
    ninos: [
      { id: 1, nombre: 'Alejandra', apellido: 'Lopez',   pin: '8778', edad: 10, grado: 4, profesor_id: 2, padre_id: 4, monedas: 120, nivel: 3, experiencia: 280, avatar: 'nina1', racha_dias: 5 },
      { id: 2, nombre: 'Carla',     apellido: 'Mendez',  pin: '5079', edad: 9,  grado: 3, profesor_id: 2, padre_id: 7, monedas: 80,  nivel: 2, experiencia: 150, avatar: 'nina2', racha_dias: 2 },
      { id: 3, nombre: 'Mariano',   apellido: 'Torres',  pin: '1220', edad: 11, grado: 5, profesor_id: 3, padre_id: 5, monedas: 200, nivel: 4, experiencia: 380, avatar: 'nino1', racha_dias: 7 },
      { id: 4, nombre: 'Cristian',  apellido: 'Vargas',  pin: '3213', edad: 10, grado: 4, profesor_id: 3, padre_id: 6, monedas: 60,  nivel: 2, experiencia: 120, avatar: 'nino2', racha_dias: 1 },
      { id: 5, nombre: 'Miguel',    apellido: 'Quispe',  pin: '9685', edad: 9,  grado: 3, profesor_id: 2, padre_id: 5, monedas: 95,  nivel: 2, experiencia: 190, avatar: 'nino1', racha_dias: 3 },
      { id: 6, nombre: 'Jose',      apellido: 'Mamani',  pin: '7895', edad: 11, grado: 5, profesor_id: 3, padre_id: 4, monedas: 150, nivel: 3, experiencia: 310, avatar: 'nino2', racha_dias: 4 },
    ],
    tareas: [
      { id: 1, titulo: 'Sumas y Restas', descripcion: 'Practica operaciones básicas', tipo_ejercicio: 'multiple', profesor_id: 2,
        nino_ids: [1, 2, 5],
        ejercicios: [
          { id: 1, pregunta: '¿Cuánto es 5 + 3?', opciones: ['6','7','8','9'], respuesta_correcta: '8', explicacion: '5 más 3 igual a 8', orden: 0 },
          { id: 2, pregunta: '¿Cuánto es 10 - 4?', opciones: ['5','6','7','8'], respuesta_correcta: '6', explicacion: '10 menos 4 igual a 6', orden: 1 },
          { id: 3, pregunta: '¿Cuánto es 7 + 6?', opciones: ['11','12','13','14'], respuesta_correcta: '13', explicacion: '7 más 6 igual a 13', orden: 2 },
        ]
      },
      { id: 2, titulo: 'Multiplicación', descripcion: 'Tablas del 2 al 5', tipo_ejercicio: 'multiple', profesor_id: 2,
        nino_ids: [1, 5],
        ejercicios: [
          { id: 4, pregunta: '¿Cuánto es 3 x 4?', opciones: ['10','11','12','13'], respuesta_correcta: '12', explicacion: '3 por 4 igual a 12', orden: 0 },
          { id: 5, pregunta: '¿Cuánto es 5 x 5?', opciones: ['20','25','30','35'], respuesta_correcta: '25', explicacion: '5 por 5 igual a 25', orden: 1 },
        ]
      },
      { id: 3, titulo: 'Lectura Comprensiva', descripcion: 'Comprensión de textos cortos', tipo_ejercicio: 'multiple', profesor_id: 3,
        nino_ids: [3, 4, 6],
        ejercicios: [
          { id: 6, pregunta: '¿Cuál es el personaje principal del cuento?', opciones: ['El lobo','Caperucita','La abuela','El cazador'], respuesta_correcta: 'Caperucita', explicacion: 'Caperucita es la protagonista', orden: 0 },
        ]
      },
    ],
    progreso: [
      { nino_id: 1, tarea_id: 1, completada: true,  puntuacion: 90, fecha: '2025-04-01' },
      { nino_id: 1, tarea_id: 2, completada: false, puntuacion: 0,  fecha: null },
      { nino_id: 2, tarea_id: 1, completada: false, puntuacion: 0,  fecha: null },
      { nino_id: 3, tarea_id: 3, completada: true,  puntuacion: 100, fecha: '2025-04-02' },
      { nino_id: 5, tarea_id: 1, completada: true,  puntuacion: 80, fecha: '2025-04-03' },
    ],
    logros: [
      { id: 1, nombre: 'Primera Tarea',    descripcion: 'Completaste tu primera tarea',    tipo: 'bronce', icono: 'star',        valor_requerido: 1,   condicion: 'tareas_completadas' },
      { id: 2, nombre: 'Estudioso',        descripcion: 'Completaste 3 tareas',            tipo: 'plata',  icono: 'book',        valor_requerido: 3,   condicion: 'tareas_completadas' },
      { id: 3, nombre: 'Experto',          descripcion: 'Completaste 5 tareas',            tipo: 'oro',    icono: 'graduation-cap', valor_requerido: 5, condicion: 'tareas_completadas' },
      { id: 4, nombre: 'Racha de 3 días',  descripcion: 'Estudiaste 3 días seguidos',      tipo: 'bronce', icono: 'fire',        valor_requerido: 3,   condicion: 'racha' },
      { id: 5, nombre: 'Racha de 7 días',  descripcion: 'Estudiaste 7 días seguidos',      tipo: 'oro',    icono: 'fire',        valor_requerido: 7,   condicion: 'racha' },
      { id: 6, nombre: '100 Monedas',      descripcion: 'Acumulaste 100 monedas',          tipo: 'plata',  icono: 'coins',       valor_requerido: 100, condicion: 'monedas' },
    ],
    logros_nino: [
      { nino_id: 1, logro_id: 1, fecha_obtenido: '2025-04-01' },
      { nino_id: 1, logro_id: 4, fecha_obtenido: '2025-04-03' },
      { nino_id: 1, logro_id: 6, fecha_obtenido: '2025-04-02' },
      { nino_id: 3, logro_id: 1, fecha_obtenido: '2025-04-02' },
      { nino_id: 3, logro_id: 4, fecha_obtenido: '2025-04-03' },
      { nino_id: 3, logro_id: 5, fecha_obtenido: '2025-04-04' },
      { nino_id: 5, logro_id: 1, fecha_obtenido: '2025-04-03' },
    ],
    skins: [
      { id: 1, nombre: 'Astronauta',  descripcion: 'Traje espacial',    imagen: 'astronauta',  precio: 50,  rareza: 'comun',      activo: true },
      { id: 2, nombre: 'Superhéroe',  descripcion: 'Capa y máscara',    imagen: 'superheroe',  precio: 100, rareza: 'raro',       activo: true },
      { id: 3, nombre: 'Dragón',      descripcion: 'Disfraz de dragón', imagen: 'dragon',      precio: 200, rareza: 'legendario', activo: true },
      { id: 4, nombre: 'Ninja',       descripcion: 'Traje ninja',       imagen: 'ninja',       precio: 80,  rareza: 'raro',       activo: true },
      { id: 5, nombre: 'Pirata',      descripcion: 'Disfraz pirata',    imagen: 'pirata',      precio: 60,  rareza: 'comun',      activo: false },
    ],
    stickers: [
      { id: 1, nombre: 'Estrella',    descripcion: 'Sticker estrella',  imagen: 'estrella',    precio: 20,  rareza: 'comun',      activo: true },
      { id: 2, nombre: 'Cohete',      descripcion: 'Sticker cohete',    imagen: 'cohete',      precio: 40,  rareza: 'raro',       activo: true },
      { id: 3, nombre: 'Arcoíris',    descripcion: 'Sticker arcoíris',  imagen: 'arcoiris',    precio: 30,  rareza: 'comun',      activo: true },
      { id: 4, nombre: 'Unicornio',   descripcion: 'Sticker unicornio', imagen: 'unicornio',   precio: 150, rareza: 'legendario', activo: true },
    ]
  };

  private db: any;

  constructor() {
    // Siempre recargar datos frescos en desarrollo
    localStorage.removeItem(this.storageKey);
    this.db = JSON.parse(JSON.stringify(this.defaultData));
    this.save();
  }

  private save(): void {
    localStorage.setItem(this.storageKey, JSON.stringify(this.db));
  }

  // ── USUARIOS ──────────────────────────────────────────────────────────────
  getUsuarios()          { return [...this.db.usuarios]; }
  suspenderUsuario(id: number) { this.db.usuarios.find((u:any) => u.id === id).activo = false; this.save(); }
  activarUsuario(id: number)   { this.db.usuarios.find((u:any) => u.id === id).activo = true;  this.save(); }
  eliminarUsuario(id: number)  { this.db.usuarios = this.db.usuarios.filter((u:any) => u.id !== id); this.save(); }

  // ── NIÑOS ─────────────────────────────────────────────────────────────────
  getNinos()                        { return [...this.db.ninos]; }
  getNinoByPin(pin: string)         { return this.db.ninos.find((n:any) => n.pin === pin) ?? null; }
  getNinoById(id: number)           { return this.db.ninos.find((n:any) => n.id === id) ?? null; }
  getNinosByProfesor(profId: number){ return this.db.ninos.filter((n:any) => Number(n.profesor_id) === Number(profId)); }
  getNinosByPadre(padreId: number)  { return this.db.ninos.filter((n:any) => Number(n.padre_id)    === Number(padreId)); }
  updateNinoAvatar(id: number, avatar: string) {
    const n = this.db.ninos.find((n:any) => n.id === id);
    if (n) { n.avatar = avatar; this.save(); }
  }

  // ── TAREAS ────────────────────────────────────────────────────────────────
  getTareas()                         { return [...this.db.tareas]; }
  getTareasByProfesor(profId: number) { return this.db.tareas.filter((t:any) => Number(t.profesor_id) === Number(profId)); }
  getTareaById(id: number)            { return this.db.tareas.find((t:any) => t.id === id) ?? null; }

  getTareasByNino(ninoId: number) {
    return this.db.tareas.filter((t:any) => t.nino_ids?.includes(ninoId));
  }

  crearTarea(data: any, profesorId: number): any {
    const id = Math.max(0, ...this.db.tareas.map((t:any) => t.id)) + 1;
    const tarea = { ...data, id, profesor_id: profesorId,
      ejercicios: (data.ejercicios || []).map((e:any, i:number) => ({ ...e, id: Date.now() + i, orden: i }))
    };
    this.db.tareas.push(tarea);
    this.save();
    return tarea;
  }

  editarTarea(id: number, data: any): any {
    const idx = this.db.tareas.findIndex((t:any) => t.id === id);
    if (idx !== -1) {
      this.db.tareas[idx] = { ...this.db.tareas[idx], ...data,
        ejercicios: (data.ejercicios || []).map((e:any, i:number) => ({ ...e, id: Date.now() + i, orden: i }))
      };
      this.save();
      return this.db.tareas[idx];
    }
  }

  eliminarTarea(id: number): void {
    this.db.tareas = this.db.tareas.filter((t:any) => t.id !== id);
    this.db.progreso = this.db.progreso.filter((p:any) => p.tarea_id !== id);
    this.save();
  }

  // ── PROGRESO ──────────────────────────────────────────────────────────────
  getProgresoNino(ninoId: number) { return this.db.progreso.filter((p:any) => p.nino_id === ninoId); }

  completarTarea(ninoId: number, tareaId: number, puntuacion: number): void {
    const existing = this.db.progreso.find((p:any) => p.nino_id === ninoId && p.tarea_id === tareaId);
    if (existing) {
      existing.completada = true; existing.puntuacion = puntuacion; existing.fecha = new Date().toISOString().split('T')[0];
    } else {
      this.db.progreso.push({ nino_id: ninoId, tarea_id: tareaId, completada: true, puntuacion, fecha: new Date().toISOString().split('T')[0] });
    }
    // Dar monedas y XP
    const nino = this.db.ninos.find((n:any) => n.id === ninoId);
    if (nino) {
      nino.monedas += Math.round(puntuacion / 10);
      nino.experiencia += puntuacion;
      nino.nivel = Math.floor(nino.experiencia / 100) + 1;
      nino.racha_dias += 1;
    }
    this.verificarLogros(ninoId);
    this.save();
  }

  // ── LOGROS ────────────────────────────────────────────────────────────────
  getLogros()                    { return [...this.db.logros]; }
  getLogrosNino(ninoId: number)  {
    const ids = this.db.logros_nino.filter((l:any) => l.nino_id === ninoId);
    return ids.map((ln:any) => ({
      ...this.db.logros.find((l:any) => l.id === ln.logro_id),
      pivot: { fecha_obtenido: ln.fecha_obtenido }
    }));
  }

  private verificarLogros(ninoId: number): void {
    const nino = this.db.ninos.find((n:any) => n.id === ninoId);
    if (!nino) return;
    const tareasCompletadas = this.db.progreso.filter((p:any) => p.nino_id === ninoId && p.completada).length;
    const yaGanados = this.db.logros_nino.filter((l:any) => l.nino_id === ninoId).map((l:any) => l.logro_id);

    this.db.logros.forEach((logro:any) => {
      if (yaGanados.includes(logro.id)) return;
      let cumple = false;
      if (logro.condicion === 'tareas_completadas' && tareasCompletadas >= logro.valor_requerido) cumple = true;
      if (logro.condicion === 'racha'   && nino.racha_dias  >= logro.valor_requerido) cumple = true;
      if (logro.condicion === 'monedas' && nino.monedas     >= logro.valor_requerido) cumple = true;
      if (cumple) this.db.logros_nino.push({ nino_id: ninoId, logro_id: logro.id, fecha_obtenido: new Date().toISOString().split('T')[0] });
    });
  }

  // ── INVENTARIO ─────────────────────────────────────────────────────────
  getInventario() { return { skins: [...this.db.skins], stickers: [...this.db.stickers] }; }
  toggleInventario(tipo: string, id: number): void {
    const lista = tipo === 'skin' ? this.db.skins : this.db.stickers;
    const item  = lista.find((i: any) => i.id === id);
    if (item) { item.activo = !item.activo; this.save(); }
  }

  // ── DASHBOARD ─────────────────────────────────────────────────────────────
  getDashboardDirector() {
    return {
      total_profesores: this.db.usuarios.filter((u:any) => u.role === 'profesor').length,
      total_padres:     this.db.usuarios.filter((u:any) => u.role === 'padre').length,
      total_ninos:      this.db.ninos.length,
      total_tareas:     this.db.tareas.length,
    };
  }

  getDashboardProfesor(profId: number) {
    return this.getNinosByProfesor(profId);
  }

  getDashboardPadre(padreId: number) {
    const hijos = this.getNinosByPadre(padreId);
    return hijos.map((h:any) => ({
      ...h,
      tareas_completadas: this.db.progreso.filter((p:any) => p.nino_id === h.id && p.completada).length,
      logros: this.getLogrosNino(h.id).length
    }));
  }
}
