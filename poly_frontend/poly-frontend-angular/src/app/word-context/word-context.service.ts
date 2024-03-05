import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class WordContextService {
  private apiUrl = 'http://localhost:8000/api/word-with-context/';

  constructor(private http: HttpClient) {}

  postWordWithContext(word: string, context: string): Observable<any> {
    return this.http.post(this.apiUrl, { word, context });
  }
}