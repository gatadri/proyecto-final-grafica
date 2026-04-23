import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

export type AvatarExpression =
  | 'feliz'
  | 'sorprendido'
  | 'guino'
  | 'pensando'
  | 'triste'
  | 'enojado';

@Injectable({ providedIn: 'root' })
export class AvatarStateService {
  private expressionSubject = new BehaviorSubject<AvatarExpression>('feliz');
  expression$ = this.expressionSubject.asObservable();

  setExpression(expression: AvatarExpression): void {
    this.expressionSubject.next(expression);
  }

  resetExpression(): void {
    this.expressionSubject.next('feliz');
  }
}
