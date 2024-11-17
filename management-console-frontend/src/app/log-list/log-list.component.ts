import { Component, OnInit } from '@angular/core';
import { LogService } from '../log.service';


@Component({
  selector: 'app-log-list',
  templateUrl: './log-list.component.html',
  styleUrls: ['./log-list.component.css'],
})
export class LogListComponent implements OnInit {
  logs: any[] = [];

  constructor(private logService: LogService) {}

  ngOnInit(): void {
    this.logService.getAllLogs().subscribe((data: any[]) => {
      this.logs = data;
    });
  }
  
}
