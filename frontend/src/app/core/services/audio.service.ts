import { Injectable } from '@angular/core';

export enum AudioType {
  GENERAL = 'general',
  TUTORIALES = 'tutoriales',
  EJERCICIOS = 'ejercicios'
}

@Injectable({
  providedIn: 'root'
})
export class AudioService {
  private audios: Map<AudioType, HTMLAudioElement> = new Map();
  private currentAudio: HTMLAudioElement | null = null;
  private audioStates: Map<AudioType, boolean> = new Map();

  constructor() {
    this.initializeAudios();
    this.loadAudioStates();
    
    // Si es la primera vez (no hay estados guardados), activar el audio general por defecto
    const savedStates = localStorage.getItem('audioStates');
    if (!savedStates) {
      this.audioStates.set(AudioType.GENERAL, true);
      this.saveAudioStates();
      console.log('Primera vez: Audio general activado por defecto');
    }
  }

  private initializeAudios(): void {
    // Inicializar los tres tipos de audio
    const audioGeneral = new Audio('/audios/audio%20general.mp3');
    audioGeneral.loop = true;
    audioGeneral.volume = 0.2; // Volumen bajo (20%)
    this.audios.set(AudioType.GENERAL, audioGeneral);

    const audioTutoriales = new Audio('/audios/audio%20tutoriales.mp3');
    audioTutoriales.loop = true;
    audioTutoriales.volume = 0.2;
    this.audios.set(AudioType.TUTORIALES, audioTutoriales);

    const audioEjercicios = new Audio('/audios/audio%20ejercicios.mp3');
    audioEjercicios.loop = true;
    audioEjercicios.volume = 0.2;
    this.audios.set(AudioType.EJERCICIOS, audioEjercicios);
    
    console.log('Audios inicializados correctamente');
  }

  private loadAudioStates(): void {
    // Cargar estados guardados del localStorage
    const savedStates = localStorage.getItem('audioStates');
    if (savedStates) {
      const states = JSON.parse(savedStates);
      Object.keys(states).forEach(key => {
        this.audioStates.set(key as AudioType, states[key]);
      });
    }
  }

  private saveAudioStates(): void {
    const states: any = {};
    this.audioStates.forEach((value, key) => {
      states[key] = value;
    });
    localStorage.setItem('audioStates', JSON.stringify(states));
  }

  play(type: AudioType): void {
    // Detener cualquier audio que esté sonando
    this.stopAll();

    const audio = this.audios.get(type);
    if (audio) {
      // Intentar reproducir
      const playPromise = audio.play();
      
      if (playPromise !== undefined) {
        playPromise
          .then(() => {
            // Reproducción exitosa
            this.currentAudio = audio;
            this.audioStates.set(type, true);
            this.saveAudioStates();
            console.log(`Audio ${type} reproduciendo`);
          })
          .catch(err => {
            console.warn(`Error al reproducir audio ${type}:`, err.message);
            // Si falla, marcar como no reproduciendo pero mantener el estado de "activado"
            // para que se intente reproducir cuando el usuario interactúe
            if (err.name === 'NotAllowedError') {
              console.log('El navegador requiere interacción del usuario. El audio se reproducirá al hacer clic.');
            }
          });
      }
    }
  }

  pause(type: AudioType): void {
    const audio = this.audios.get(type);
    if (audio) {
      audio.pause();
      if (this.currentAudio === audio) {
        this.currentAudio = null;
      }
      this.audioStates.set(type, false);
      this.saveAudioStates();
    }
  }

  pauseAndReturnToGeneral(type: AudioType): void {
    // Pausar el audio actual
    this.pause(type);
    
    // Si no es el audio general, volver a reproducir el general
    if (type !== AudioType.GENERAL) {
      // Pequeño delay para evitar conflictos
      setTimeout(() => {
        this.play(AudioType.GENERAL);
      }, 100);
    }
  }

  toggle(type: AudioType): boolean {
    const isPlaying = this.isPlaying(type);
    if (isPlaying) {
      this.pause(type);
    } else {
      this.play(type);
    }
    return !isPlaying;
  }

  stopAll(): void {
    this.audios.forEach(audio => {
      audio.pause();
      audio.currentTime = 0;
    });
    this.currentAudio = null;
  }

  isPlaying(type: AudioType): boolean {
    const audio = this.audios.get(type);
    return audio ? !audio.paused : false;
  }

  isEnabled(type: AudioType): boolean {
    return this.audioStates.get(type) || false;
  }

  setVolume(type: AudioType, volume: number): void {
    const audio = this.audios.get(type);
    if (audio) {
      audio.volume = Math.max(0, Math.min(1, volume));
    }
  }

  getCurrentAudioType(): AudioType | null {
    if (!this.currentAudio) return null;
    
    for (const [type, audio] of this.audios.entries()) {
      if (audio === this.currentAudio) {
        return type;
      }
    }
    return null;
  }
}
