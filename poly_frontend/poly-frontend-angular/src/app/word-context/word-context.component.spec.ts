import { ComponentFixture, TestBed } from '@angular/core/testing';

import { WordContextComponent } from './word-context.component';

describe('WordContextComponent', () => {
  let component: WordContextComponent;
  let fixture: ComponentFixture<WordContextComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [WordContextComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(WordContextComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
