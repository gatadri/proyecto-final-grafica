export interface User {
  id: number;
  name: string;
  nombre: string;
  apellido: string;
  email: string;
  role: 'director' | 'profesor' | 'padre';
  activo: boolean;
  hijos: Nino[];
}

export interface Nino {
  id: number;
  nombre: string;
  apellido: string;
  pin: string;
  nivel: number;
  experiencia: number;
  monedas: number;
  avatar: string;
  racha_dias: number;
  ultima_actividad: string | null;
  progreso?: number;
  profesor?: {
    id: number;
    nombre: string;
    apellido: string;
    email: string;
  };
  tareas: Tarea[];
  estadisticas: {
    monedas: number;
    nivel: number;
    experiencia: number;
    racha_dias: number;
  };
}

export interface Tarea {
  id: number;
  titulo: string;
  descripcion: string;
  tipo_ejercicio: string;
  ejercicios?: Ejercicio[];
  ninos?: { id: number; nombre: string; apellido: string }[];
}

export interface Ejercicio {
  id: number;
  pregunta: string;
  opciones: string[];
  respuesta_correcta: string;
  explicacion?: string;
}

export interface Skin {
  id: number;
  nombre: string;
  descripcion: string;
  imagen: string;
  precio: number;
  rareza: 'comun' | 'raro' | 'legendario';
  categoria: string | null;
  activo: boolean;
}

export interface Sticker {
  id: number;
  nombre: string;
  descripcion: string;
  imagen: string;
  precio: number;
  rareza: 'comun' | 'raro' | 'legendario';
  categoria: string | null;
  pdf_template: string | null;
  activo: boolean;
}

export interface Logro {
  id: number;
  nombre: string;
  descripcion: string;
  tipo: 'bronce' | 'plata' | 'oro';
  condicion: string;
  valor_requerido: number;
  icono: string;
  activo: boolean;
  pivot?: { fecha_obtenido: string };
}

export interface AuthResponse {
  token: string;
  user: User;
}

export interface NinoLoginResponse {
  nino: Nino;
}
