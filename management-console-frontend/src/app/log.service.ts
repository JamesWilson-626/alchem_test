import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface LogEntry {
  id?: number;
  source: string;
  log: string;
}

@Injectable({
  providedIn: 'root'
})
export class LogService {
  private apiUrl = 'http://localhost:8000'; // Your FastAPI URL

  constructor(private http: HttpClient) {}

  getAllLogs(): Observable<LogEntry[]> {
    return this.http.get<LogEntry[]>(`${this.apiUrl}/logs/`);
  }

  addLog(log: LogEntry): Observable<LogEntry> {
    return this.http.post<LogEntry>(`${this.apiUrl}/logs/`, log);
  }

  updateLog(id: number, log: LogEntry): Observable<LogEntry> {
    return this.http.put<LogEntry>(`${this.apiUrl}/logs/${id}/`, log);
  }

  deleteLog(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/logs/${id}/`);
  }

  clearAllLogs(): Observable<any> {
    return this.http.delete(`${this.apiUrl}/logs/clear-all/`);
  }
}