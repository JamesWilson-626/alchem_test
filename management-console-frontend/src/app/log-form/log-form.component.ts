import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { LogService, LogEntry } from '../log.service';

@Component({
  selector: 'app-log-form',
  templateUrl: './log-form.component.html',
  styleUrls: ['./log-form.component.css']
})
export class LogFormComponent {
  log: LogEntry = {
    source: '',
    log: ''
  };

  constructor(
    private logService: LogService,
    private router: Router
  ) {}

  submitLog() {
    if (this.log.source && this.log.log) {
      this.logService.addLog(this.log).subscribe({
        next: () => {
          // Navigate back to log list after successful submission
          this.router.navigate(['/logs']);
        },
        error: (error) => {
          console.error('Error adding log:', error);
          // Handle error (you might want to show an error message to the user)
        }
      });
    }
  }
}