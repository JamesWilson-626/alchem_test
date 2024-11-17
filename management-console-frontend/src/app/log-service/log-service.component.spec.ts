import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LogServiceComponent } from './log.service.';

describe('LogServiceComponent', () => {
  let component: LogServiceComponent;
  let fixture: ComponentFixture<LogServiceComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LogServiceComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(LogServiceComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
