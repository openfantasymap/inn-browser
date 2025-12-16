import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BuildRoomComponent } from './build-room.component';

describe('BuildRoomComponent', () => {
  let component: BuildRoomComponent;
  let fixture: ComponentFixture<BuildRoomComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [BuildRoomComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(BuildRoomComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
